from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import httpx
import asyncio
#import redis
from fastapi.concurrency import run_in_threadpool
from typing import Optional
from submit import *
from utils import *

MAXRETRY=10
app = FastAPI()
#redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)
# 存储请求结果的临时缓存（实际生产环境建议用数据库）
requests_cache = {}
#with open("flageval_evaldiffs_infos.json","r") as f:
#    taskqueue=json.load(f)
#print("server init taskqueue", taskqueue)
# 请求模型定义
class CompareInfo(BaseModel):
    eval_url: str
    model: str
    eval_model: str
    base_model_name: str
    tokenizer: Optional[str] = ''
    api_key: Optional[str] = 'EMPTY'
    batch_size: Optional[int] = 1
    num_concurrent: Optional[int] =1
    num_retry: Optional[int] =10
    max_gen_toks: Optional[int] = -1
    gen_kwargs: Optional[str] = ''
    thinking: Optional[bool] = False
    retry_time: Optional[int] = -1
    chip: Optional[str] = 'Nvidia-H100'

class CompareRequest(BaseModel):
    #eval_urls: list[str]  # 需要请求的URL列表
    #model: str #模型名称
    #eval_model:str
    #tokenizer: str #模型token
    eval_infos: list[CompareInfo]
    domain: str
    mode: Optional[str] = 'FlagRelease'
    region: Optional[str] = 'bj'
    special_event: Optional[str] = 'Chips'
    user_id: Optional[int] =0

class DiffRequest(BaseModel):
    request_id: str  # 用于查询缓存的UUID

class DiffsRequest(BaseModel):
    request_ids : list[str]

class ProgressRequest(BaseModel):
    request_id: str  # 用于查询缓存的UUID
    domain: str
# 异步请求单个URL
#async
def fetch_url(request_id,taskqueue, taskinfo, mode, region, special_event, user_id) -> dict:
    #global taskqueue
    try:
        print("taskinfo",taskinfo)
        response = submit_evaluation(taskinfo.eval_model, taskinfo.model, taskinfo.eval_url, taskinfo.tokenizer, taskinfo.api_key, taskinfo.batch_size, taskinfo.num_concurrent, taskinfo.num_retry, taskinfo.max_gen_toks, taskinfo.gen_kwargs, mode, region, special_event, taskinfo.chip, taskinfo.base_model_name, user_id)
        if response["err_code"] == 0:
            taskqueue[taskinfo.eval_model]={"request_id":request_id,"eval_model": taskinfo.eval_model, "model":taskinfo.model,"url":taskinfo.eval_url,"tokenizer":taskinfo.tokenizer,"api_key": taskinfo.api_key, "batch_id": response["batch_id"],"batch_size": taskinfo.batch_size,"num_concurrent":taskinfo.num_concurrent, "num_retry":taskinfo.num_retry, "max_gen_toks":taskinfo.max_gen_toks,"gen_kwargs": taskinfo.gen_kwargs, "status":"R", "retry": 1, "Domain":"NLP", "mode": mode, "region": region, "special_event":special_event, "chip":taskinfo.chip, "base_model_name": taskinfo.base_model_name, "user_id": user_id}
        print(response)
        return response
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return {"err_code":2, "err_msg": str(e)}

