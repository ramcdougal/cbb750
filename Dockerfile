FROM andrewosh/binder-base

USER root

RUN apt-get update
RUN apt-get install -y mongodb 
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server
RUN apt-get install -y libmysqlclient-dev
RUN pip install pymongo
RUN pip install nltk
RUN pip install sqlalchemy
RUN pip install pymysql
RUN pip install MySQL-python

# let's give ourselves an initial MySQL database
#RUN mysql -u root -e "create database test"; 

RUN cp /home/main/notebooks/setup/my.cnf /etc/mysql/my.cnf

USER main

#CMD mongod --dbpath=/home/main/notebooks/data/db