import base64
import sys
sys.path.insert(1,"/data/liran_code/sat/common/")
import xgcondb as xdb


def get_user_info(type) -> dict:
    if "music" == type or "database" == type:
        path = r"/CMADAAS/APPDATA/DPL/NMIC_BASE_DATASET/CONFIG/DPL.env"
        un_get = dict()
        username, password = str(), str()
        with open(path, "r") as f:
            for i in f.readlines():
                res = base64.b64decode(i.encode("utf-8")).decode("utf-8")
                if type in res.strip():
                    if un_get.setdefault(type):
                        un_get[type].append(res)
                    else:
                        un_get[type] = [res]
        return {"user": [i.split(":")[-1].strip() for i in un_get[type] if "user" in i][0],
                "password": [i.split(":")[-1].strip() for i in un_get[type] if "password" in i][0]}
    else:
        raise Exception("获取方式错误")


def get_database_info():
    conf_sql = r"/CMADAAS/APPDATA/CONFIG/env.properties"
    host_list = str()
    port = str()
    db_name = str()
    with open(conf_sql, "r") as f:
        for i in f.readlines():
            if i.split("=")[0] == "datasource.stdb.addresses":
                host_list = i.split("=")[-1].strip().split(":")[0]
            if i.split("=")[0] == "datasource.stdb.port":
                port = i.split("=")[-1].strip()
            if i.split("=")[0] == "datasource.stdb.dbname":
                db_name = i.split("=")[-1].strip()
    user_info = get_user_info("database")
    _info = {
        "host": host_list,
        "port": int(port),
        "database": db_name,
        "user": user_info["user"],
        "password": user_info["password"],
        "charset": "utf8"
    }
    return _info


def con_xgdb():
    info = get_database_info()
    conn = xdb.connect(host=info['host'], port=info['port'], database=info['database'], user=info['user'],password=info['password'],charset=info['charset'])
    conn.autocommit(False)
    cur = conn.cursor()
    return conn, cur, info['host']


