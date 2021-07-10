FROM python:3.8.6

WORKDIR /opt/powertofly-crawler

VOLUME ["/opt/powertofly-crawler/log","/opt/powertofly-crawler/output"]

COPY requirements.txt /opt/powertofly-crawler

RUN pip install --upgrade pip\
    pip install --no-cache-dir --compile -r requirements.txt

COPY . /opt/powertofly-crawler/

ENTRYPOINT [ "python3", "-u" ]

CMD ["./bin/crawler/main.py"]
