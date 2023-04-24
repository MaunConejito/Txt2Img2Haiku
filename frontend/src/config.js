import path from 'path-browserify';

const serviceUrl = 'https://' + process.env.REACT_APP_SERVICE_ADDRESS;
const rootDir = path.join(__dirname, '../..');

export const config = {
  serviceUrl: serviceUrl
};
