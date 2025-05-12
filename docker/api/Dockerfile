FROM python:3.12-slim

WORKDIR /app
COPY app/ .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/resources/*.csv /app/resources

EXPOSE 5000

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

CMD ["python","app.py"]