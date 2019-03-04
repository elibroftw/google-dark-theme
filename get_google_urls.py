import requests
from bs4 import BeautifulSoup

url = 'http://www.orchidbox.com/list-of-google-websites-with-country-codes'
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, 'html.parser')


with open('matches.txt', 'w') as f:
    for td in soup.find_all('td'):
        if td.get('width') == '164':
            f.write(', "' + td.text + '/"')
            f.write(', "' + td.text + '/search*"')
