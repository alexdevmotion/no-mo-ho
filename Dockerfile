FROM python:3-slim

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

CMD ["flask", "run"]
