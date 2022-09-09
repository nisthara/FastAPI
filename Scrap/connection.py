from functools import wraps
from typing import Callable, Any
from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine
from basemodel import DBInfo
import urllib
from config import config 

router = APIRouter(prefix="/connect")

@router.post("/")
async def connect(details: DBInfo):
    dialect = "pyodbc"
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
    engine = create_engine("{}+{}:///?odbc_connect={}".format(details.database_name,dialect, params))
    config.engine = engine
    config.connection_details = details
    print("{}+{}:///?odbc_connect={}".format(details.database_name,dialect, params))
    try:
        config.engine.connect()
        return {"msg": "Connection successful"}
    except:
        return {"msg": "Wrong or missing Credentials"}


# A decorator to check if a connection exists before calling the passed function
def connection_required(func : Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args:Any, **kwargs:Any):
        if not config.engine:
            raise HTTPException(status_code=403, detail="No live connection exists on the server, try to connect before doing this operation")
        else:
            return func(*args, **kwargs)
    return wrapper