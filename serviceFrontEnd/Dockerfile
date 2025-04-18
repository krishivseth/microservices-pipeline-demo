FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install flask redis requests
EXPOSE 5000
CMD ["python", "app.py"]
