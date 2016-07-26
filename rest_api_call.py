import requests, time

r = requests.post('http://requestb.in/rrj3msrr', data={"ts":time.time()})

print r.status_code
print r.content


r = requests.get('http://requestb.in/rrj3msrr', data={"ts":time.time()})

print r.status_code
print r.content

