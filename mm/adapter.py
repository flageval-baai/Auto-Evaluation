import re
import os
import os.path as osp
import json
from typing import Dict, Any, Optional, Union, List
from concurrent.futures import ThreadPoolExecutor, as_completed
import atexit
import signal
from importlib.metadata import version, PackageNotFoundError

from flagevalmm.server import ServerDataset
from flagevalmm.models.base_model_adapter import BaseModelAdapter
from flagevalmm.models import HttpClient, Claude, Gemini, GPT, Hunyuan
from flagevalmm.models.api_response import ApiResponse, ProcessResult
from flagevalmm.server.model_server import ModelServer
from flagevalmm.server.utils import get_random_port
from flagevalmm.common.logger import get_logger
from flagevalmm.server.utils import parse_args

logger = get_logger(__name__)

def parse_final_answer(text_string: str) -> str | None:
    """
    从一个以 </answer> 标签结束的字符串中提取内容。
    它专门用于解析 "一些内容 </answer>" 这样的格式。

    Args:
        text_string (str): 输入的字符串。

    Returns:
        str | None: 提取并清理后的内容字符串，如果未找到匹配项则返回 None。
    """
    # 正则表达式解释:
    # (.*?)   - 非贪婪模式捕获所有字符，直到下一个模式匹配为止。这是我们想要的内容。
    # \s* - 匹配 </answer> 标签前的任意空白字符（空格、换行符等）。
    # </answer> - 匹配文字字符串 "</answer>"。
    # re.DOTALL - 使 '.' 特殊字符可以匹配包括换行符在内的任意字符。
    match = re.search(r"(.*?)\s*</answer>", text_string, re.DOTALL)

    if match:
        # group(1) 获取第一个捕获组的内容，即 (.*?) 匹配到的部分
        # .strip() 用于移除内容前后可能存在的无用空白
        return match.group(1).strip()

    # 如果没有找到匹配项，返回 None
    return None

