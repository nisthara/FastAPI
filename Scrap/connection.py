from functools import wraps
from typing import Callable, Any
from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine
from basemodel import DBInfo
import urllib

engine = None
connection_details = None


router = APIRouter(prefix="/connect")

@router.post("/")
async def connect(details: DBInfo):
    dialect = "pyodbc"
    global engine
    if details.database_name == "mysql":
        dialect = "pymysql"
    elif details.database_name == "oracle":
        dialect = "cx_oracle"
    elif details.database_name == "mssql":
        dialect == "pymssql"
    params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"+
                                    f"SERVER={details.ip_address};"
                                    f"DATABASE={details.schema_name};"
                                    f"UID={details.username};"
                                    f"PWD={details.password}")
    conn_string = f"{details.database_name}+{dialect}://{details.username}:{details.password}@{details.ip_address}:{details.port_number}/{details.schema_name}"
    global connection_details
    engine = create_engine("{}+{}:///?odbc_connect={}".format(details.database_name,dialect, params))
    print("{}+{}:///?odbc_connect={}".format(details.database_name,dialect, params))
    connection_details = details
    try:
        engine.connect()
        return {"msg": "Connection successful"}
    except:
        return {"msg": "Wrong or missing Credentials"}


# A decorator to check if a connection exists before calling the passed function
def connection_required(func : Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args:Any, **kwargs:Any):
        global engine
        if not engine:
            raise HTTPException(status_code=403, detail="No live connection exists on the server, try to connect before doing this operation")
        else:
            return func(*args, **kwargs)
    return wrapper