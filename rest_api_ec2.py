import requests, time

# store a new record on db on server 
r = requests.post('http://52.65.64.111:8080/activity?activity=touched&code=1')

print r.status_code
print r.content

# get most recent record
r = requests.get('http://52.65.64.111:8080/activity')

print r.status_code
print r.content

# get list of all records
r = requests.get('http://52.65.64.111:8080')

print r.status_code
print r.content
