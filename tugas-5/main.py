import re
import requests
from bs4 import BeautifulSoup

# TODO: try catch mechanism, make file modular

golang_doc = requests.get("https://go.dev/doc/")

soup = BeautifulSoup(golang_doc.content, 'html.parser')
html = list(soup.children)[2]
body = list(html.children)[3]

a_tag = BeautifulSoup(str(body), 'html.parser').find_all('a')

a_doc = BeautifulSoup( str(a_tag), 'html.parser').find_all('a', href=re.compile('/doc/tutorial'))

# print a doc
for idx, a in enumerate(a_doc):
    print(idx, ",akan mengambil: ", a.text)


def getGoPackage(query, n):
    golang_package = requests.get("https://pkg.go.dev/search?q=" + query)
    golang_package = requests.get("https://pkg.go.dev/search?limit="+str(n)+"&m=package&q=" + query)
    soup = BeautifulSoup(golang_package.content, 'html.parser')
    packages_links = soup.find_all('div', class_=re.compile("SearchSnippet-headerContainer"))
    packages_descriptions = soup.find_all('p', class_=re.compile("SearchSnippet-synopsis"))

    print("\n")
    for idx, package_link in enumerate(packages_links):
        print(idx + 1, package_link.find('a').get('href'))
        print(packages_descriptions[idx].text)
        



getGoPackage("llrb", 10)