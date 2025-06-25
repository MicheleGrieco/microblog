FROM python:3.12.6-slim

WORKDIR /app

# Update system packages and remove cache after installation
RUN apt-get update && apt-get upgrade -y --with-new-pkgs && apt-get dist-upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=microblog.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["flask", "run"]