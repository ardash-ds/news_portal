import requests
import lxml.html
from lxml import etree
from bs4 import BeautifulSoup

url = 'https://santehnika-tut.ru/product/vanna-iz-litevogo-mramora-marmo-bagno-alessa-new-180-na-80-mbaln18080-s-nozhkami-bez-gidromassazha-233889.html'
html = requests.get(url).content
text = lxml.html.document_fromstring(html)
soup = BeautifulSoup(html, 'lxml')
l = soup.find_all(class_='chars')
var = l[1].find_all(class_='left')
value = l[1].find_all(class_='val')

for i in var:
    print(i.text.strip())

for j in value:
    print(j.text.strip())

# for i in var:
#     print(i)
# for i in li:
#     a = i.find('span')
#     print(a)
# tree = etree.parse('Python.html', lxml.html.HTMLParser())
#
# ul = tree.findall('/body/div/div[3]/div/section/div[2]/div[1]/div/ul/li')
#
# for li in ul:
#     a = li.find('a')
#     t = li.find('time')
#     print(f'{a.text} - {t.get("datetime")}')


# tree = lxml.html.document_fromstring(html)
# t = tree.xpath('/html/body/div[2]/section/div[2]/div[4]/div[3]/text()')
# print(t)
#
# for i in t:
#     print(i)
