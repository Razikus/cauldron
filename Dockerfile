FROM tiangolo/uwsgi-nginx-flask:python2.7
ADD requirements.txt /app
RUN pip install -r /app/requirements.txt
ADD cauldronBase /app
RUN ls /app

