const net = require('net');

const PORT = 50500;

const server = net.createServer((socket) => {
  console.log('client connected');

  socket.on('data', (data) => {
    try {
      const jsonData = data.toString();
      console.log('received data:', jsonData);
      
      const parsedData = JSON.parse(jsonData);
      console.log('parsed data:', parsedData);
    } catch (error) {
      console.error('error parsing data:', error);
    }
  });

  socket.on('end', () => {
    console.log('client disconnected');
  });
});

server.listen(PORT, () => {
  console.log(`listening on port ${PORT}`);
});
