import requests
import json
import time
import hmac, hashlib



# 生产环境
base_url = 'https://flageval.baai.ac.cn/api/hf'
secret = b'M2L84t36MdzwS1Lb'
gpu_id = 'f016ff98-6ec8-4b1e-aed2-9a93753119b2'
# 测试环境
#base_url = 'http://120.92.17.239:8080/api/hf'
#secret = b'Dn29TMCxzvKBGMS8'
#gpu_id='1ac04795-a552-4f79-8c13-1b43d0f15b17'

redis_map={}

dataset_size={
	"lm_eval-mmlu":56168,
    "lm_eval-gsm8k":1319,
    "lm_eval-TheoremQA":800,
    "lm_eval-gpqa_generative_cot":1192,
    "lm_eval-mmlu_pro":12032,
    "lm_eval-musr_generative":756,
    "lm_eval-leaderboard_bbh":31710,
    "lm_eval-livebench_new":910,
    "lm_eval-aime":30,
    "lm_eval-math_hard":1324,
    "lm_eval-math_500":500
}
DataSets=[
    "lm_eval-musr_generative",
    "lm_eval-mmlu_pro",
    "lm_eval-gpqa_generative_cot",
    "lm_eval-aime",
    "lm_eval-livebench_new",
    #"lm_eval-math_500",
    ]
    
XLCInfer_DataSets=[
    #"lm_eval-gpqa_generative_cot",
    #"lm_eval-gpqa_diamond_generative_cot",
    "lm_eval-aime",
    "lm_eval-math_500",
    ]

XLCTrain_DataSets=[
    'lm_eval-truthfulqa',
    'lm_eval-winogrande',
    'lm_eval-commonsense_qa',
    'lm_eval-piqa',
    'lm_eval-openbookqa',
    'lm_eval-boolq',
    'lm_eval-arc_easy',
    'lm_eval-arc_challenge',
    'lm_eval-minerva_math_algebra',
    'lm_eval-mmlu',
    'lm_eval-gsm8k',
    'lm_eval-ceval-valid',
    'lm_eval-cmmlu'
    ]

XLC_MMDataSets=[
    "MMMU",
    "CMMMU",
    "MMMU_Pro_standard",
    "MMMU_Pro_vision",
    "OCRBench",
    "MathVision",
    "CII-Bench",
    "Blink",
    "MM-Vet v2",
]

Embodied_DataSets=[
    "ERQA",
    "ERQAPlus",
    "Where2Place",
    "Blink_ev",
    "CVBench",
    "EmbspatialBench",
    "SAT",
    "VSI-Bench",
    "RoboSpatial-Home",
    "All-Angles Bench",
    "EgoPlan-Bench2",
    "EmbodiedVerse-Open-Sampled",
 ]

Qwen_DataSets=[
    'lm_eval-mmlu',
    'lm_eval-cmmlu',
]

Robo_MMDataSets=[
    #"MMMU",
    #"CMMMU",
    #"MathVision",
    "MMBench_en",
]

#`DataSets=[
#    "lm_eval-mmlu",
#    "lm_eval-gsm8k",
#    ]
    #"lm_eval-aime",
    #"lm_eval-TheoremQA",
    #"lm_eval-aime"
    #"lm_eval-musr_generative",
    #"lm_eval-TheoremQA",
    #"lm_eval-mmlu_pro",
    #"lm_eval-gpqa_generative_cot",
    #"lm_eval-aime"
    #"lm_eval-aime"
    #"lm_eval-aime"
    #"lm_eval-musr_generative",
    #"lm_eval-TheoremQA",
    #"lm_eval-mmlu_pro",
    #"lm_eval-gpqa_generative_cot",
    #"lm_eval-math_hard"
    #"lm_eval-livebench_new",
    #"lm_eval-TheoremQA",
    #"lm_eval-gpqa_generative_cot",
    #"lm_eval-TheoremQA",
    #"lm_eval-gpqa_generative_cot",
    #"lm_eval-mmlu_pro",
    #"lm_eval-musr_generative",
    #"lm_eval-livebench_new"
	#"lm_eval-mmlu",
    #"lm_eval-cmmlu",
    #"lm_eval-gsm8k",
    #"lm_eval-leaderboard_bbh",
    #"lm_eval-s8"

