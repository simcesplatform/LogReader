FROM python:3.7.6

RUN mkdir -p /LogReader/

COPY requirements.txt /LogReader/requirements.txt
RUN pip install -r /LogReader/requirements.txt

COPY LogReader /LogReader/LogReader
COPY testLogReader /LogReader/testLogReader

WORKDIR /LogReader

CMD [ "python", "-m", "LogReader.app" ]
