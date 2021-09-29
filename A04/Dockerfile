FROM python:3

COPY ./server.py ./server.py
RUN apt-get update
RUN apt-get install -y socat
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
RUN pip install socket
RUN pip install random

EXPOSE 2345
CMD socat TCP-LISTEN:2345,reuseaddr,fork EXEC:"python server.py"