def generate_signature(secret, url, body):
    timestamp = str(int(time.time()))
    to_sign = f'{timestamp}{url}{body}'
    h = hmac.new(secret, to_sign.encode('utf-8'), digestmod=hashlib.sha256)
    sign = h.hexdigest()
    return sign, timestamp

def get_datasetsize():
    count = 0
    for data in DataSets:
        count += dataset_size[data]
    return count

def submit_evaluation(model_id, online_model_name, online_url, tokenizer,online_api_key="EMPTY", batch_size=1, num_concurrent=1, num_retry=1, max_gen_toks=-1, gen_kwargs="",mode="FlagRelease", region="bj", special_event="Chips", chip="Nvidia-H100", base_model_name="", user_id=0):
    url = f'{base_url}/batches'
    datasets, model_type = [],"Chat"
    if mode == "XLC_infer":
        datasets = XLCInfer_DataSets
    elif mode == "XLC_train":
        datasets = XLCTrain_DataSets
        model_type =""
    elif mode == "Qnext":
        datasets = Qwen_DataSets
        model_type =""
    else:
        datasets = DataSets

    data = {
 		"user_id": user_id,
        "model_type":model_type,
        "tokenizer":{"tokenizer_name":tokenizer},
        "gpus_queue_id":"uuid",
		"sence":"EA",
		"model_id": model_id if model_id else online_model_name,
		"online_model_name": online_model_name,
		"base_model_name": base_model_name,
		"online_url": online_url,
		"online_api_key": online_api_key,
		"dataset":datasets,
        "batch_size": batch_size,
        "num_concurrent": num_concurrent,
        "num_retry":num_retry,
        "max_gen_toks": max_gen_toks,
        "gen_kwargs":gen_kwargs,
        "joint_region":region,
        "special_event":special_event,
        "special_event_meta":{"chip":chip}
	}
    print(data, type(data))
    raw_body = json.dumps(data)
    sign, timestamp = generate_signature(secret, url, raw_body)

    headers = {
        'Content-Type': 'application/json',
        'X-Flageval-Sign': sign,
        'X-Flageval-Timestamp': timestamp,
    }

    response = requests.post(url, data=raw_body, headers=headers)
    if response.status_code == 201:
        response_data = response.json()
        if "detail" in response_data and response_data["detail"] == "A job is still running":
            return {"err_code": 1, "err_msg":"A job is still running"}
        print(response_data)
        evaluation_info = {
            'err_code': 0,
            'err_msg': 'New evaluation is created',
            'eval_id': response_data.get('evaluationId'),
            'batch_id': response_data.get('id'),
            'datasize': get_datasetsize()
        }
    else:
        evaluation_info = {
            'err_code': 1,
            'err_msg': 'flageval server failed with err_code'+str(response.status_code),
            'eval_id': -1,
            'batch_id': -1,
            'datasize': -1
        }
    #redis_map[model_id]=response_data.get('id')
    #print(redis_map)
    return evaluation_info

#def get_evaluation(eval_id):
def poll_evaluation_progress(batch_id):
    url = f'{base_url}/batches/{int(batch_id)}'
    sign, timestamp = generate_signature(secret, url, '')

    headers = {
        'X-Flageval-Sign': sign,
        'X-Flageval-Timestamp': timestamp,
    }

    #data = {"user_id": 66}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 如果响应状态不是200，将引发HTTPError异常

        response_data = response.json()

        evaluation_progress = {
            'evaluationId': response_data.get('evaluationId'),
            'eval_id': response_data.get('id'),
            'status': response_data.get('status'),
            'details': response_data.get('details', [])
        }
        return evaluation_progress

    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except ValueError:
        print(f"解析JSON时出错:{response}")
    except Exception as e:
        print(f"未知错误: {e}")

    return {'status': '未执行成功'}    

