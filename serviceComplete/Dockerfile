FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install redis requests
CMD ["python", "service_complete.py"]
