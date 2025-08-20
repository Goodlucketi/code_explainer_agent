# src/code_explainer_agent/app.py
import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from src.code_explainer_agent.crew import CodeExplainerAgent

# Environment variables
API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = os.environ.get("MODEL_NAME")

# Initialize FastAPI app
app = FastAPI(title="Code Explainer Agent")

origins = [
    "http://localhost:5173",  # React dev
    "https://code-explainer-agent.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ExplainRequest(BaseModel):
    code: Optional[str] = None
    file_path: Optional[str] = None

def run_crew(code_text: str) -> str:
    agent = CodeExplainerAgent()  # Reference the initialized agent
    inputs = {"code_snippet": code_text}
    result = agent.crew().kickoff(inputs=inputs)
    return str(result)

@app.get("/health")
def health():
    return {"status": "ok"}

# JSON-based
@app.post("/explain")
async def explain(code: str = Form(...)):
    if not code.strip():
        raise HTTPException(status_code=400, detail="No code provided.")

    result = run_crew(code.strip())
    return {"ok": True, "result": result}

# File upload (API clients)
@app.post("/explain-file")
async def explain_file(file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8", errors="ignore")
    await file.close()
    if not content.strip():
        raise HTTPException(status_code=400, detail="Uploaded file was empty or non-text.")
    
    result = run_crew(content)
    return {"ok": True, "filename": file.filename, "result": result}

# # 🔑 HTML form submission (pasted code OR file)
# @app.post("/explain-form")
# async def explain_form(code: str = Form(None), file: UploadFile = File(None)):
#     content = None

#     if code:
#         content = code
#     elif file:
#         content = (await file.read()).decode("utf-8", errors="ignore")
#         await file.close()

#     if not content or not content.strip():
#         raise HTTPException(status_code=400, detail="No code or file provided.")

#     result = run_crew(content)
#     return {"ok": True, "result": result}
