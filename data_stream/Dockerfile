FROM python:3.6-slim 

WORKDIR /app 

ADD . /app 

RUN pip install --trusted-host pypi.python.org -r requirements.txt

#CMD ["bash"] in case you want to open a bash terminal 

CMD ["python", "data_stream.py"]