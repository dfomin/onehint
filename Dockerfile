FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

ARG DATABASE
ARG HOST
ARG PORT
ARG USER
ARG PASSWORD

ENV PYTHONUNBUFFERED=1

ENV DATABASE=$DATABASE
ENV HOST=$HOST
ENV PORT=$PORT
ENV USER=$USER
ENV PASSWORD=$PASSWORD

CMD ["uvicorn", "onehint.main:app", "--host", "0.0.0.0", "--port", "8000"]
