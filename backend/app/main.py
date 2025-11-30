# backend/app/main.py 

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from app.crew.crew_runner import run_industrypath_pipeline

class IdeaRequest(BaseModel):
    idea: str

app = FastAPI(title="IndustryPath AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/generate-roadmap")
async def generate_roadmap(payload: IdeaRequest):
    result = run_industrypath_pipeline(payload.idea)
    return result

@app.get("/health")
async def health():
    return {"status": "ok"}
