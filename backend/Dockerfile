FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV DB_HOST=db
ENV DB_PORT=5432
ENV DB_NAME=mydb
ENV DB_USER=admin
ENV DB_PASSWORD=admin
EXPOSE 5000
CMD ["python", "app.py"]