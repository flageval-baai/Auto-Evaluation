import os
import requests
import json

def client_batches(eval_infos, mode, region, user_id):
    url = "http://120.92.17.239:5050/evaluation"
    #url = "http://172.31.125.164:5050/evaluation"
    headers = {
        "Content-Type": "application/json" 
    }
    data={"eval_infos": eval_infos, "domain":"NLP", "mode":mode, "region": region, "user_id": user_id}
    try:
        raw_body = json.dumps(data)
        response = requests.post(url,data= raw_body, headers=headers)
        response.raise_for_status()  # 如果响应状态不是200，将引发HTTPError异常

        response_data = response.json()
        print(response_data)
    except:
        import traceback
        print(traceback.format_exc())


def client_mmbatches(eval_infos, mode, region, user_id):
    url = "http://120.92.17.239:5050/evaluation"
    #url = "http://172.31.125.164:5050/evaluation"
    headers = {
        "Content-Type": "application/json"
    }
    data = {"eval_infos":eval_infos, "domain":"MM", "mode":mode, "region": region, "user_id": user_id}
    try:
        raw_body = json.dumps(data)
        response = requests.post(url,data= raw_body, headers=headers)
        print(response)
        response.raise_for_status()  # 如果响应状态不是200，将引发HTTPError异常

        response_data = response.json()
        print(response_data.keys())
        print(response_data)
    except:
        import traceback
        print(traceback.format_exc())


def get_batches(request_id):
    #url = "http://172.31.125.164:5050/evaldiffs"
    url = "http://120.92.17.239:5050/evaldiffs"
    headers = {
        "Content-Type": "application/json"
    }
    #"eval_url":"http://120.92.208.64:7609/v1/completions",
    #"api_key":"EMPTY"
    data={
        "request_id": request_id
    }

    try:
        raw_body = json.dumps(data)
        response = requests.get(url,data= raw_body, headers=headers)
        print(response)
        response.raise_for_status()  # 如果响应状态不是200，将引发HTTPError异常

        response_data = response.json()
        print(response_data.keys())
        print(response_data)
    except:
        import traceback
        print(traceback.format_exc())

def resume_batch(request_id):
    url = "http://120.92.17.239:5050/resume_evaluation"
    #url = "http://172.31.125.164:5050/resume_evaluation"
    headers = {
        "Content-Type": "application/json"
    }
    #"eval_url":"http://120.92.208.64:7609/v1/completions",
    #"api_key":"EMPTY"
    data={
        "request_id": request_id
    }

    try:
        raw_body = json.dumps(data)
        response = requests.post(url,data= raw_body, headers=headers)
        print(response)
        response.raise_for_status()  # 如果响应状态不是200，将引发HTTPError异常

        response_data = response.json()
        print(response_data.keys())
        print(response_data)
    except:
        import traceback
        print(traceback.format_exc())


def stop_batch(request_id):
    url = "http://120.92.17.239:5050/stop_evaluation"
    #url = "http://172.31.125.164:5050/stop_evaluation"
    headers = {
        "Content-Type": "application/json"
    }
    #"eval_url":"http://120.92.208.64:7609/v1/completions",
    #"api_key":"EMPTY"
    data={
        "request_id": request_id
    }

    try:
        raw_body = json.dumps(data)
        response = requests.post(url,data= raw_body, headers=headers)
        print(response)
        response.raise_for_status()  # 如果响应状态不是200，将引发HTTPError异常

        response_data = response.json()
        print(response_data.keys())
        print(response_data)
    except:
        import traceback
        print(traceback.format_exc())


def get_diffs(request_ids):
    url = "http://172.31.125.164:5050/evaluation_diffs"
    headers = {
        "Content-Type": "application/json"
    }
    #"eval_url":"http://120.92.208.64:7609/v1/completions",
    #"api_key":"EMPTY"
    data={
        "request_ids": request_ids
    }

    try:
        raw_body = json.dumps(data)
        response = requests.get(url,data= raw_body, headers=headers)
        print(response)
        response.raise_for_status()  # 如果响应状态不是200，将引发HTTPError异常

        response_data = response.json()
        print(response_data.keys())
        print(response_data)
    except:
        import traceback
        print(traceback.format_exc())


        evaluation_process
