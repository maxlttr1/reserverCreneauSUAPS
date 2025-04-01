FROM python:3.10.8-slim-buster
RUN pip install --upgrade pip

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r config/requirements.txt
RUN mkdir -p /app/config

CMD ["python", "-u", "src/run_auto.py"]