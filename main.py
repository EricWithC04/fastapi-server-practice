from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import tempfile
from flake8.api import legacy as flake8
import os
import io
import contextlib
from fastapi.middleware.cors import CORSMiddleware
from chatbot import get_completion
from stream_data import websocket_endpoint
from langchain_chat import obtain_qa

app = FastAPI()

class CodeBody(BaseModel):
    code: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las orígenes, puedes especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    
@app.post("/consult")
def consult_chatbot(body_code: CodeBody):
    # return get_completion(body_code.code)
    qa = obtain_qa()
    res = qa.invoke({"query": body_code.code})
    return res["result"]

@app.websocket("/ws/chat")
def consult_websocket(websocket: WebSocket):
    return websocket_endpoint(websocket)