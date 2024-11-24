FROM python:3.10.8-slim-buster
RUN pip install --upgrade pip

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Copier example.env en .env si .env n'existe pas
RUN if [ ! -f .env ]; then cp example.env .env; fi

CMD ["python", "-u", "main.py"]