def submit_mm_evaluation(model_id, online_url, online_api_key, online_model_name, batch_size=1, num_concurrent=1, num_retry=1, max_gen_toks=-1,thinking=False, retry_time=-1, mode='FlagRelease', region='bj', special_event="Chips", chip="Nvidia-H100", base_model_name="", user_id=0):
    url = f'{base_url}/mm/batches'
    mmdataset,runsh,adapter = [],"",""
    if mode == "EmbodiedVerse":
        mmdataset = Embodied_DataSets
    elif mode == "XLC" or mode == "FlagRelease":
        mmdataset = XLC_MMDataSets
    elif mode == "RoboTrain":
        mmdataset = Robo_MMDataSets
    else:
        mmdataset = []
    print(mode, mmdataset)
       
    data = {
            "user_id": user_id,
	        "require_gpus":0,
            "priority":"high",
	        "gpus_queue_id":"uuid",
            "hfUserId": None,
            'modelId': model_id,
            "online_api_key":online_api_key,
            "online_url":online_url,
            "online_model_name":online_model_name,
            "base_model_name":base_model_name,
            "batch_size": batch_size,
            "num_concurrent": num_concurrent,
            "num_retry":num_retry,
            #"max_gen_toks": max_gen_toks,
            "mmdataset": mmdataset,
            "joint_region":region,
            "special_event":special_event,
            "special_event_meta":{"chip":chip}
	}
    print(data, type(data))
    #if "RoboBrain" in online_model_name:
    #    runsh = open("mm/run.sh","r").read()
    #    if "RoboBrain2.0" in online_model_name:
    #        if not thinking:
    #            adapter = open("mm/2.0_nothiking_adapter.py","r").read()
    #        else:
    #            adapter = open("mm/2.0_thiking_adapter.py","r").read()
    #    elif "RoboBrain1.0" in online_model_name:
    #        if not thinking:
    #            adapter = open("mm/1.0_nothiking_adapter.py","r").read()
    #        else:
    #            adapter = open("mm/1.0_thiking_adapter.py","r").read()

    #  
    #    data = {
	#            "require_gpus":1,
    #            "priority":"high",
	#            "gpus_queue_id":gpu_id,
    #            "hfUserId": None,
    #            'modelId': model_id,
    #            "offline_api_key":online_api_key,
    #            "offline_url":online_url,
    #            "offline_model_name":online_model_name,
    #            "batch_size": num_concurrent, #batch_size,
    #            "num_concurrent": num_concurrent,
    #            "num_retry":num_retry,
    #            "max_gen_toks": max_gen_toks,
    #            "mmdataset": mmdataset,
    #            "runsh": runsh,
    #            "adapter": adapter,
    #            "joint_region":region
	#    }
        
    if max_gen_toks >0:
        data["max_tokens"] = max_gen_toks
    if retry_time > 0:
        data["retry_time"] = retry_time
    else:
        data["retry_time"] =3600
    print("submit mm evaluation", data)
    raw_body = json.dumps(data)
    sign, timestamp = generate_signature(secret, url, raw_body)

    headers = {
        'Content-Type': 'application/json',
        'X-Flageval-Sign': sign,
        'X-Flageval-Timestamp': timestamp,
    }

    response = requests.post(url, data=raw_body, headers=headers)
    print("submit_evaluation response",response.text)
    response_data = response.json()
    
    if "detail" in response_data and response_data["detail"] == "A job is still running":
        return {"err_code": 1, "err_msg":"A job is still running"}
    print(response_data)
    evaluation_info = {
        'err_code': 0,
        'err_msg': 'New evaluation is created',
        'eval_id': response_data.get('evaluationId'),
        'batch_id': response_data.get('id'),
        'datasize': 22301
    }

    #evaluation_info = {
    #    'evaluationId': response_data.get('evaluationId'),
    #    'eval_id': response_data.get('id')
    #}
    return evaluation_info

def poll_mm_evaluation_progress(batch_id):
    try:
        #print("= = b0", base_url, batch_id)
        url = f'{base_url}/mm/batches/{int(batch_id)}'
        sign, timestamp = generate_signature(secret, url, '')

        headers = {
            'X-Flageval-Sign': sign,
            'X-Flageval-Timestamp': timestamp,
        }

        response = requests.get(url, headers=headers)
        #print("= = e0", url, response)
        response.raise_for_status()  # 如果响应状态不是200，将引发HTTPError异常

        response_data = response.json()
        #print("= = e1", url, response)

        evaluation_progress = {
            'evaluationId': response_data.get('evaluationId'),
            'eval_id': response_data.get('batchId'),
            'status': response_data.get('status'),
            'details': response_data.get('details', [])
        }
        return evaluation_progress

    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except ValueError:
        print(f"解析JSON时出错:")
    except Exception as e:
        print(f"未知错误: {e}")

    return {'status': '未执行成功'}


