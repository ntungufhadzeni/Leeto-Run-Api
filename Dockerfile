FROM python:3.9-slim
WORKDIR /usr/src/leetoflaskapp
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:50", "app:server"]
