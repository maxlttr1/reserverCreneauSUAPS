FROM python:3.10.8-slim-buster
RUN pip install --upgrade pip

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]