def batchresumption(batch_id,model_id, online_model_name, online_url, tokenizer,online_api_key="EMPTY", batch_size=1, num_concurrent=1, num_retry=1, max_gen_toks=-1, gen_kwargs="", mode="FlagRelease", region='bj', user_id=0):
    print("batchresumption",batch_id,model_id, online_model_name, online_url, tokenizer,online_api_key, batch_size, num_concurrent, num_retry, max_gen_toks, gen_kwargs, mode, region, user_id)
    try:
        #print("= = b0", base_url, batch_id, type(batch_id))
        url = f'{base_url}/resumebatches'
        mmdataset,datasets =[],[]
        if mode == "XLC_infer":
            datasets = XLCInfer_DataSets
        elif mode == "XLC_train":
            datasets = XLCTrain_DataSets
        elif mode == "FlagRelease":
            datasets = DataSets
        elif mode == "Qnext":
            datasets = Qwen_DataSets
        elif mode == "XLC":
            mmdataset = XLC_MMDataSets
        elif mode == "EmbodiedVerse":
            mmdataset = Embodied_DataSets
        elif mode == "RoboTrain":
            mmdataset = Robo_MMDataSets

        
        data = {
 	    	"user_id": user_id,
            "model_type":"Chat",
            "tokenizer":{"tokenizer_name":tokenizer},
            "gpus_queue_id":"uuid",
	    	"sence":"EA",
	    	"model_id": model_id if model_id else online_model_name,
	    	"online_model_name": online_model_name,
	    	"online_url": online_url,
	    	"online_api_key": online_api_key,
	    	"dataset":datasets,
            "batch_size": batch_size,
            "num_concurrent": num_concurrent,
            "num_retry":num_retry,
            "max_gen_toks": max_gen_toks,
            "gen_kwargs":gen_kwargs,
            "batch_id":int(batch_id),
            "mmdataset": mmdataset,
            "joint_region":region
	    }
        raw_body = json.dumps(data)
        sign, timestamp = generate_signature(secret, url, raw_body)

        headers = {
            'X-Flageval-Sign': sign,
            'X-Flageval-Timestamp': timestamp,
            'Content-Type': 'application/json',
        }
        response = requests.post(url, headers=headers, data=raw_body)
        if response.status_code == 201:
            response_data = response.json()
            response_data["err_code"]=0
            return response_data
        else:
            return {'err_code':1, 'message': 'resume evaluation failed with:'+response.text}

    except Exception as e:
        print(f"未知错误: {e}")
        return {'err_code':1, 'message': f'resume evaluation except with: {e}'}

def stop_batch(batch_id):
    print("submit stop batch", batch_id)
    try:
        url = f'{base_url}/stopbatches/{int(batch_id)}'

        sign, timestamp = generate_signature(secret, url, "")
        headers = {
            'X-Flageval-Sign': sign,
            'X-Flageval-Timestamp': timestamp,
        }
        response = requests.post(url, headers=headers)
        if response.status_code == 201:
            response_data = response.json()
            response_data["err_code"]=0
            return response_data
        else:
            return {'err_code':1, 'message': 'stop evaluation failed with:'+response.text}
        #response.raise_for_status()  # 如果响应状态不是200，将引发HTTPError异常
        #response_data = response.json()
        #response_data["err_code"]=0
        #return response_data
    except Exception as e:
        print(f"未知错误: {e}")
        import traceback
        print(traceback.format_exc())
        return {'err_code':1,'message': f"stop evluation except with:{e}", 'batchId': batch_id}


