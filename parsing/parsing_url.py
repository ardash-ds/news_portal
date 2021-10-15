import requests
import lxml.html
from bs4 import BeautifulSoup


products_list =[]
for i in range(1, 4):   # проходим по 3-м страницам с товарами
    url=f'https://santehnika-tut.ru/vanny/akrilovye/laufen/page{i}.html'

    q = requests.get(url)
    result = q.content

    soup = BeautifulSoup(result, 'lxml')
    products = soup.find_all(class_='img pos_rel')

    for product in products:
        product_url = product.get('href')
        products_list.append(product_url)

with open('products_url.txt', 'w') as file:
    for line in products_list:
        file.write(f'https://santehnika-tut.ru{line}\n')
