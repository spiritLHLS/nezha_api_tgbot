FROM python:3.9.13-alpine3.16
RUN cd /opt/ \
    mkdir nezha_api_tgbot \
    cd /opt/
WORKDIR /opt/nezha_api_tgbot
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "run.py"]