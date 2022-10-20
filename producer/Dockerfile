FROM python:3.9

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ADD main.py .
ADD entrypoint.sh .

ENV RUNTIME_ENVIRONMENT="DOCKER"

CMD ["./entrypoint.sh"]