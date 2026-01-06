import mysql.connector
import uuid
import json

#test
#mysql_config = {"host": "127.0.0.1","port":13306, "user": "root","password": "pdXxEHTVAI9k1Q","database": "flageval"}
#online
mysql_config = {"host": "172.31.252.170","port":3306, "user": "flageval","password": "vpPnLRApuWsi84I3CKVnpAJdY0PRKQzEh7/CvNMhS6CAuschP19WF2bDa+FfMU9A","database": "flageval"}

def insertwithid(request_id, model_names, eval_model, batch_id):
    """
    request_id: uuid
    model_names: 模型名称[]
    """
    cnx = mysql.connector.connect(
        host=mysql_config["host"],
        port=mysql_config["port"],
        user=mysql_config["user"],
        password=mysql_config["password"],
        database=mysql_config["database"]
    )

    if cnx.is_connected():
        print("mysql connect")
    # 创建游标对象
    cursor = cnx.cursor()
    record = {'request_id': request_id, "model_names": json.dumps(model_names),"eval_model":eval_model, "batch_id": batch_id}
    insert_query = f'''
    INSERT INTO evaluation_evaldiffs ({", ".join(record.keys())})
    VALUES ({", ".join(["%s"] * len(record))});
    '''
    #VALUES ({", ".join(record.values())}) on DUPLICATE KEY;
    success = False
    cursor.execute(insert_query, tuple(record.values()))
    try:
        cnx.commit()
        success = True
        print("insert success")
    except Exception as e:
        print("insert error:", e)
        cnx.rollback()
    # 关闭游标和连接
    cursor.close()
    cnx.close()
    return success
    
def insert(request_id, model_names, eval_model):
    """
    request_id: uuid
    model_names: 模型名称[]
    """
    cnx = mysql.connector.connect(
        host=mysql_config["host"],
        port=mysql_config["port"],
        user=mysql_config["user"],
        password=mysql_config["password"],
        database=mysql_config["database"]
    )

    if cnx.is_connected():
        print("mysql connect")
    # 创建游标对象
    cursor = cnx.cursor()
    record = {'request_id': request_id, "model_names": json.dumps(model_names),"eval_model":eval_model}
    insert_query = f'''
    INSERT INTO evaluation_evaldiffs ({", ".join(record.keys())})
    VALUES ({", ".join(["%s"] * len(record))});
    '''
    #VALUES ({", ".join(record.values())}) on DUPLICATE KEY;
    success = False
    cursor.execute(insert_query, tuple(record.values()))
    try:
        cnx.commit()
        success = True
        print("insert success")
    except Exception as e:
        print("insert error:", e)
        cnx.rollback()
    # 关闭游标和连接
    cursor.close()
    cnx.close()
    return success

def query(request_id):
    """
    request_id: uuid
    model_names: 模型名称[]
    """
    # 建立连接
    cnx = mysql.connector.connect(
        host=mysql_config["host"],
        port=mysql_config["port"],
        user=mysql_config["user"],
        password=mysql_config["password"],
        database=mysql_config["database"]
    )

    # 创建游标对象
    cursor = cnx.cursor()
    query = f'''
    SELECT eval_model,batch_id, details, status FROM evaluation_evaldiffs WHERE request_id = %s;
    '''
    cursor.execute(query, (request_id,))
    eval_names =[]
    try:
        result = cursor.fetchall()
        eval_names = result[0][0]
        #eval_names = json.loads(result[0][0])
        batch_id = result[0][1] if result[0][1] else -1
        details = json.loads(result[0][2]) if result[0][2] else []
        status = result[0][3] if result[0][3] else 'R'
    except Exception as e:
        print("request_id:", request_id, "query error:", e)
        cnx.rollback()
    # 关闭游标和连接
    cursor.close()
    cnx.close() 
    return eval_names, batch_id, details, status