def evaluation_process(request_id, domain):
    url = "http://172.31.125.164:5050/evaluation_progress"
    headers = {
        "Content-Type": "application/json"
    }
    #"eval_url":"http://120.92.208.64:7609/v1/completions",
    #"api_key":"EMPTY"
    data={
        "request_id": request_id,
        "domain":domain
    }

    try:
        raw_body = json.dumps(data)
        response = requests.post(url,data= raw_body, headers=headers)
        print(response)
        response.raise_for_status()  # 如果响应状态不是200，将引发HTTPError异常

        response_data = response.json()
        print(response_data.keys())
        print(response_data)
    except:
        import traceback
        print(traceback.format_exc())
if __name__ == "__main__":
    #eval_infos = [{"eval_model": "llama4scout-nv-flagos-1", "model": "llama4scout-nv-flagos", "eval_url": "http://125.72.144.144:9031/v1/chat/completions", "tokenizer": "meta-llama/Llama-4-Scout-17B-16E-Instruct", "api_key": "EMPTY"}]
    #eval_infos = [{"eval_model": "glm4z1r32-nv-flagos-bs32-151830", "model": "glm4z1r32-nv-flagos", "eval_url": "http://125.72.144.144:9031/v1/chat/completions", "tokenizer": "THUDM/GLM-Z1-Rumination-32B-0414", "api_key": "EMPTY", "batch_size": 32}]
    #eval_infos= [{"eval_model":"MiniCPM-o-2_6-hg-02","model":"/MiniCPM_o_2_6","eval_url":"http://10.1.15.198:8000/v1/chat/completions","num_concurrent":1,"num_retry":10}]
    #eval_infos = [{"eval_model": "huawei_llama3", "model": "/workspace/hardware_ckpt/huawei/huawei_mcore_to_hf_llama3_ckpt", "eval_url": "http://10.1.15.233:8000/v1/completions", "tokenizer": "Qwen/Qwen2-7B-Instruct", "api_key": "EMPTY",  "num_concurrent": 6, "num_retry": 10, "max_gen_toks": -1, "gen_kwargs": ""}]
    #eval_infos = [{"eval_model": "tianshu_llama3", "model": "/workspace/hardware_ckpt/tianshu/tianshu_mcore_to_hf_llama3_ckpt", "eval_url": "http://10.1.15.141:8000/v1/completions", "tokenizer": "Qwen/Qwen2-7B-Instruct", "api_key": "EMPTY",  "num_concurrent": 6, "num_retry": 10, "max_gen_toks": -1, "gen_kwargs": ""}]
    #eval_infos = [{"eval_model": "tsingmicro_llama3_5", "model": "/workspace/hardware_ckpt/tsingmicro/tsingmocro_to_hf_llama3_ckpt", "eval_url": "http://10.1.15.124:8000/v1/completions", "tokenizer": "Qwen/Qwen2-7B-Instruct", "api_key": "EMPTY",  "num_concurrent": 6, "num_retry": 10, "max_gen_toks": -1, "gen_kwargs": ""}]
    #eval_infos = [{"eval_model": "klx_llama3_1", "model": "/workspace/hardware_ckpt/kunlunxin/kunlunxin_mcore_to_hf_llama3_ckpt", "eval_url": "http://10.1.15.218:8000/v1/completions", "tokenizer": "Qwen/Qwen2-7B-Instruct", "api_key": "EMPTY",  "num_concurrent": 6, "num_retry": 10, "max_gen_toks": -1, "gen_kwargs": ""}]
    #eval_infos = [{"eval_model": "muxi_llama3_1", "model": "/workspace/hardware_ckpt/muxi/muxi_mcore_to_hf_llama3_ckpt", "eval_url": "http://10.1.15.141:8000/v1/completions", "tokenizer": "Qwen/Qwen2-7B-Instruct", "api_key": "EMPTY",  "num_concurrent": 6, "num_retry": 10, "max_gen_toks": -1, "gen_kwargs": ""}]
    #eval_infos = [{"eval_model": "moer_llama3_1", "model": "/workspace/hardware_ckpt/mthreads/mthreads_mcore_to_hf_llama3_ckpt", "eval_url": "http://10.1.15.124:8000/v1/completions", "tokenizer": "Qwen/Qwen2-7B-Instruct", "api_key": "EMPTY",  "num_concurrent": 6, "num_retry": 10, "max_gen_toks": -1, "gen_kwargs": ""}]
    #eval_infos = [{"eval_model": "moer_qwen2_5_vl_8", "model": "/workspace/hardware_ckpt/mthreads/mthreads_mcore_to_hf_qwen2_5_vl_ckpt", "eval_url": "http://10.1.15.124:9011/v1/chat/completions", "tokenizer": "Qwen/Qwen2-7B-Instruct", "api_key": "EMPTY",  "num_concurrent": 6, "num_retry": 10, "max_gen_toks": -1, "gen_kwargs": ""}]
    #eval_infos = [{"eval_model": "cz_qwen2_5_vl_8", "model": "/workspace/hardware_ckpt/a800/qwen2_5_vl/", "eval_url": "http://10.1.15.124:9010/v1/chat/completions", "tokenizer": "Qwen/Qwen2-7B-Instruct", "api_key": "EMPTY",  "num_concurrent": 6, "num_retry": 10, "max_gen_toks": -1, "gen_kwargs": ""}]
    #eval_infos = [{"eval_url":"http://10.1.15.113:9010/v1/chat/completions","model":"Qwen3-235B-A22B-Instruct-2507-ascend-flagos","eval_model":"Qwen3-235B-A22B-Instruct-2507-ascend-flagos-concur32","tokenizer":"Qwen/Qwen3-235B-A22B-Instruct-2507","api_key":'EMPTY' ,"batch_size":1 ,"num_concurrent":32 ,"num_retry":10 ,"max_gen_toks":-1,"gen_kwargs":"temperature=0.7,top_p=0.8,top_k=20,min_p=0,max_gen_toks=16000"}]
    #eval_infos = [{"eval_model":"GLM-4.5-nvidia-flagos_0807","model":"GLM-4.5-nvidia-flagos","eval_url":"http://10.1.15.153:9010/v1/chat/completions","api_key":'EMPTY' ,"batch_size":1 ,"num_concurrent":32 ,"num_retry":1 ,"max_gen_toks":-1,"gen_kwargs":"temperature=0.6,top_p=1.0"}]
    #eval_infos =[{"eval_model": "Qwen3-235B-A22B-Instruct-2507-ascend-flagos-concur32_12000", "model": "Qwen3-235B-A22B-Instruct-2507-ascend-flagos", "eval_url": "http://10.1.15.113:9010/v1/chat/completions", "tokenizer": "Qwen/Qwen3-235B-A22B-Instruct-2507", "api_key": "EMPTY", "batch_size": 1, "num_concurrent": 32, "num_retry": 10, "max_gen_toks": -1, "gen_kwargs": "temperature=0.7,top_p=0.8,top_k=20,min_p=0,max_gen_toks=12000"}]
    #eval_infos =[{"eval_model": "step3-nvidia-flagos-concur64_2", "model": "step3-nvidia-flagos", "eval_url": "http://10.1.15.153:9010/v1/chat/completions", "tokenizer": "stepfun-ai/step3", "api_key": "EMPTY","batch_size": 1, "num_concurrent": 64, "num_retry": 10}]
    #eval_infos =[{"eval_model":"RoboBrain2.0-7B-iluvatar-flagos_0.9.1_2","model":"RoboBrain2.0-7B-iluvatar-flagos","eval_url":"http://10.1.15.195:9010/v1/chat/completions","num_concurrent":8, "thinking": False}]
    #eval_infos=[{"eval_model":"nlp_toks_0916_1","model":"Qwen2-7B-Instruct","eval_url":"http://172.24.171.193:8000/v1/chat/completions", "gen_kwargs":"max_gen_toks=16000"}]
    #eval_infos = [{"eval_model": "phi-4-hygon-flagos-concur16-1", "model": "phi-4-hygon-flagos", "eval_url": "http://10.1.15.92:9010/v1/chat/completions", "tokenizer": "microsoft/phi-4", "api_key": "EMPTY", "batch_size": 1, "num_concurrent": 16, "num_retry": 10, "max_gen_toks": -1, "gen_kwargs": "temperature=0.5,max_gen_toks=13000"}]
    #eval_infos = [{"eval_model": "MiniCPM-V-4-metax-origin-concur64_3", "model": "MiniCPM-V-4-metax-origin", "eval_url": "http://10.1.15.67:9010/v1/chat/completions", "tokenizer": "openbmb/MiniCPM-V-4", "api_key": "EMPTY", "batch_size": 1, "num_concurrent": 64, "num_retry": 10, "max_gen_toks": -1, "gen_kwargs": "max_gen_toks=16000"}]
    #eval_infos =[{"eval_model": "Qwen3-Next-80B-A3B-Instruct-nvidia-flagos-concur256", "model": "Qwen3-Next-80B-A3B-Instruct-nvidia-flagos", "eval_url": "http://10.1.15.153:9010/v1/chat/completions", "tokenizer": "Qwen/Qwen3-Next-80B-A3B-Instruct", "api_key": "EMPTY", "batch_size": 1, "num_concurrent": 256, "num_retry": 10, "max_gen_toks": -1, "gen_kwargs": "temperature=0.7,top_p=0.8,top_k=20,min_p=0"}]
    #eval_infos = [{"eval_model": "RoboBrain2.0-7B-metax-flagos-concur64_5", "model": "RoboBrain2.0-7B-metax-flagos", "eval_url": "http://10.1.15.67:9010/v1/chat/completions", "tokenizer": "BAAI/RoboBrain2.0-7B", "api_key": "EMPTY", "batch_size": 1, "num_concurrent": 64, "num_retry": 10, "max_gen_toks": -1, "gen_kwargs": "", "retry_time":3600}]
    #eval_infos = [{"eval_model":"pingtouge_llama3_1", "model": "/workspace/hardware_ckpt/pingtouge/pingtouge_mcore_to_hf_llama3_ckpt", "eval_url": "http://10.1.15.124:8000/v1/completions", "tokenizer": "", "api_key": "EMPTY", "batch_size": 1, "num_concurrent": 4, "num_retry": 1,"chip":"PPU-ZW810E"}]
    #eval_infos = [{"eval_model": "online_api_1106_llm", "model": "4.0Ultra", "eval_url": "https://spark-api-open.xf-yun.com/v1/chat/completions", "tokenizer": "", "api_key": "7090834e3d9bb24a6ee543651d8fe6b3:NTI2ZmQ1MjU1OTUzY2Y3MTE0MWVmMGEx", "batch_size": 1, "num_concurrent": 20, "num_retry": 10, "max_gen_toks": -1, "gen_kwargs": "", "chip":"Nvidia-H100", "base_model_name":"4.0Ultra"}]
    #eval_infos = [{"eval_model": "online_api_1106_EV_0", "model": "RoboBrain2.0-7B", "eval_url": "http://172.24.53.132:8000/v1/chat/completions", "tokenizer": "", "api_key": "EMPTY", "batch_size": 1, "num_concurrent": 1, "num_retry": 10, "max_gen_toks": -1, "gen_kwargs": "", "chip":"Nvidia-H100", "base_model_name":"RoboBrain2.0-7B"}]
    #eval_infos =[{"eval_model":"qwen2-7b-flagos-1125_0","model":"/workspace/CODE/models/Qwen2-7B","eval_url":"http://10.6.208.39:8000/v1/chat/completions","tokenizer":"Qwen/Qwen2-7B","api_key":"EMPTY", "batch_size":1,"num_concurrent":1, "num_retry":1, "gen_kwargs":"","chip":"Nvidia-H100", "base_model_name":"Qwen2-7B"}]
    #eval_infos= [{"eval_model": "Kimi-K2-Thinking-nvidia-origin","model": "Kimi-K2-Thinking-nvidia-origin","num_concurrent": 16,"chip": "H20-SXM","eval_url": "http://172.21.16.14:8000/v1/chat/completions","tokenizer": "","base_model_name": "Kimi-K2-Thinkingg","gen_kwargs": "","api_key": "EMPTY"}]
    #eval_infos= [{"eval_model": "Kimi-K2-Thinking-nvidia-flagos","model": "Kimi-K2-Thinking-nvidia-flagos","num_concurrent": 16,"chip": "H20-SXM","eval_url": "http://172.21.16.6:8000/v1/chat/completions","tokenizer": "","base_model_name": "Kimi-K2-Thinkingg","gen_kwargs": "","api_key": "EMPTY"}]
    #eval_infos=[{"eval_model": "Qwen3-Next-80B-A3B-Instruct_fl", "model": "/share/project/ldwang/WorkSpace/models/Qwen3-Next-80B-A3B-Instruct", "eval_url": "http://172.24.178.148:8887/v1/chat/completions", "tokenizer": "Qwen/Qwen3-Next-80B-A3B-Instruct", "api_key": "EMPTY", "batch_size": 1, "num_concurrent": 1, "num_retry": 10, "gen_kwargs": "", "chip": "Nvidia-H100", "base_model_name": "Qwen3-Next-80B-A3B-Instruct"}]
    #eval_infos=[{"eval_model": "Qwen3-Next-80B-A3B-Instruct_origin", "model": "/share/project/ldwang/WorkSpace/models/Qwen3-Next-80B-A3B-Instruct", "eval_url": "http://172.24.178.148:8888/v1/chat/completions", "tokenizer": "Qwen3-Next-80B-A3B-Instruct", "api_key": "EMPTY", "batch_size": 1, "num_concurrent": 4, "num_retry": 10, "gen_kwargs": "", "chip": "Nvidia-H100", "base_model_name": "Qwen3-Next-80B-A3B-Instruct"}]
    eval_infos=[{"eval_model": "Qwen3-Next-80B-A3B-Instruct_8885", "model": "/share/project/ldwang/WorkSpace/models/Qwen3-Next-80B-A3B-Instruct", "eval_url": "http://172.26.226.221:8885/v1/chat/completions", "tokenizer": "Qwen/Qwen3-Next-80B-A3B-Instruct", "api_key": "EMPTY", "batch_size": 1, "num_concurrent": 1, "num_retry": 10, "gen_kwargs": "", "chip": "Nvidia-H100", "base_model_name": "Qwen3-Next-80B-A3B-Instruct"}]
    #eval_infos=[{"eval_model": "qwen3-8b-cambricon-flagos-1229_1", "model": "/root/Qwen3-8B", "eval_url": "http://10.1.15.238:8020/v1/chat/completions", "tokenizer": "Qwen/Qwen3-8B", "api_key": "EMPTY", "batch_size": 1, "num_concurrent": 8, "num_retry": 10, "max_gen_toks": -1, "gen_kwargs": "", "status": "F", "retry": 10,  "chip": "Nvidia-H100", "base_model_name": "Qwen3-8B"}]
    #mode="EmbodiedVerse"
    #mode="XLC"
    #mode = "FlagRelease"
    #mode = 'XLC_train'
    #mode = 'XLC'
    mode='Qnext'
    region='sz'
    #region='bj'
    user_id=0
    stop_batch("78736864-42ec-48d7-a3bb-d65b2c0465fe")
    #client_batches(eval_infos, mode, region, user_id)
    #get_batches("99c08c97-0028-4968-92ab-e50844b9a3ec")
    #evaluation_process('ebb4115d-d079-4418-96f2-de6ba8c1195a',"NLP")
    #stop_batch("49cc29d7-a545-4be4-8fe5-e1f27c872851")
    #stop_batch("6da75b70-8612-499a-bb0e-1c1bf25d88dd")
    #stop_batch("1aaa2acb-0f64-4d12-aa6e-ab048a6427a7")
    #stop_batch("")
    #stop_batch("")
    #get_batches("c0f726fa-8d2f-4763-b877-230ab016d065")
    #stop_batch("c869e2de-6c64-4615-b127-020fe9ee951f")
    #get_batches("c869e2de-6c64-4615-b127-020fe9ee951f")
    #resume_batch('8a5112ac-2329-41de-8468-e09fd9f3bf34')
    #eval_infos =[{"eval_model": "", "model": "", "eval_url": "http://10.1.15.119:9010/v1/chat/completions", "api_key": "EMPTY", "num_concurrent":4}]
    #client_mmbatches(eval_infos, mode, region, user_id)
    #get_batches("5de8be16-9bb0-49ec-8ec3-ac558f9feac6")
    #evaluation_process('',"MM")
    #stop_batch("65a7e995-06c6-4314-947a-5ab4136a6be4")
    #resume_batch('81810a49-9b63-4c5c-a9ae-eb0cc103a07e')
    #get_diffs(["f7597623-b58a-4fa3-9a6f-09a342d140b6","f80c4731-8c10-4828-a6a9-3c605c2a70da"])
    #evaluation_process('937f8728-de43-476e-87be-35b7d2780f57',"NLP")
