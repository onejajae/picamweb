"use strict";

const camera = {
  viewfinder: document.getElementById('viewfinder'),
  frameCounter: document.getElementById('frame-counter'),
  socket: null,
  countFrames: 0,
  startTime: null,
  
  connect() {
    this.socket = new WebSocket('ws://'+window.location.host+'/stream');

    this.socket.onopen = (event) => {
      document.getElementById('start-button').hidden = true;
      this.frameCounter.hidden = false;

      document.getElementById('capture-button').addEventListener('click', () => {
        this.socket.send('capture');
      });
      document.getElementById('capture-button').hidden = false;
      
      console.log("connected");
      this.start();
    };

    this.socket.onmessage = (event) => {
      this.viewfinder.src = "data:image/jpeg;base64," + event.data;
      this.countFrames++;
      this.frameCounter.innerHTML = (this.countFrames / (new Date()-this.startTime) * 1000).toFixed(2);
    };
 
  },

  start() {
    this.countFrames = 0;
    this.startTime = new Date();
    this.socket.send('start');
  },
  
  stop() {
    this.socket.send('stop');
  }

}