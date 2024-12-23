FROM python:3.12.8-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "--reload", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]