def querybybatchid(batch_id):
    """
    request_id: uuid
    model_names: 模型名称[]
    """
    # 建立连接
    cnx = mysql.connector.connect(
        host=mysql_config["host"],
        port=mysql_config["port"],
        user=mysql_config["user"],
        password=mysql_config["password"],
        database=mysql_config["database"]
    )

    # 创建游标对象
    cursor = cnx.cursor()
    query = f'''
    SELECT eval_model,batch_id, details, status FROM evaluation_evaldiffs WHERE batch_id = %s;
    '''
    cursor.execute(query, (batch_id,))
    eval_names =[]
    try:
        result = cursor.fetchall()
        eval_names = result[0][0]
        #eval_names = json.loads(result[0][0])
        batch_id = result[0][1] if result[0][1] else -1
        details = json.loads(result[0][2]) if result[0][2] else []
        status = result[0][3] if result[0][3] else 'R'
    except Exception as e:
        print("request_id:", request_id, "query error:", e)
        cnx.rollback()
    # 关闭游标和连接
    cursor.close()
    cnx.close()
    return eval_names, batch_id, details, status

def updatedetails(details, status, batch_id):
    cnx = mysql.connector.connect(
        host=mysql_config["host"],
        port=mysql_config["port"],
        user=mysql_config["user"],
        password=mysql_config["password"],
        database=mysql_config["database"]
    )

    print(details, type(details), type(json.dumps(details))) 
    # 创建游标对象
    cursor = cnx.cursor()
    update_query = """
        UPDATE evaluation_evaldiffs
        SET details = %s, status = %s
        WHERE batch_id = %s;
    """
    success = False 
    try:
        cursor.execute(update_query, (json.dumps(details),status,batch_id))
        cnx.commit()  # 提交事务
        success = True
        print(f"更新成功，影响行数: {cursor.rowcount}")
    except mysql.connector.Error as err:
        cnx.rollback()  # 回滚事务
        print(f"更新失败: {err}")
    finally:
        cursor.close()
        cnx.close()
    return success

def updatedetails_batchid(details, batch_id):
    cnx = mysql.connector.connect(
        host=mysql_config["host"],
        port=mysql_config["port"],
        user=mysql_config["user"],
        password=mysql_config["password"],
        database=mysql_config["database"]
    )

    print(details, type(details), type(json.dumps(details))) 
    # 创建游标对象
    cursor = cnx.cursor()
    update_query = """
        UPDATE evaluation_evaldiffs
        SET details = %s
        WHERE batch_id = %s;
    """
    success = False 
    try:
        cursor.execute(update_query, (json.dumps(details),batch_id))
        cnx.commit()  # 提交事务
        success = True
        print(f"更新成功，影响行数: {cursor.rowcount}")
    except mysql.connector.Error as err:
        cnx.rollback()  # 回滚事务
        print(f"更新失败: {err}")
    finally:
        cursor.close()
        cnx.close()
    return success

def updatebatch_id(batch_id, request_id):
    cnx = mysql.connector.connect(
        host=mysql_config["host"],
        port=mysql_config["port"],
        user=mysql_config["user"],
        password=mysql_config["password"],
        database=mysql_config["database"]
    )

    # 创建游标对象
    cursor = cnx.cursor()
    update_query = """
        UPDATE evaluation_evaldiffs
        SET batch_id = %s
        WHERE request_id = %s;
    """
    success = False 
    try:
        cursor.execute(update_query, (batch_id, request_id))
        cnx.commit()  # 提交事务
        success = True
        print(f"更新成功，影响行数: {cursor.rowcount}")
    except mysql.connector.Error as err:
        cnx.rollback()  # 回滚事务
        print(f"更新失败: {err}")
    finally:
        cursor.close()
        cnx.close()
    return success


