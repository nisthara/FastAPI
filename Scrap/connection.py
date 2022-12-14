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
    if details.database_type == "mysql":
        dialect = "pymysql"
    elif details.database_type == "oracle":
        dialect = "cx_oracle"
    elif details.database_type == "mssql":
        dialect == "pymssql"
    params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"+
                                    f"SERVER={details.ip_address};"
                                    f"DATABASE={details.database_name};"
                                    f"UID={details.username};"
                                    f"PWD={details.password}")
    
    print("{}+{}:///?odbc_connect={}".format(details.database_type,dialect, params))
    try:
        engine = create_engine("{}+{}:///?odbc_connect={}".format(details.database_type,dialect, params))
        config.engine = engine
        config.connection_details = details
        config.engine.connect()
        return {"msg": "Connection successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

# A decorator to check if a connection exists before calling the passed function
def connection_required(func : Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args:Any, **kwargs:Any):
        if not config.engine:
            raise HTTPException(status_code=403, detail="No live connection exists on the server, try to connect before doing this operation")
        else:
            return func(*args, **kwargs)
    return wrapper