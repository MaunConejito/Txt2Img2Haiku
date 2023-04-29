FROM node:slim as build

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

# add dependencies
COPY ./package.json ./package-lock.json ./

# clean install
RUN npm ci \
    && npm cache clean --force

# add appc
COPY ./ ./

# prepare .env for build process (prefix with REACT_APP_)
# for some reason environment variables have to be present
# during build-time in order to be read by React
RUN grep -e '^#' -e '^$' frontend.prod.env -v | perl -ne 'print "REACT_APP_$_"' > .env

# Build production
RUN npm run build \
    && npm install -g serve

## Start the app on port 3006
CMD serve -s build -l 3006
