FROM ubuntu
EXPOSE 5000
RUN apt-get update && apt-get install -y
RUN apt-get install python3 -y
RUN apt-get install python3-pandas -y
RUN apt-get install python3-matplotlib -y
RUN apt-get install python3-flask -y
RUN apt-get install python3-certifi
COPY ./ /var/python_app/
WORKDIR /var/python_app
RUN chmod +x run.sh
RUN /bin/bash run.sh
