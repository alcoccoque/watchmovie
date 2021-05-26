FROM python:3.9
WORKDIR /watchmovie
COPY requirements.txt /
RUN pip3 install --upgrade pip -r requirements.txt
COPY . /watchmovie
EXPOSE 5000

