FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install redis
CMD ["python", "service_a.py"]
