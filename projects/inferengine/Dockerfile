FROM python:3.11-slim

WORKDIR /opt/app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

RUN pip install poetry==1.6.0
COPY . .

RUN poetry install --no-dev --only=worker,infer
RUN poetry run mim install mmengine 
RUN poetry run mim install "mmcv-lite>=2.0.0rc1"
RUN poetry run mim install mmdet
CMD ["poetry", "run", "dramatiq", "cnninfer.inferengine:broker", "--threads=1", "--processes=1"]