def mmfetch_url(request_id, taskqueue, taskinfo, mode, region, special_event, user_id) -> dict:
    try:
        print(taskinfo)
        if "max_gen_toks" in taskinfo.gen_kwargs:
            params = taskinfo.gen_kwargs.split(",")
            for param in params:
                key,value = param.split("=")[0], param.split("=")[1]
                if key == "max_gen_toks":
                    taskinfo.max_gen_toks = int(value)
        print(taskinfo)
        response = submit_mm_evaluation(taskinfo.eval_model, taskinfo.eval_url, taskinfo.api_key, taskinfo.model, taskinfo.batch_size, taskinfo.num_concurrent, taskinfo.num_retry, taskinfo.max_gen_toks, taskinfo.thinking, taskinfo.retry_time, mode, region, special_event, taskinfo.chip, taskinfo.base_model_name, user_id)
        if response["err_code"] == 0:
            taskqueue[taskinfo.eval_model]={"request_id":request_id,"eval_model": taskinfo.eval_model, "model":taskinfo.model,"url":taskinfo.eval_url,"tokenizer":taskinfo.tokenizer,"api_key": taskinfo.api_key, "batch_id": response["batch_id"],"batch_size": taskinfo.batch_size,"num_concurrent":taskinfo.num_concurrent, "num_retry":taskinfo.num_retry,"max_gen_toks":taskinfo.max_gen_toks, "gen_kwargs": taskinfo.gen_kwargs,"status":"R", "retry": 1, "Domain":"MM", "mode":mode,"region": region, "special_event":special_event, "chip":taskinfo.chip, "base_model_name": taskinfo.base_model_name, "user_id": user_id}
        return response
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return {"err_code":2, "err_msg": str(e)}

# 接口1：并发请求多个URL并缓存结果
@app.post("/evaluation")
async def compare_urls(request: CompareRequest):
    try:
        print("get a new request")
        # 生成唯一UUID
        request_id = str(uuid.uuid4())
        
        # 并发请求所有URL
        eval_infos = request.eval_infos
        Domain = request.domain
        mode = request.mode
        region = request.region
        special_event = request.special_event
        user_id = request.user_id
        with open("logs/flageval_evaldiffs_infos.json","r") as f:
            taskqueue=json.load(f)
        #print("befor new request taskqueue", taskqueue)
        if Domain == "NLP":
            #tasks = [fetch_url(request_id, taskqueue, taskinfo) for taskinfo in request.eval_infos]
            tasks = fetch_url(request_id, taskqueue, request.eval_infos[0], mode, region, special_event, user_id)
        else:
            #tasks = [mmfetch_url(request_id, taskqueue, taskinfo) for taskinfo in request.eval_infos]
            tasks = mmfetch_url(request_id, taskqueue,request.eval_infos[0], mode, region, special_event, user_id)
        print("tasks", tasks)
        with open("logs/flageval_evaldiffs_infos.json", "w") as f:
            f.write(json.dumps(taskqueue))
        # 存储结果到缓存
        eval_models=[taskinfo.eval_model for taskinfo in request.eval_infos]
        if tasks["err_code"] == 0:
            insertwithid(request_id, eval_models,eval_models[0], tasks["batch_id"])
            #requests_cache[request_id] = eval_models
            return {"err_code": 0, "err_msg":"eval task begin", "request_id": request_id, "eval_tasks": tasks}
        else:
            return tasks
    except:
        import traceback
        print(traceback.format_exc())
        return {"err_code":1, "err_msg":"except failed"}
