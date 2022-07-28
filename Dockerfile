
FROM python:3.7
ENV PYTHONUNBUFFERED=1
RUN mkdir -p /var/www/
WORKDIR /var/www/



#Install Cron
RUN apt-get update
RUN apt-get -y install cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD /etc/init.d/cron start && tail -f /var/log/cron.log

#Install vim
RUN apt-get install -y vim


#time zone change
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
RUN TZ=Asia/Taipei \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata

RUN service cron restart
