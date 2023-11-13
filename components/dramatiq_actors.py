import dramatiq

@dramatiq.actor
def infer_standard_dataset() -> None:
    ...