# 接口2：对比差异（以第一个结果为基准）
@app.get("/evaldiffs")
async def get_diffs(request: DiffRequest):
    # 从mysql中获取结果
    eval_results = {}
    eval_model,_,details, status = query(request.request_id)
    print("eval_model", "details", "status")
    print(eval_model, details, status)
    #if not details and status=='S':
    #    with open("flageval_evaldiffs_infos.json","r") as f:
    #        taskqueue=json.load(f)
    #    model_result = taskqueue[eval_model]
    #    status = model_result["status"]
    #    details = model_result["details"]
    #print("query from mysql eval_models:", request.request_id, eval_models)
    #if not eval_models:
    #    return {"err_code":1, "err_msg":"request_id not found"}
    #with open("flageval_evaldiffs_infos.json","r") as f:
    #    taskqueue=json.load(f)
    #print("right now taskqueue", taskqueue, type(taskqueue), taskqueue.keys())
    #eval_results = {}
    #for i, model in enumerate(eval_models):
    #    print("each model", model)
    #    model_result = taskqueue[model]
    #    #eval_results[model] = {"status":taskqueue[model]["status"]}
    #    status = model_result["status"]
    #    details, diff, release = {},{}, False
    #    if status == "S":
    #        details = model_result["details"]
    #        if i == 0:
    #            baseline = details
    #        else:
    #            #[{'dataset': 'lm_eval-gsm8k', 'status': 'S', 'accuracy': None, 'rawDetails': {}}, {'dataset': 'lm_eval-mmlu', 'status': 'S', 'accuracy': 0.7140008545791198, 'rawDetails': {}}]}
    #            #release = False
    #            for base, detail in zip(baseline, details):
    #                diff = base["accuracy"] - detail["accuracy"]
    #                detail["diff"] = diff
    #                if abs(diff) >= 0.5:
    #                    release = False
    #    eval_results[model]={"status":status, "details": details, "release": release}
    # [{'dataset': 'AIME', 'status': 'S', 'accuracy': 0.7667, 'rawDetails': {}}, {'dataset': 'GPQA', 'status': 'S', 'accuracy': 0.5, 'rawDetails': {}}, {'dataset': 'MMLU', 'status': 'S', 'accuracy': 0.7689, 'rawDetails': {}}, {'dataset': 'MUSR', 'status': 'S', 'accuracy': 0.6892, 'rawDetails': {}}, {'dataset': 'LiveBench', 'status': 'S', 'accuracy': 0.4869, 'rawDetails': {}}]
    dataset_map = {
        "AIME":"AIME_0fewshot_@avg1",
        "GPQA":"GPQA_0fewshot_@avg1",
        "MUSR":"MUSR_0fewshot_@avg",
        "LiveBench":"LiveBench-0fewshot_@avg1",
        "MMLU":"MMLU_5fewshot_@avg1",
        "math_500":"math_500_0fewshot_@avg1"
    }
    for detail in details:
        for k in detail.keys():
            if k == "dataset" and detail[k] in dataset_map.keys():
                detail[k] = dataset_map[detail[k]]
    eval_results[eval_model]={"status":status, "details": details}
    return {"err_code": 0, "err_msg":"Get Evaluations Details Sucess!", "eval_results": eval_results}
        

@app.get("/evaluation_diffs")
async def evaluation_diffs(request: DiffsRequest):
    # 从mysql中获取结果
    eval_diffs={}
    eval_results=[]
    for i, request_id in enumerate(request.request_ids):
        eval_model,_,details, status = query(request_id)
        if status == "S":
            eval_results.append(details)
            if i == 0:
                baseline = details
    if len(eval_results) == len(request.request_ids):
        for i, details in enumerate(eval_results):
            if i == 0:
                baseline = details
            else:
                release = True
                newdetails=[]
                for base, detail in zip(baseline, details):
                    if base["dataset"] == detail["dataset"]:
                        diff = base["accuracy"] - detail["accuracy"]
                        newdetails.append({"dataset":detail["dataset"],"base_acc":base["accuracy"], "accuracy":detail["accuracy"],"diff":diff})
                        if abs(diff) >= 0.5:
                            release = False
                eval_diffs[request_id]={"details": newdetails, "release":release}
        return {"err_code": 0, "err_msg":"GET Evaluations Diffs Done!", "eval_diffs": eval_diffs}        
    else:
        return {"err_code": 1, "err_msg":"Not all Evaluations Sucess Done!"}        

@app.post("/stop_evaluation")
async def stopbatch(request: DiffRequest):
    eval_model,batch_id,details,_ = query(request.request_id)
    print(eval_model, batch_id, request.request_id)
    response = stop_batch(batch_id) 
    with open("logs/flageval_evaldiffs_infos.json","r") as f:
        taskqueue=json.load(f)
    taskqueue[eval_model]["status"]="C"
    taskqueue[eval_model]["retry"]=MAXRETRY
    with open("logs/flageval_evaldiffs_infos.json", "w") as fw:
        fw.write(json.dumps(taskqueue))
    updatedetails(details, "C", batch_id)
    return response

