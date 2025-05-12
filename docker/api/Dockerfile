FROM python:3.12-slim

WORKDIR /app
COPY api/ .

RUN pip install --no-cache-dir -r requirements.txt

COPY docker/api/wait-for-it.sh /app/
COPY api/resources/*.csv /app/resources

RUN chmod +x /app/wait-for-it.sh
EXPOSE 5000

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

CMD ["python","app.py"]