FROM ubuntu
RUN apt-get update
RUN apt-get install -y git postgresql python3-pip python3 libpq-dev npm
RUN git clone -b docker https://github.com/uaprom-summer-2015/Meowth.git
WORKDIR /Meowth

RUN pip3 install -r requirements.txt
RUN python3 manage.py collectstatic

EXPOSE 8000

CMD gunicorn project:app --log-file=- -b 0.0.0.0:8000