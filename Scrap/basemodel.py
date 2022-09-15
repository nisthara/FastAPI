from pydantic import BaseModel 

class DBInfo(BaseModel):
    database_type:str
    username:str 
    password:str 
    ip_address:str 
    port_number:int
    database_name:str
