import os
import io
import time
import base64

import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.ioloop import PeriodicCallback

import picamera

camera = picamera.PiCamera()
camera.resolution = (320, 240)

WEB_PATH = 'web'

base_path = os.path.dirname(os.path.realpath(__file__))
public_path = os.path.join(base_path, WEB_PATH)

class MainHandler(tornado.web.RequestHandler):
  
  def get(self):
    self.render(os.path.join(public_path, 'index.html'))


class StreamingWebSocket(tornado.websocket.WebSocketHandler):

  def on_message(self, message):
    print(message)
    if message == 'start':
      self.camera_loop = PeriodicCallback(self.loop, 16)
      self.camera_loop.start()
      print('streaming start')

  def loop(self):
    bio = io.BytesIO()

    camera.capture(bio, 'jpeg', use_video_port=True)

    try:
      self.write_message(base64.b64encode(bio.getvalue()))
    except tornado.websocket.WebSocketClosedError:
      self.camera_loop.stop()
      print('streaming end')


def make_app():
  return tornado.web.Application([
    (r'/', MainHandler),
    (r'/stream', StreamingWebSocket),
    (r'/js/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(public_path,'js')}),
  ])

if __name__ == '__main__':
  port = 8080

  app = make_app()
  app.listen(port)
  print(f'webserver is running on http://localhost:{port}')
  tornado.ioloop.IOLoop.instance().start()