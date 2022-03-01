const http = require('http');
const { hostname } = require('os');
const port = process.env.PORT || 3000;
// const hostname = process.env.HOSTNAME || "unknow";
const app_version = process.env.APP_VERSION || "unknow";

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  const msg = `Hello Nodejs! Application version ${app_version} - Alpine ${hostname}\n`
  res.end(msg);
});

server.listen(port, () => {
  console.log(`Server running on http://localhost:${port}/`);
});
