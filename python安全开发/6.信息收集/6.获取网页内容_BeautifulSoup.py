from bs4 import BeautifulSoup
import requests

content = requests.get('https://www.51kim.com/').text
soup = BeautifulSoup(content, "html.parser")
print(soup.title.string)