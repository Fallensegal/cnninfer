from pydantic import BaseModel
from fastapi import FastAPI
from dramatiq import group
from datetime import timedelta
from components.cnninfer.broker import broker
from components.cnninfer.tasks import core

app = FastAPI()

class Annotations(BaseModel):
    label: str
    confidence: float
class ExperimentData(BaseModel):
    processing_time: timedelta
    picture_label: list[Annotations]
class ExperimentResult(BaseModel):
    before_picture: bytes
    after_picture: bytes
    experiment_data: ExperimentData
class ExperimentResponse(BaseModel):
    result: list[ExperimentResult]

@app.get("/healthz")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/greet")
def greet_users(names: list[str]) -> list[str]:
    g = group([core.hello.send("Wasif"), core.hello.send("Tory")]).run()
    return g.get_results(timeout=10_000, block=True)

