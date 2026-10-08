import requests
from datetime import datetime, timedelta

BASE = 'http://127.0.0.1:5000'

s = requests.Session()

print('GET /')
r = s.get(BASE + '/')
print(r.status_code)

# Try register
username = 'smoketest_user'
email = 'smoke@example.com'
password = 'password123'

print('POST /api/register')
r = s.post(BASE + '/api/register', json={'username': username, 'email': email, 'password': password})
print(r.status_code, r.text)

print('POST /api/login')
r = s.post(BASE + '/api/login', json={'username': username, 'password': password})
print(r.status_code, r.text)

print('GET /api/bikes')
r = s.get(BASE + '/api/bikes')
print(r.status_code)
if r.status_code == 200:
    bikes = r.json()
    if not bikes:
        print('No bikes available')
        exit(1)
    bike_id = bikes[0]['id']
else:
    exit(1)

start = (datetime.utcnow() + timedelta(hours=1)).isoformat()
end = (datetime.utcnow() + timedelta(hours=2)).isoformat()

print('POST /api/reservations')
r = s.post(BASE + '/api/reservations', json={'bike_id': bike_id, 'start': start, 'end': end})
print(r.status_code, r.text)

print('GET /api/my_reservations')
r = s.get(BASE + '/api/my_reservations')
print(r.status_code, r.text)

print('GET /app/')
r = s.get(BASE + '/app/')
print(r.status_code)
