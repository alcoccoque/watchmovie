FROM python:3.9
WORKDIR /heroku
COPY requirements.txt /
RUN pip3 install --upgrade pip -r requirements.txt
COPY . /heroku
EXPOSE 5000

