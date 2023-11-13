import threading
import requests

def make_request():
    r = requests.post('http://127.0.0.1:5000/gen', json={'reese': 'https://www.ticketmaster.de/tmol-dstlxhr.js'})
    print(r.text)

threads = []
for i in range(3):
    thread = threading.Thread(target=make_request)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
