FROM python:3-slim

RUN apt-get update && apt-get install -y \
    python-numpy \
    libicu-dev \
    python3-icu

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY requirements.txt ./

# RUN pip install
RUN pip3 install -r requirements.txt

# Bundle app source
COPY . .

# Expose port for outsite connection
EXPOSE 5000

ENV FLASK_APP server.py

CMD ["flask", "run", "--host=0.0.0.0"]
