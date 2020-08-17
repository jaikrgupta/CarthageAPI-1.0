# Dockerfile - To builld an Docker Image of Python/Flask app.
FROM python:3.8.5
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
