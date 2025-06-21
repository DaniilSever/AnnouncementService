FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ARG ENV=${ENV}

WORKDIR /src

COPY ./src/requirements* ./

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends netcat-traditional curl \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# Copying source code
COPY src/ /src/

ENV PYTHONPATH=/app

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--app-dir=./", "--reload", "--workers=1", "--proxy-headers", "--host=0.0.0.0", "--port=8080", "--use-colors", "--loop=uvloop"]