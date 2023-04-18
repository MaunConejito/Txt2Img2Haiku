FROM node:latest as build

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

# add dependencies
COPY ./frontend/package.json ./frontend/package-lock.json ./

# clean install
RUN npm ci

# add data
COPY ./data/imgs/ ./public/data/imgs/

# add app
COPY ./frontend/ ./

# prepare .env for build process (prefix with REACT_APP_)
RUN grep -e '^#' -e '^$' .env -v | perl -ne 'print "REACT_APP_$_"' > .env.new
RUN rm .env && mv .env.new .env

# Build production
RUN npm run build
RUN npm install -g serve

## Start the app on port 3006
CMD serve -s build -l 3006
