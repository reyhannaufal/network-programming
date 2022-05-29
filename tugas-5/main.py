import re
import requests
from bs4 import BeautifulSoup


golang_doc = requests.get("https://go.dev/doc/")

soup = BeautifulSoup(golang_doc.content, 'html.parser')
# print(soup.prettify())
# print(soup.title)
html = list(soup.children)[2]
body = list(html.children)[3]

a_tag = BeautifulSoup(str(body), 'html.parser').find_all('a')

# a tag with href "/doc/tutorial"
a_doc = BeautifulSoup( str(a_tag), 'html.parser').find_all('a', href=re.compile('/doc/tutorial'))

# print a doc
for idx, a in enumerate(a_doc):
    print(idx, ",akan mengambil: ", a.text)


# print(a_doc)
# print(list(body.children)[4])