class ModelAdapter(BaseModelAdapter):
    def __init__(
        self,
        server_ip: str,
        server_port: int,
        timeout: int,
        model_type: Optional[str] = None,
        extra_cfg: Optional[Union[str, Dict]] = None,
        local_mode: bool = False,
        task_names: List[str] = None,
        **kwargs,
    ):
        self.model_type = model_type
        super().__init__(
            server_ip=server_ip,
            server_port=server_port,
            timeout=timeout,
            extra_cfg=extra_cfg,
            local_mode=local_mode,
            task_names=task_names,
            **kwargs,
        )

        atexit.register(self.cleanup)
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, signum, frame):
        logger.info(f"Received signal {signum}, cleaning up...")
        self.cleanup()
        os._exit(0)

    def model_init(self, task_info: Dict):
        if task_info.get("backend", None):
            self.model_server = self.launch_model(task_info)

        model_config_keys = [
            "model_name",
            "url",
            "base_url",
            "api_key",
            "use_cache",
            "max_image_size",
            "min_short_side",
            "max_long_side",
            "max_tokens",
            "temperature",
            "chat_name",
            "max_num_frames",
            "stream",
            "system_prompt",
            "num_infers",
            "reasoning",
        ]
        print(f"task_info: {task_info}")
        model_config = {k: task_info[k] for k in model_config_keys if k in task_info}

        model_type_map = {
            "http": HttpClient,
            "claude": Claude,
            "gemini": Gemini,
            "gpt": GPT,
            "hunyuan": Hunyuan,
        }
        model_type = self.model_type or task_info.get("model_type", "http")
        self.model = model_type_map[model_type](**model_config)

    def launch_model(self, task_info: Dict):
        if task_info.get("server_port"):
            port = task_info.get("server_port")
        else:
            port = get_random_port()
        # replace port in url
        url = re.sub(
            r":(\d+)/",
            f":{port}/",
            task_info.get("url", "http://localhost:8000/v1/chat/completions"),
        )
        task_info["url"] = url

        model_name = task_info["model_name"]
        backend = task_info.get("backend", "vllm")
        model_server = ModelServer(
            model_name,
            port=port,
            backend=backend,
            extra_args=task_info.get("extra_args", None),
        )
        task_info["execute_cmd"] = model_server.execute_cmd
        important_packages = [backend, "transformers", "torch"]
        task_info["important_packages"] = []
        for package in important_packages:
            try:
                version_pkg = version(package)
                task_info["important_packages"].append(f"{package}=={version_pkg}")
            except PackageNotFoundError:
                task_info["important_packages"].append(f"{package} not installed")
        return model_server

    def _process_single_result(self, single_result: ApiResponse) -> Dict[str, Any]:
        """
        Process a single inference result and extract content, reason, and usage.

        Args:
            single_result: Single inference result (string or ApiResponse)

        Returns:
            Dictionary containing processed content, reason, and usage
        """
        usage_info = None
        reason = ""

        # Extract content and usage from ApiResponse
        content = single_result.content
        if single_result.usage:
            usage_info = single_result.usage.to_dict()

        # Split reasoning and answer if present
        if "</think>" in content:
            reason, answer = content.split("</think>", 1)
            reason += "</think>"
        else:
            answer = parse_final_answer(content)

        return {"answer": answer, "reason": reason, "usage": usage_info}

    def process_single_item(self, i, inter_results_dir):
        question_id, multi_modal_data, qs = self.dataset[i]
        qs = f"{qs}<think></think><answer>"
        inter_results_file = osp.join(inter_results_dir, f"{question_id}.json")
        if osp.exists(inter_results_file):
            logger.info(f"Skipping {question_id} because it already exists")
            with open(inter_results_file, "r") as f:
                data = json.load(f)
                reason = data.get("reason", "")
                result = data.get("answer", "")
                usage_info = data.get("usage", None)
                return ProcessResult(
                    question_id=question_id,
                    question=qs,
                    answer=result,
                    reason=reason,
                    usage=usage_info,
                )
        logger.info(f"Processing {question_id}")
        logger.info(qs)
        messages = self.model.build_message(qs, multi_modal_data=multi_modal_data)

        try:
            result = self.model.infer(messages)
            if isinstance(result, list):
                # Multiple inferences case
                inference_answers = {}
                reasons = []
                usages = []

                for i, single_result in enumerate(result):
                    processed = self._process_single_result(single_result)
                    inference_answers[f"inference_{i}"] = processed["answer"]
                    reasons.append(processed["reason"])
                    if processed["usage"]:
                        usages.append(processed["usage"])

                final_result = inference_answers
                final_reason = reasons  # Store all reasons as list
                final_usage = usages if usages else None  # Store all usages as list

                logger.info(
                    f"Multiple inferences completed. Got {len(inference_answers)} results."
                )
            else:
                # Single inference case
                processed = self._process_single_result(result)
                final_result = processed["answer"]
                final_reason = processed["reason"]
                final_usage = processed["usage"]

        except Exception as e:
            final_result = "Error code " + str(e)
            final_reason = ""
            final_usage = None

        # Create ProcessResult object
        process_result = ProcessResult(
            question_id=question_id,
            question=qs,
            answer=final_result,
            reason=final_reason,
            usage=final_usage,
        )

        return process_result

    def cleanup(self):
        if hasattr(self, "model_server") and self.model_server is not None:
            try:
                self.model_server.stop()
                self.model_server = None
            except Exception as e:
                logger.error(f"Error shutting down model server: {e}")

    def run_one_task(self, task_name: str, meta_info: Dict[str, Any]):
        self.dataset = ServerDataset(
            task_name,
            task_type=meta_info["type"],
            task_manager=self.task_manager,
        )

        results = []
        num_workers = self.task_info.get("num_workers", 1)
        inter_results_dir = osp.join(meta_info["output_dir"], "items")
        os.makedirs(inter_results_dir, exist_ok=True)
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            future_to_item = {
                executor.submit(self.process_single_item, i, inter_results_dir): i
                for i in range(len(self.dataset))
            }

            for future in as_completed(future_to_item):
                result = future.result()
                results.append(result)
                if isinstance(result.answer, str) and result.answer.startswith(
                    "Error code"
                ):
                    continue
                else:
                    self.save_item(result, result.question_id, meta_info)

        self.save_result(results, meta_info)


if __name__ == "__main__":
    args = parse_args()
    model_adapter = ModelAdapter(
        server_ip=args.server_ip,
        server_port=args.server_port,
        timeout=args.timeout,
        model_type=args.model_type,
        extra_cfg=args.cfg,
        local_mode=args.local_mode,
        task_names=args.tasks,
        output_dir=args.output_dir,
        model_path=args.model,
        debug=args.debug,
        quiet=args.quiet,
    )
    model_adapter.run()
