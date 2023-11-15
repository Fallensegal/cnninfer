
from fastapi import FastAPI
from fastapi import APIRouter
from dramatiq import group
from components.cnninfer.broker import broker
from cnninfer.tasks import tasks

app = FastAPI()
storage_router = APIRouter(prefix="/storage", tags=["storage"])
coco_router = APIRouter(prefix="/coco", tags=["coco"])

@app.get("/healthz")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/greet")
def greet_users(names: list[str]) -> list[str]:
    g = group([tasks.hello.send("Wasif"), tasks.hello.send("Tory")]).run()
    return g.get_results(timeout=10_000, block=True)

@storage_router.post("/initialize")
def initialize_coco_dataset(num_pictures: int) -> str:
    msg = tasks.prepare_coco_dataset.send(num_pictures=num_pictures)
    return msg.get_result(timeout=100_000, block=True)

app.include_router(storage_router)
app.include_router(coco_router)

