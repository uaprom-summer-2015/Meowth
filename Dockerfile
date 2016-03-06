FROM ubuntu

ENV LC_CTYPE C.UTF-8
ENV APP_SETTINGS config.ProductionConfig
ENV STATIC_DIST /staticdata/dist

RUN apt-get update

# Install required packages
RUN apt-get install -y git python3-pip python3 libpq-dev curl \
    libjpeg-dev libfreetype6-dev zlib1g-dev libpng12-dev
# Install nvm and node
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.0/install.sh | bash
RUN . /root/.nvm/nvm.sh && nvm install 0.12

# Change workdir to /opt/hrportal
WORKDIR /opt/hrportal
# Mount current dir to docker's cwd
ADD . .

# Install app's requirements
RUN pip3 install -r requirements.txt

# Build static
RUN echo '{ "allow_root": true }' > /root/.bowerrc
RUN . /root/.nvm/nvm.sh && python3 manage.py static collect

# Run app
CMD gunicorn project:app --log-file=- -b 0.0.0.0:8000
