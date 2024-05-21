from fastapi import FastAPI
from pydantic import BaseModel
import tempfile
from flake8.api import legacy as flake8
import os
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
    
@app.post("/lint")
def lint_code(body_code: CodeBody):
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
        f.write(body_code.code.encode("utf-8"))
        temp_file_name = f.name
    
    style_guide = flake8.get_style_guide(ignore=["E501"])
    report = style_guide.check_files([temp_file_name])
    
    lint_errors = []
    for line in report.get_statistics(""):
        lint_errors.append(line)
    
    os.remove(temp_file_name)
    
    if lint_errors:
        return {"errors": lint_errors}
    else:
        return {"message": "No linting issues found"}