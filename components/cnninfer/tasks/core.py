import dramatiq

@dramatiq.actor(store_results=True)
def hello(name:str) -> str:
    saved_string = f'Hello {name}'
    print(saved_string)
    return saved_string

@dramatiq.actor

@dramatiq.actor
def startEverything() -> None:
    download Files
    upload to s3 bucket
    submit each file for inference