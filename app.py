from flask import Flask
from datetime import timedelta
import requests_cache
from bs4 import BeautifulSoup as BS

session = requests_cache.CachedSession('fotd', expire_after=timedelta(hours=3))

app = Flask(__name__, static_folder='web/static')

@app.get('/fotd')
def get_fotd():
    return {
        'kopps': get_kopps(),
        # 'oscars': get_oscars(),
        # 'culvers_capitol': get_culvers_capitol(),
        # 'culvers_bluemound': get_culvers_bluemound(),
        # 'culvers_mainst': get_culvers_mainst(),
    }

def get_kopps():
    res = session.get("https://www.kopps.com/flavor-preview")
    soup = BS(res.content, 'html.parser')
    all_fotds = soup.find(id='page').find_all('div', class_='wrap todays-flavors-wrap flavor-forecast')
    two_flavors = all_fotds[0].find_all('div', class_='col-3')
    fotds = []
    for f in two_flavors:
        img_url = "https://www.kopps.com" + f.find('img').get('src')
        flavor_name = f.find('span').get_text()
        fotds.append({'img_url': img_url, 'flavor_name': flavor_name})
    return { 
        'cached': res.from_cache, 
        'fotds': fotds,
    }