def batchlog(batch_id,model_id, online_model_name, online_url, tokenizer,online_api_key="EMPTY", batch_size=1, num_concurrent=1, num_retry=1, max_gen_toks=-1, gen_kwargs="", mode="FlagRelease", user_id=0):
    try:
        #print("= = b0", base_url, batch_id, type(batch_id))
        url = f'{base_url}/batchProgress'
        
        if mode == "XLC_infer":
            datasets = XLCInfer_DataSets
        elif mode == "XLC_train":
            datasets = XLCTrain_DataSets
        else:
            datasets = DataSets
        data = {
 	    	"user_id": user_id,
            "model_type":"Chat",
            "tokenizer":{"tokenizer_name":tokenizer},
            "gpus_queue_id":"uuid",
	    	"sence":"EA",
	    	"model_id": model_id if model_id else online_model_name,
	    	"online_model_name": online_model_name,
	    	"online_url": online_url,
	    	"online_api_key": online_api_key,
	    	"dataset":datasets,
            "batch_size": batch_size,
            "num_concurrent": num_concurrent,
            "num_retry":num_retry,
            "max_gen_toks": max_gen_toks,
            "gen_kwargs":gen_kwargs,
            "batch_id":int(batch_id)
	    }
        raw_body = json.dumps(data)
        sign, timestamp = generate_signature(secret, url, raw_body)

        headers = {
            'X-Flageval-Sign': sign,
            'X-Flageval-Timestamp': timestamp,
            'Content-Type': 'application/json',
        }
        response = requests.post(url, headers=headers, data=raw_body)
        if response.status_code == 200:
            response_data = response.json()
            response_data["err_code"]=0
            return response_data
        else:
            return {'err_code':1, 'message': 'get log failed with:'+response.text}

    except Exception as e:
        print(f"未知错误: {e}")
        return {'err_code':1, 'message': f'get log except with: {e}'}


def mmbatchlog(batch_id,model_id, online_model_name, online_url, tokenizer,online_api_key="EMPTY", batch_size=1, num_concurrent=1, num_retry=1, max_gen_toks=-1, gen_kwargs="", mode="FlagRelease", user_id=0):
    try:
        #print("= = b0", base_url, batch_id, type(batch_id))
        url = f'{base_url}/mmbatchProgress'
        #url = f'{base_url}/batcheprogress'
        
        if mode == "XLC_infer":
            datasets = XLCInfer_DataSets
        elif mode == "XLC_train":
            datasets = XLCTrain_DataSets
        else:
            datasets = DataSets
        data = {
 	    	"user_id": user_id,
            "model_type":"Chat",
            "tokenizer":{"tokenizer_name":tokenizer},
            "gpus_queue_id":"uuid",
	    	"sence":"EA",
	    	"model_id": model_id if model_id else online_model_name,
	    	"online_model_name": online_model_name,
	    	"online_url": online_url,
	    	"online_api_key": online_api_key,
	    	"dataset":datasets,
            "batch_size": batch_size,
            "num_concurrent": num_concurrent,
            "num_retry":num_retry,
            "max_gen_toks": max_gen_toks,
            "gen_kwargs":gen_kwargs,
            "batch_id":int(batch_id)
	    }
        raw_body = json.dumps(data)
        sign, timestamp = generate_signature(secret, url, raw_body)

        headers = {
            'X-Flageval-Sign': sign,
            'X-Flageval-Timestamp': timestamp,
            'Content-Type': 'application/json',
        }
        response = requests.post(url, headers=headers, data=raw_body)
        if response.status_code == 200:
            response_data = response.json()
            response_data["err_code"]=0
            return response_data
        else:
            return {'err_code':1, 'message': 'get log failed with:'+response.text}

    except Exception as e:
        print(f"未知错误: {e}")
        return {'err_code':1, 'message': f'get log except with: {e}'}

