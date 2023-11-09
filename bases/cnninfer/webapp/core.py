from fastapi import FastAPI

app = FastAPI()

@app.get("/healthz")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
