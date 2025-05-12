FROM python:3.12-slim

WORKDIR /app
COPY app/ .

RUN pip install --no-cache-dir -r requirements.txt

COPY docker/api/wait-for-it.sh /app/
COPY app/resources/*.csv /app/resources

RUN chmod +x /app/wait-for-it.sh
EXPOSE 5000

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

CMD ["python","app.py"]