from fastapi import FastAPI
from pydantic import BaseModel
import io
import contextlib

app = FastAPI()

class CodeBody(BaseModel):
    code: str

@app.get("/")
def read_root():
    return "Hello World!"

@app.post("/execute")
def execute_code(body_code: CodeBody):
    try:
        
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            exec(body_code.code)
        
        output = stdout.getvalue().rstrip()
        
        return { "result": output }
    except Exception as e:
        return {"error": str(e)}