FROM python:3-slim

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY requirements.txt ./

# RUN pip install
RUN pip3 install -r requirements.txt

ENV FLASK_APP server.py

# Bundle app source
COPY . .

EXPOSE 5000

CMD ["flask", "run"]