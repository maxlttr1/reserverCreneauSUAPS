FROM python:3.10.8-slim-buster
RUN pip install --upgrade pip

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r config/requirements.txt

EXPOSE 5000

CMD ["sh", "-c", "python -u src/main.py & python -u src/web_ui.py"]
