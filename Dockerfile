FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

FROM builder AS final
WORKDIR /app
RUN pip install -r requirements.txt --production
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
