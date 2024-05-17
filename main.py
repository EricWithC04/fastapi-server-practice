from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CodeBody(BaseModel):
    code: str

@app.get("/")
def read_root():
    return "Hello World!"

@app.post("/execute")
def execute_code(body_code: CodeBody):
    exec(body_code.code)
    return "Code Executed Successfully"