FROM python:3.12

COPY . /io_remastered

WORKDIR /io_remastered

RUN pip3 install -r requirements/common.txt
RUN pip3 install -r requirements/prod.txt
