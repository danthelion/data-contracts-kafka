FROM python:3.9

RUN mkdir /app
WORKDIR /app

# Update default packages
RUN apt-get update

# Get Ubuntu packages
RUN apt-get install -y \
    build-essential \
    curl

# Update new packages
RUN apt-get update

# Get Rust
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y

ENV PATH="/root/.cargo/bin:${PATH}"

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ADD main.py .
ADD entrypoint.sh .

ENV RUNTIME_ENVIRONMENT="DOCKER"

CMD ["./entrypoint.sh"]