FROM python:3.8.5

RUN pip3 install django

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python3 manage.py migrate

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000