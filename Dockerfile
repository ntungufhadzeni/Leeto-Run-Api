FROM python:3.9-slim
COPY requirements.txt /
RUN pip3 install -r requirements.txt
COPY . /app
WORKDIR /app
CMD ["gunicorn", "--workers=1", "--threads=2", "-b 0.0.0.0:50", "app:app"]
