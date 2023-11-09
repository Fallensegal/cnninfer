FROM python:3.11-slim

WORKDIR /opt/app
RUN pip install poetry==1.6.0
COPY . .
RUN poetry install
CMD ["poetry", "run", "dramatiq", "cnninfer.inferengine:broker", "--threads=1", "--processes=1", "--watch", "."]