def updateall(request_id, eval_model, details, status, batch_id):
    cnx = mysql.connector.connect(
        host=mysql_config["host"],
        port=mysql_config["port"],
        user=mysql_config["user"],
        password=mysql_config["password"],
        database=mysql_config["database"]
    )

    print(details, type(details), type(json.dumps(details)))
    # 创建游标对象
    cursor = cnx.cursor()
    update_query = """
        UPDATE evaluation_evaldiffs
        SET details = %s, status = %s, eval_model=%s, batch_id=%s
        WHERE request_id = %s;
    """
    success = False
    try:
        cursor.execute(update_query, (json.dumps(details),status,eval_model,batch_id, request_id))
        cnx.commit()  # 提交事务
        success = True
        print(f"更新成功，影响行数: {cursor.rowcount}")
    except mysql.connector.Error as err:
        cnx.rollback()  # 回滚事务
        print(f"更新失败: {err}")
    finally:
        cursor.close()
        cnx.close()
    return success

def updateparams(batch_id, description):
    cnx = mysql.connector.connect(
        host=mysql_config["host"],
        port=mysql_config["port"],
        user=mysql_config["user"],
        password=mysql_config["password"],
        database=mysql_config["database"]
    )

    # 创建游标对象
    cursor = cnx.cursor()
    update_query = """
        UPDATE evaluation_evaluation
        SET description = %s
        WHERE id = %s;
    """
    success = False
    try:
        cursor.execute(update_query, (json.dumps(description),batch_id))
        cnx.commit()  # 提交事务
        success = True
        print(f"更新成功，影响行数: {cursor.rowcount}")
    except mysql.connector.Error as err:
        cnx.rollback()  # 回滚事务
        print(f"更新失败: {err}")
    finally:
        cursor.close()
        cnx.close()
    return success

def update_avg(avg,eval_id):
    cnx = mysql.connector.connect(
        host=mysql_config["host"],
        port=mysql_config["port"],
        user=mysql_config["user"],
        password=mysql_config["password"],
        database=mysql_config["database"]
    )

    # 创建游标对象
    cursor = cnx.cursor()

    # 创建游标对象
    cursor = cnx.cursor()
    update_sql = """
                UPDATE evaluation_evaluation
                SET special_event_meta = JSON_SET(
                    special_event_meta, 
                    '$.avg', %s
                )
                WHERE id = %s; 
            """
    success = False
    try:
        cursor.execute(update_sql, (avg,eval_id))
        cnx.commit()  # 提交事务
        success = True
        print(f"更新成功，影响行数: {cursor.rowcount}")
    except mysql.connector.Error as err:
        cnx.rollback()  # 回滚事务
        print(f"更新失败: {err}")
    finally:
        cursor.close()
        cnx.close()
    return success

def updateavg_evalmodel(eval_model, details):
    avg,count = 0,0
    for detail in details:
        print(detail)
        count += detail["accuracy"]
        avg = count/len(details)

    cnx = mysql.connector.connect(
        host=mysql_config["host"],
        port=mysql_config["port"],
        user=mysql_config["user"],
        password=mysql_config["password"],
        database=mysql_config["database"]
    )

    # 创建游标对象
    cursor = cnx.cursor()

    # 创建游标对象
    cursor = cnx.cursor()
    update_sql = """
                UPDATE evaluation_evaluation
                SET special_event_meta = JSON_SET(
                    special_event_meta, 
                    '$.avg', %s
                )
                WHERE name = %s; 
            """
    success = False
    try:
        cursor.execute(update_sql, (avg,eval_model))
        cnx.commit()  # 提交事务
        success = True
        print(f"更新成功，影响行数: {cursor.rowcount}")
    except mysql.connector.Error as err:
        cnx.rollback()  # 回滚事务
        print(f"更新失败: {err}")
    finally:
        cursor.close()
        cnx.close()
    return success

