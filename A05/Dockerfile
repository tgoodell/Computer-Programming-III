FROM python:3

COPY ./test.py ./test.py
RUN apt-get update
RUN apt-get install -y socat
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
RUN pip install numpy
RUN pip install sympy

EXPOSE 1234
CMD socat TCP-LISTEN:1234,reuseaddr,fork EXEC:"python test.py"
