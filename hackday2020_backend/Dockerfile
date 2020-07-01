FROM ubuntu:latest

RUN apt-get update \
  && apt install -y busybox-static \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN apt-get -y install locales && locale-gen ja_JP.UTF-8 && localedef -f UTF-8 -i ja_JP ja_JP.utf8
ENV LANG ja_JP.UTF-8
ENV LC_CTYPE ja_JP.UTF-8

COPY requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /app

COPY . .

RUN mkdir /app/log

EXPOSE 9000

CMD ["python3", "main.py"]
