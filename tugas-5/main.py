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
    golang_package = requests.get("https://pkg.go.dev/search?limit="+ str(n) +"&m=package&q=" + query)
    soup = BeautifulSoup(golang_package.content, 'html.parser')
    packages_links = soup.find_all('div', class_=re.compile("SearchSnippet-headerContainer"))
    packages_descriptions = soup.find_all('p', class_=re.compile("SearchSnippet-synopsis"))

    print("\n")
    for idx, package_link in enumerate(packages_links):
        if idx == n:
            break
        print(idx + 1, ": ", package_link.text)
        print("\t", packages_descriptions[idx].text)
        print("\n")

def readGoDoc(query):
    golang_doc = requests.get("https://pkg.go.dev/search?q=" + query)
    soup = BeautifulSoup(golang_doc.content, 'html.parser')
    # get href
    packages_links = soup.find_all('div', class_=re.compile("SearchSnippet-infoLabel"))[0]
    packages_links = packages_links.find_all('a')[0]

    read_more = "https://pkg.go.dev" + packages_links.get('href')

    # remove ? from href
    read_more = read_more.split("?")[0]

    read_more_desc = requests.get(read_more)
    soup = BeautifulSoup(read_more_desc.content, 'html.parser')

    # get description
    packages_descriptions = soup.find_all('section', class_=re.compile("Documentation-index"))

    for idx, description in enumerate(packages_descriptions):
        if idx == 2:
            break
        print(description.text)
        print("\n")
    

# TODO: make it modular, use constants, make it more readable ✅   
    


readGoDoc("llrb")
# getGoPackage("llrb", 2)