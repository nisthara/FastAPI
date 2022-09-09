from pydantic import BaseModel 
from typing import Union

class DBInfo(BaseModel):
    database_name:str
    username:str 
    password:str 
    ip_address:str 
    port_number:int
    schema_name:str
