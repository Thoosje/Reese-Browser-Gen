import requests, re

site = 'www.ticketmaster.de'
reeseUrl = 'https://www.ticketmaster.de/tmol-dstlxhr.js'

i = 0
while True:
    session = requests.Session()

    r = requests.post('http://localhost:5000/gen', json={'reese': reeseUrl})
    
    data = r.json()['reese']
    print('---- Data ----')
    print(data)

    headers = {
        'accept': 'application/json; charset=utf-8',
        'accept-language': 'nl-NL,nl;q=0.9',
        'content-type': 'text/plain; charset=utf-8',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Chrome OS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    params = {
        'd': site,
    }

    data = {
        'solution': {
            'interrogation': data['data'],
            'version': 'beta'
        },
        'old_token': None,
        'error': None,
        'performance': {
            'interrogation': data['timeSum']
        }
    }

    r = session.post(
        reeseUrl,
        params=params,
        headers=headers,
        json=data,
    )
    print('----- Response -----')
    print(r.text)

    session.cookies.set('reese84', r.json()['token'])
    print('---- Cookies ----')
    print(session.cookies)

    r = session.get(f'https://availability.ticketmaster.de/api/v2/TM_DE/availability/520749', headers=headers)
    
    print(r.text)
    if r.status_code == 200:
        i += 1
        print(i)
        break
    else:
        print(i)
        print('Done')
        break