@app.post("/resume_evaluation")
async def resume_evaluation(request: DiffRequest):
    eval_model,batch_id,details,_ = query(request.request_id)
    with open("logs/flageval_evaldiffs_infos.json","r") as f:
        taskqueue=json.load(f)
    taskinfo = taskqueue[eval_model]
    resp = batchresumption(taskinfo["batch_id"],taskinfo["eval_model"], taskinfo["model"], taskinfo["url"], taskinfo["tokenizer"], taskinfo["api_key"], taskinfo["batch_size"], taskinfo["num_concurrent"], taskinfo["num_retry"],taskinfo["max_gen_toks"], taskinfo["gen_kwargs"], taskinfo["mode"],taskinfo["region"],taskinfo["user_id"])
    taskqueue[eval_model]["status"]='R'
    taskqueue[eval_model]['retry']=1
    with open("logs/flageval_evaldiffs_infos.json", "w") as fw:
        fw.write(json.dumps(taskqueue))
    updatedetails(details, "R", batch_id)
    return resp


@app.post("/evaluation_progress")
async def process_evaluation(request: ProgressRequest):
    eval_model,batch_id,details,status = query(request.request_id)
    with open("logs/flageval_evaldiffs_infos.json","r") as f:
        taskqueue=json.load(f)
        taskinfo = taskqueue[eval_model]
    #loginfos = batchlog(taskinfo["batch_id"],taskinfo["eval_model"], taskinfo["model"], taskinfo["url"], taskinfo["tokenizer"], taskinfo["api_key"], taskinfo["batch_size"], taskinfo["num_concurrent"], taskinfo["num_retry"],taskinfo["max_gen_toks"], taskinfo["gen_kwargs"], taskinfo.get("mode","FlagRelease"))
    #print("loginfos", loginfos)
    #print("details", details)
    #if loginfos["totalDatasets"] == 0:
    #    finished,finished_datasets,running_dataset,running_progress = False,0,"",""
    #    if status == "S":
    #        finished=True
    #        finished_datasets = len(details)
    #    else:
    #        finished_datasets=0
    #        for detail in details:
    #            if detail["status"] == "S":
    #                finished_datasets += 1
    #            elif detail["status"] == "R":
    #                running_dataset = detail["dataset"]
    #                break
 
    #    loginfos["totalDatasets"] = len(details)
    #    loginfos["finishedDataset"] = finished_datasets
    #    loginfos["runningDataset"] = running_dataset
    #    
    #return loginfos
    finished,finished_datasets,running_dataset,running_progress = False,0,"",""
    if status == "S":
        finished=True
        finished_datasets = len(details)
    else:
        finished_datasets=0
        for detail in details:
            if detail["status"] == "S":
                finished_datasets += 1
            elif detail["status"] == "R":
                running_dataset = detail["dataset"]
                with open("logs/flageval_evaldiffs_infos.json","r") as f:
                    taskqueue=json.load(f)
                    taskinfo = taskqueue[eval_model]
                if request.domain == "NLP":
                    loginfos = batchlog(taskinfo["batch_id"],taskinfo["eval_model"], taskinfo["model"], taskinfo["url"], taskinfo["tokenizer"], taskinfo["api_key"], taskinfo["batch_size"], taskinfo["num_concurrent"], taskinfo["num_retry"],taskinfo["max_gen_toks"], taskinfo["gen_kwargs"], taskinfo.get("mode","FlagRelease"),taskinfo.get("user_id",0))
                else:
                    loginfos = mmbatchlog(taskinfo["batch_id"],taskinfo["eval_model"], taskinfo["model"], taskinfo["url"], taskinfo["tokenizer"], taskinfo["api_key"], taskinfo["batch_size"], taskinfo["num_concurrent"], taskinfo["num_retry"],taskinfo["max_gen_toks"], taskinfo["gen_kwargs"], taskinfo.get("mode","FlagRelease"),taskinfo.get("user_id",0))
                print("loginfos", loginfos)
                if loginfos["err_code"] == 0:
                    running_progress = loginfos["runningProgress"]
                break
    resp={"finished":finished,"status": status,"datasets_progress":str(finished_datasets)+"/"+str(len(details)), "running_dataset":running_dataset, "running_progress":running_progress}
    return resp

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5050)

