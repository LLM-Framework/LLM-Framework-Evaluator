from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import evaluate_router
from src.config import settings

app = FastAPI(title="LLM Evaluator Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(evaluate_router, prefix="/api/v1", tags=["Evaluation"])

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "evaluator"}

@app.get("/")
async def root():
    return {"service": "LLM Evaluator Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.evaluator_host,
        port=settings.evaluator_port,
        reload=settings.debug
    )