if __name__ == "__main__":
    print()
    #print(submit_evaluation("QwQ-32B","http://172.24.165.136:8000/v1/completions"))
    #print(submit_evaluation("doubao-0318","ep-20241112180840-h6t7d","https://ark.cn-beijing.volces.com/api/v3",{"tokenizer_name":"Doubao/ep-20241112180840-h6t7d"},"2936fb06-eebb-414d-9445-75dbeb1d8596"))$^
    #submit_evaluation("Kimi-K2-Instruct-nvidia-origin-concur64", "Kimi-K2-Instruct-nvidia-origin", "http://10.1.15.128:30000/v1/chat/completions", "moonshotai/Kimi-K2-Instruct", "EMPTY", 1, 64, 10, -1, "temperature=0.6")
    #submit_evaluation("Qwen3-235B-A22B-Instruct-2507-ascend-flagos-concur32", "Qwen3-235B-A22B-Instruct-2507-ascend-flagos", "http://10.1.15.113:9010/v1/chat/completions", "Qwen/Qwen3-235B-A22B-Instruct-2507", "EMPTY", 4459, 1, 32,  10, -1,  "temperature=0.7,top_p=0.8,top_k=20,min_p=0,max_gen_toks=16000")
    #submit_evaluation(model_id, online_model_name, online_url, tokenizer,online_api_key="EMPTY", batch_size=1, num_concurrent=1, num_retry=1, max_gen_toks=-1, gen_kwargs="",mode="FlagRelease", region="bj", special_event="Chips", chip="Nvidia-H100", base_model_name="", user_id=0)
    #submit_evaluation("online_api_1120", "Qwen2-7B-Ins", "https://spark-api-open.xf-yun.com/v1/chat/completions", "","7090834e3d9bb24a6ee543651d8fe6b3:NTI2ZmQ1MjU1OTUzY2Y3MTE0MWVmMGEx",1, 1, 10, -1,"","Flagrelease","bj","Chips","Nvidia","4.0Ultra",1526)
    #model_id, online_model_name, online_url, tokenizer,online_api_key="EMPTY", batch_size=1, num_concurrent=1, num_retry=1, max_gen_toks=-1, gen_kwargs="",mode="FlagRelease", region="bj"
    #print(submit_evaluation("robobrain_sz_hfapi", "RoboBrain2.0-7B","https://172.27.37.254:8000/v1/chat/completions", "", "EMPTY",1, 1,10, -1,"","EmbodiedVerse","sz"))
    #(model_id, online_url, online_api_key, online_model_name, batch_size=1, num_concurrent=1, num_retry=1, max_gen_toks=-1,thinking=False, retry_time=-1, mode='FlagRelease', region='bj')
    #print(submit_mm_evaluation("RoboBrain2.0-7B-sz_hfapi", "http://172.27.37.254:8000/v1/chat/completions","EMPTY","RoboBrain2.0-7B", batch_size=1, num_concurrent=6, num_retry=1, max_gen_toks=-1, mode='EmbodiedVerse',region="sz"))
    #submit_evaluation("Kimi-K2-Instruct-nvidia-flagos-concur64", "Kimi-K2-Instruct-nvidia-flagos", "http://10.1.15.128:30000/v1/chat/completions", "moonshotai/Kimi-K2-Instruct",  "EMPTY", 1, 64,  10, -1,  "temperature=0.6")
    #print(submit_evaluation("Qwen2-7B-Instruct-1120","Qwen2-7B-Instruct","http://172.24.226.215:8000/v1/chat/completions","Qwen/Qwen2-7B-Instruct",online_api_key="EMPTY", batch_size=1, num_concurrent=1, num_retry=1, max_gen_toks=-1, gen_kwargs="", mode="FlagRelease", special_event="Chips", chip="Nvidia-A800", base_model_name="Qwen2-7B-Instruct", user_id=66))
    #print(poll_mm_evaluation_progress(3750))
    #print(poll_mm_evaluation_progress(4176))
    #print(poll_evaluation_progress(4877))
    #print(batchlog(4877,"Qwen2-7B-Instruct-1120", "Qwen2-7B-Instruct","http://172.24.226.215:8000/v1/chat/completions","Qwen/Qwen2-7B-Instruct","EMPTY",1,1,1,-1,"","FlagRelease",66))
    #print(stop_batch(4877))
    print(batchresumption(4878,"Qwen2-7B-Instruct-1120", "Qwen2-7B-Instruct","http://172.24.226.215:8000/v1/chat/completions","Qwen/Qwen2-7B-Instruct","EMPTY",1,1,1,-1,"","FlagRelease",'bj',66))
    #print(get_datasetsize())
    #batchresumption(batch_id,model_id, online_model_name, online_url, tokenizer,online_api_key="EMPTY", batch_size=1, num_concurrent=1, num_retry=1, max_gen_toks=-1, gen_kwargs=""):
    #print(batchlog(4149,'Qwen3-4B-cambricon-flagos-lowgems-2', 'Qwen3-4B-cambricon-flagos', 'http://10.1.15.85:9010/v1/chat/completions', 'Qwen/Qwen3-4B',"EMPTY",1,256,10,-1,"temperature=0.6,top_k=20,top_p=0.95,min_p=0",1))
    #print(mmbatchlog(4176,'qwenvl32-klx-flagos-concur32', 'qwenvl32-klx-flagos', 'http://10.1.15.77:8802/v1/chat/completions', "Qwen/Qwen2.5-VL-32B-Instruct", "EMPTY",1,256,10,-1,""))
    #print(stop_batch(4548))
    #details = poll_evaluation_progress(4453)
    #from utils import updatedetails
    #updatedetails(details,"S",4453)