def updateavg_evalmodel_evalid(eval_id, details,created_at):
    avg,count = 0,0
    for detail in details:
        count += detail["accuracy"]
        avg = count/len(details)

    cnx = mysql.connector.connect(
        host=mysql_config["host"],
        port=mysql_config["port"],
        user=mysql_config["user"],
        password=mysql_config["password"],
        database=mysql_config["database"]
    )

    # 创建游标对象
    cursor = cnx.cursor()

    # 创建游标对象
    cursor = cnx.cursor()
    update_sql = """
                UPDATE evaluation_evaluation
                SET special_event_meta = JSON_SET(
                    special_event_meta, 
                    '$.avg', %s
                ), created_at = %s
                WHERE id = %s; 
            """
    success = False
    try:
        cursor.execute(update_sql, (avg,created_at,eval_id))
        cnx.commit()  # 提交事务
        success = True
        print(f"更新成功，影响行数: {cursor.rowcount}")
    except mysql.connector.Error as err:
        cnx.rollback()  # 回滚事务
        print(f"更新失败: {err}")
    finally:
        cursor.close()
        cnx.close()
    return success

def update_cembatch(batch_id, results, try_sequence):

    cnx = mysql.connector.connect(
        host=mysql_config["host"],
        port=mysql_config["port"],
        user=mysql_config["user"],
        password=mysql_config["password"],
        database=mysql_config["database"]
    )

    # 创建游标对象
    cursor = cnx.cursor()
    #SET status='DI' and results = %s
    update_sql = """
                UPDATE cem_batch
                SET status=%s, results = %s, try_sequence =%s
                WHERE id = %s; 
            """
            #"""UPDATE cem_batch 
            #   SET resource,created_at,updated_at,submitted,status,joint_job_id,results,sequence,dry_run,failure_details,failure_kind,model_id,model_ks3_url,try_sequence,model_revision,priority,dags_ready,dags_delayed_tasks,datasets_config,nlp_trending,include_robustness,mm_tar_ks3_key,joint_region,online_model_name
            #   where id=%s;
            #"""
    success = False
    try:
        cursor.execute(update_sql, ("DI",results, try_sequence, batch_id,))
        #cursor.execute(update_sql, (details,batch_id))
        cnx.commit()  # 提交事务
        success = True
        print(f"更新成功，影响行数: {cursor.rowcount}")
    except mysql.connector.Error as err:
        cnx.rollback()  # 回滚事务
        print(f"更新失败: {err}")
    finally:
        cursor.close()
        cnx.close()
    return success


def update_cemdag(batch_id, dataset_id, daginfo):

    cnx = mysql.connector.connect(
        host=mysql_config["host"],
        port=mysql_config["port"],
        user=mysql_config["user"],
        password=mysql_config["password"],
        database=mysql_config["database"]
    )

    # 创建游标对象
    cursor = cnx.cursor()
    #SET status='DI' and results = %s
    update_sql = """
                UPDATE cem_dag
                SET status=%s, result = %s, created_at=%s, updated_at=%s, started_at=%s,stopped_at=%s
                WHERE batch_id = %s and dataset_id = %s; 
            """
            #"""UPDATE cem_batch 
            #   SET resource,created_at,updated_at,submitted,status,joint_job_id,results,sequence,dry_run,failure_details,failure_kind,model_id,model_ks3_url,try_sequence,model_revision,priority,dags_ready,dags_delayed_tasks,datasets_config,nlp_trending,include_robustness,mm_tar_ks3_key,joint_region,online_model_name
            #   where id=%s;
            #"""
    success = False
    try:
        cursor.execute(update_sql, ("S",daginfo["result"],daginfo["created_at"], daginfo["updated_at"], daginfo["started_at"], daginfo["stopped_at"], batch_id,dataset_id,))
        #cursor.execute(update_sql, (details,batch_id))
        cnx.commit()  # 提交事务
        success = True
        print(f"更新成功，影响行数: {cursor.rowcount}")
    except mysql.connector.Error as err:
        cnx.rollback()  # 回滚事务
        print(f"更新失败: {err}")
    finally:
        cursor.close()
        cnx.close()
    return success


