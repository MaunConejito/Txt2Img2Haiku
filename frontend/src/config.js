import path from 'path-browserify';

const serviceUrl = process.env.REACT_APP_SERVICE_URL;
const rootDir = path.join(__dirname, '../..');

export const config = {
  serviceUrl: serviceUrl
};
