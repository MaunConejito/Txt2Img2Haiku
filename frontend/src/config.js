import path from 'path-browserify';

const serviceUrl = 'http://' + process.env.REACT_APP_SERVICE_ADDRESS;
const rootDir = path.join(__dirname, '../..');
const imgDirectory = path.join(rootDir,
                               process.env.REACT_APP_DATA_REL_PATH,
                               process.env.REACT_APP_IMG_SUB_DIR);

export const config = {
  serviceUrl: serviceUrl,
  imgDirectory: imgDirectory
};