def query_cembatch(batch_id):

    cnx = mysql.connector.connect(
        host=mysql_config["host"],
        port=mysql_config["port"],
        user=mysql_config["user"],
        password=mysql_config["password"],
        database=mysql_config["database"]
    )

    # 创建游标对象
    cursor = cnx.cursor()
    query = f'''
    SELECT results FROM cem_batch WHERE id = %s; 
    '''
    cursor.execute(query, (batch_id,))
    eval_names =[]
    try:
        result = cursor.fetchall()
        results = result[0][0]
        print(type(results))
    except Exception as e:
        print("request_id:", batch_id, "query error:", e)
        cnx.rollback()
    # 关闭游标和连接
    cursor.close()
    cnx.close()
    return results

if __name__ == "__main__":
    #model_names = ["MiniMax-M2-nvidia-origin"]
    #request_id = str(uuid.uuid4())
    #batch_id = 28536
    #print(request_id)
    #print(insert(request_id, model_names,model_names[0]))
    #details = [
    #    {"dataname":"livebench_new","status": "S", "dataset": "LiveBench", "accuracy": 74.58, "rawDetails": {}},
    #    {"dataname":"gpqa","status": "S", "dataset": "GPQA", "accuracy": 76.85, "rawDetails": {}},
    #    {"dataname":"musr","status": "S", "dataset": "MUSR", "accuracy": 68.65, "rawDetails": {}},
    #    {"dataname":"mmlu_pro","status": "S", "dataset": "MMLU", "accuracy": 83.21, "rawDetails": {}}, 
    #    {"dataname":"aime","status": "S", "dataset": "AIME", "accuracy": 90, "rawDetails": {}},
    #    {"dataname":"math_500","status": "S", "dataset": "math_500", "accuracy": 93.6, "rawDetails": {}}
    #]
    #details=[{"status": "S", "dataset": "AIME", "accuracy": 0.6666666666666666, "rawDetails": {}}, {"status": "S", "dataset": "GPQA", "accuracy": 0.4303691275167785, "rawDetails": {}}, {"status": "S", "dataset": "LiveBench", "accuracy": 0.4965462105942368, "rawDetails": {}}, {"status": "S", "dataset": "MMLU", "accuracy": 0.671376329787234, "rawDetails": {}}, {"status": "S", "dataset": "MUSR", "accuracy": 0.5925925925925926, "rawDetails": {}}]
    #batch_id=28542
    #eval_id=1367
    #eval_model = 'qwen3moe235-nv-flagos-concur1'
    #batch_id=4604
    #eval_id=257
    #print(updatedetails_evalid(details, eval_id))
    #print(updateall(request_id, model_names[0], details, 'S', batch_id))
    #print(updatedetails(details,'S',batch_id))
    #print(updateavg_evalmodel_evalid(eval_id,details))
    #eval_model,_,details,_ = querybybatchid(4833)
    #avg,count = 0,0
    #for detail in details:
    #    count += detail["accuracy"]
    #avg = count/len(details)
    #print(avg)
    #update_avg(avg,1361)
    #updateavg_evalmodel(eval_model,details)
    #results=query_cembatch(28530)
    #print(type(results))
    #print(type(json.loads(results)))
    #l_results=json.loads(results)
    #for l in l_results:
    #    print(len(l["details"]))
    #    for detail in l["details"]:
    #        print(type(detail))
    #        for k,v in detail.items():
    #            print(k)
    #            if k=="key":
    #                print("key",v)
    #            #if k=="results":
    #            #    for ek,ev in v[0].items():
    #            #        print(ek)
    #            #        #break
    #            #    print(len(v))
    #            if k =="accuracy":
    #                print("acc",v)
            #break
        #for k,v in l.items():
        #    print(k)
        #break
    eval_id=1399
    batch_id=28581

    batchmap={batch_id:28566}
    evalmap={eval_id:1384}
    s="0.4774  0.8051  0.7723  0.8237  0.366   0.548   0.8493  0.5785  0.6161  0.7892  0.5425  0.6404  0.6556"
    s="0.4823   0.8019  0.7649  0.8248  0.374   0.5492  0.8476  0.5802  0.6159  0.7233  0.5291  0.6412  0.6527"
    s="0.4761   0.8082  0.7666  0.827   0.366   0.5483  0.8464  0.5759  0.6183  0.7324  0.5181  0.6359  0.6513"
    s="0.481  0.8011  0.7649  0.8237  0.364   0.5498  0.8485  0.5768  0.6169  0.7832  0.4347  0.636   0.6552"
    s="0.4786   0.8066  0.7551  0.8248  0.376   0.5508  0.8493  0.5853  0.6174  0.8036  0.5451  0.6419  0.6544"
    s="0.4847   0.8122  0.7674  0.8275  0.372   0.5474  0.8489  0.5828  0.6181  0.8059  0.5324  0.6441  0.6514"
    s="0.4761  0.8035  0.7649  0.8264  0.37  0.5474  0.8476  0.5785  0.6171  0.8006  0.535   0.6389  0.6547"
    s="0.4761   0.8106  0.7617  0.8259  0.378   0.5483  0.8485  0.5751  0.6174  0.765   0.4229  0.6412  0.651"
    s="0.2705   0.6251  0.4472  0.7601  0.396   0.667   0.7424  0.4369  0.4346  0.0523  0.0329  0.4042  0.4325"
    s="0.257  0.6275  0.4439  0.765   0.4  0.6954  0.737  0.43  0.4185  0.0447  0.0219  0.3744  0.3843"
    s="0.2546  0.6109  0.2465  0.7612  0.408  0.645  0.7403  0.4147  0.2928  0.1463  0.0505  0.2363  0.2667  0.39"
    #s="0.2448  0.6085  0.2195  0.7644  0.398  0.6287  0.7496  0.401  0.2915  0.144  0.0489  0.2407  0.2579"
    #TruthfulQA (0-shot)    Winogrande (5-shot) CommonsenseQA (5-shot)  PIQA (5-shot)   OpenBookQA (5-shot) BoolQ (5-shot)  ARC Easy (5-shot)   ARC Challenge (5-shot)  MMLU (5-shot)   GSM8K (5-shot)  Minerva Math (4-shot)   CEval (5-shot)  CMMLU (5-shot)
    ls = s.split("  ")
    print(ls, len(ls), type(ls[0]))
    #details = {"details":[{"status": "S", "dataset": "LiveBench", "accuracy": 0.4975, "rawDetails": {}}, {"status": "S", "dataset": "GPQA", "accuracy": 0.3381, "rawDetails": {}}, {"status": "S", "dataset": "MUSR", "accuracy": 0.586, "rawDetails": {}}, {"status": "S", "dataset": "MMLU", "accuracy": 0.6748, "rawDetails": {}}, {"status": "S", "dataset": "AIME", "accuracy": 0.7667, "rawDetails": {}}]}
    details={"details":[{"status": "S", "dataset": "arc_challenge", "accuracy": float(ls[7]), "rawDetails": {}},
                        {"status": "S", "dataset": "arc_easy", "accuracy": float(ls[6]), "rawDetails": {}},
                        {"status": "S", "dataset": "boolq", "accuracy": float(ls[5]), "rawDetails": {}},
                        {"status": "S", "dataset": "ceval-valid", "accuracy": float(ls[11]), "rawDetails": {}},
                        {"status": "S", "dataset": "CMMLU", "accuracy": float(ls[12]), "rawDetails": {}}, 
                        {"status": "S", "dataset": "commonsense_qa", "accuracy":float(ls[2]), "rawDetails": {}},
                        {"status": "S", "dataset": "GSM", "accuracy": float(ls[9]), "rawDetails": {}},
                        {"status": "S", "dataset": "minerva_math_algebra", "accuracy": float(ls[10]), "rawDetails": {}},
                        {"status": "S", "dataset": "MMLU", "accuracy": float(ls[8]), "rawDetails": {}},
                        {"status": "S", "dataset": "openbookqa", "accuracy": float(ls[4]), "rawDetails": {}},
                        {"status": "S", "dataset": "piqa", "accuracy": float(ls[3]), "rawDetails":{}}, 
                        {"status": "S", "dataset": "truthfulqa_mc1", "accuracy": float(ls[0]), "rawDetails": {}},
                        {"status": "S", "dataset": "winogrande", "accuracy": float(ls[1]), "rawDetails": {}}]}
    #with open ("datas/"+str(batchmap[batch_id])+"_details.json","r") as f:
    #    details = json.load(f)
    #    print(updatedetails_batchid(details["details"], batch_id))
    print(updatedetails_batchid(details["details"], batch_id))
    with open ("datas/"+str(evalmap[eval_id])+"_evalinfo.json","r") as f:
        evaldata = json.load(f)
        print(updateavg_evalmodel_evalid(eval_id,details["details"], evaldata["created_at"]))
    with open ("datas/"+str(batchmap[batch_id])+"_cembatch.json","r") as f:
        batchdata = json.load(f)
        results = json.loads(batchdata["results"])
        #with open ("datas/4300_cembatch.json","r") as f:
        #    batchdata2 = json.load(f)
        #    for d in json.loads(batchdata2["results"])[0]["details"]:
        #        if d["key"] == "aime":
        #            results[0]["details"].append(d)
        for detail in results[0]["details"]:
            #print(detail["key"], detail["accuracy"])
            for evdetail in details["details"]:
                if detail["key"] == "gsm8k":
                    if evdetail["dataset"] == "GSM":
                        #print("evacc", evdetail["accuracy"])
                        detail["accuracy"] = evdetail["accuracy"]
                if detail["key"] == "mmlu":
                    if evdetail["dataset"] == "MMLU":
                        detail["accuracy"] = evdetail["accuracy"]
                        #print("evacc", evdetail["accuracy"])
                if detail["key"] == "cmmlu":
                    if evdetail["dataset"] == "CMMLU":
                        detail["accuracy"] = evdetail["accuracy"]
                        #print("evacc", evdetail["accuracy"])
                if evdetail["dataset"] == detail["key"]:
                    detail["accuracy"] = evdetail["accuracy"]
                    #print("evacc", evdetail["accuracy"])
            if detail["key"] == "aime":
                detail["dataset_id"] = 96
                #detail["accuracy"] = 0.7667
                print("change aime dataset id")
    #    for detail in results[0]["details"]:
    #        print(detail["key"], detail["accuracy"])
    #    for detail in results[0]["details"][:]:
    #        if detail["key"] == "TheoremQA":
    #            results[0]["details"].remove(detail)
    #    results[0]["details"].append({"key":"livebench_new","dataset_id":77,"accuracy":0.4975})
    #    results[0]["details"].append({"key":"gpqa_generative_cot","dataset_id":76,"accuracy":0.3381})
    #    results[0]["details"].append({"key":"mmlu_pro","dataset_id":79,"accuracy":0.6748})
    #    results[0]["details"].append({"key":"musr_generative","dataset_id":80,"accuracy":0.586})
        update_cembatch(batch_id, json.dumps(results), batchdata["try_sequence"])
    with open ("datas/"+str(batchmap[batch_id])+"_cemdag.json","r") as f:
        dagdatas = json.load(f)
        for dagdata in dagdatas:
            dataset_id=dagdata["dataset_id"]
     #        #result = "ks3://baai-flageval/"+json.loads(dagdata["result"])["__ks3_key"]
            if dataset_id == 94:
                dataset_id=96
            #dagdata["updated_at"]=None
            update_cemdag(batch_id, dataset_id, dagdata)
