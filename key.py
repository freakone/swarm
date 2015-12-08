import threading

def keyboard():
  while True:
    mode = raw_input('Enter your input:')


th_server = threading.Thread(target=keyboard)
th_server.setDaemon(True)
th_server.start()