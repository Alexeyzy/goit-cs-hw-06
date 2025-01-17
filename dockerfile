
FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install pymongo

CMD ["python", "main.py"]
