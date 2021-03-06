FROM python:2.7.11
EXPOSE 80
ENV MYDIR /tfdnapredictions
RUN apt-get update
RUN apt-get install nodejs -y
RUN apt-get install npm -y
RUN ln -s /usr/bin/nodejs /usr/bin/node

# Install bigBedToBed
ADD http://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/bigBedToBed /usr/local/bin/bigBedToBed
RUN ["chmod", "777", "/usr/local/bin/bigBedToBed"]

# Install global dependencies
RUN npm install -g npm
RUN npm install webpack -g
RUN ["pip", "install", "gunicorn"]

# Install project dependencies - dependency files are added independently so that
# changes to application source code don't trigger a cache invalidation at this step
WORKDIR ${MYDIR}

ADD requirements.txt ${MYDIR}/
RUN ["pip", "install", "-r", "requirements.txt"]

# install portal requirements
WORKDIR ${MYDIR}/portal
ADD portal/package.json ${MYDIR}/portal/package.json
RUN npm install
RUN npm install --only=dev

# Now add the rest of the application source and run webpack
ADD . ${MYDIR}
RUN webpack

WORKDIR ${MYDIR}
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--timeout", "180", "--log-level=debug", "webserver:app"]
