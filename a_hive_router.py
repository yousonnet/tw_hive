
from accounts_gen import accounts_root_data
from hive_class import Hive
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


a_hive = Hive(accounts_root_data)
app = FastAPI()

class CallFunctionRequest(BaseModel):
    account_index: int
    call_class: str
    method_name: str
    parameters_dict: dict

@app.post("/call-function")
async def call_function(request: CallFunctionRequest):
    try:
        result = await a_hive.call_func(
            account_index=request.account_index,
            call_class=request.call_class,
            method_name=request.method_name,
            parameters_dict=request.parameters_dict
        )
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/accounts-nums")
async def get_accounts_nums():
    try:
        result = a_hive.accounts_length
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.get("/")
async def read_root():
    return {"Hello": "World"}