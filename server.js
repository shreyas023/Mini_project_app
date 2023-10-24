const { createServer } = require('http');
const { spawn } = require('child_process');

const server = createServer((req, res) => {
  const pythonProcess = spawn('python', ['main.py']);

  pythonProcess.stdout.on('data', (data) => {
    res.end(data);
  });

  pythonProcess.stderr.on('data', (data) => {
    res.end(`Error: ${data}`);
  });
});

server.listen(3000, () => {
  console.log('Node.js server listening on port 3000');
});
