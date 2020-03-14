FROM python:latest
RUN apt -y update && apt -y upgrade && apt -y install python-dev && mkdir /ml
RUN pip3 install oss2 pandas numpy
COPY ./src/process.py /ml/process.py
ENTRYPOINT [ "python3", "/ml/process.py" ]
