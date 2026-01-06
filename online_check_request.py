import os,json
from submit import *
from utils import *

while True:
    with open("logs/flageval_evaldiffs_infos.json","r") as f:
        taskqueue=json.load(f)
        print("taskqueue", taskqueue)
    if taskqueue:
        for taskinfo in taskqueue.values():
            #{'evaluationId': 481, 'eval_id': None, 'status': 'R', 'details': [{'dataset': 'lm_eval-gsm8k', 'status': 'S', 'accuracy': None, 'rawDetails': {}}, {'dataset': 'lm_eval-mmlu', 'status': 'R', 'accuracy': None, 'rawDetails': {}}]}
            #'R': 'RUNNING','S': 'FINISHED','F': 'FAILED',
            print("taskinfo", taskinfo['model'], taskinfo["status"], taskinfo["retry"])
            if taskinfo["status"] == "S" or (taskinfo["status"] in ("F","C") and taskinfo["retry"]>=10) :
                continue
            if taskinfo["Domain"] == "NLP":
                evalinfo = poll_evaluation_progress(taskinfo["batch_id"])
                if "details" in evalinfo and evalinfo["details"]:
                    for detail in evalinfo["details"]:
                        #if detail["status"] == "S" and detail["accuracy"] not None:
                        if detail["accuracy"]:
                            detail["accuracy"] = detail["accuracy"]*100
            else:
                evalinfo = poll_mm_evaluation_progress(taskinfo["batch_id"])
            print("get status from flagevla", evalinfo)
            if evalinfo["status"] in ["S","DI"]:
                #taskinfo["details"] = evalinfo["details"]
                taskinfo["status"] = "S"
                print("update details and status in sql")
                updatedetails(evalinfo["details"], "S", taskinfo["batch_id"])
                print("update details and status in sql done")
                updateavg_evalmodel(taskinfo["eval_model"], evalinfo["details"])
            elif evalinfo["status"] == "R":
                #taskinfo["details"] = evalinfo["details"]
                status = "R"
                if evalinfo["details"]:
                    allsucc = True
                    for detail in evalinfo["details"]:
                        if detail["status"] != "S":
                            allsucc = False
                    if allsucc:
                        taskinfo["status"] = "S"
                        status="S"
                updatedetails(evalinfo["details"],status, taskinfo["batch_id"])
                if status == "S":
                    updateavg_evalmodel(taskinfo["eval_model"], evalinfo["details"])
                        
            elif evalinfo["status"] in ["F","C"]:
                if taskinfo["retry"] >= 10:
                    taskinfo["details"] = {}
                    taskinfo["status"] = "F"
                    updatedetails(evalinfo["details"],"OOR", taskinfo["batch_id"])
                else:
                    print("befor submit",taskinfo)
                    resp = batchresumption(taskinfo["batch_id"],taskinfo["eval_model"], taskinfo["model"], taskinfo["url"], taskinfo["tokenizer"], taskinfo["api_key"], taskinfo["batch_size"], taskinfo["num_concurrent"], taskinfo["num_retry"],taskinfo["max_gen_toks"], taskinfo["gen_kwargs"], taskinfo.get("mode","FlagRelease"), taskinfo.get("region","bj"), taskinfo.get("user_id",0))
                    print("resume batch", resp)
                    taskinfo["retry"] = taskinfo["retry"] + 1
                    #if taskinfo["Domain"] == "NLP":
                    #   
                    #    response = submit_evaluation(taskinfo["eval_model"], taskinfo["model"], taskinfo["url"], taskinfo["tokenizer"], taskinfo["api_key"], taskinfo["batch_size"], taskinfo["num_concurrent"], taskinfo["num_retry"],taskinfo["max_gen_toks"])
                    #else:
                    #    response = submit_mm_evaluation(,taskinfo["eval_model"], taskinfo["model"], taskinfo["url"], taskinfo["api_key"],taskinfo["batch_size"], taskinfo["num_concurrent"], taskinfo["num_retry"],taskinfo["max_gen_toks"])
                    #if response["err_code"] == 0:
                    #    #if model in taskqueue:
                    #    
                    #    retry = taskinfo["retry"] + 1
                    #    #if retry == 10 and taskinfo["status"] == "F":
                    #    #    retry = 0
                    #    #    taskinfo['status'] = 'R'
                    #    taskinfo["batch_id"] = response["batch_id"]
                    #    updatebatch_id(response["batch_id"], taskinfo["request_id"])
                    #    taskinfo["retry"] = retry
                    #        #({"eval_model": eval_model, "model":model,"url":url,"tokenizer":tokenizer,"batch_id": response["batch_id"], "status":"R", "retry": retry, "Domain":"NLP"})
                    #    #else:
                    #    #    taskqueue[model]={"eval_model": eval_model, "model":model,"url":url,"tokenizer":tokenizer,"batch_id": response["batch_id"], "status":"R", "retry": 1, "Domain":"NLP"}
                    ##print("after submit",taskinfo)
            else:
                continue
        #print("after for done", taskqueue)
        with open("logs/flageval_evaldiffs_infos.json", "w") as f:
            f.write(json.dumps(taskqueue))
    time.sleep(300)
