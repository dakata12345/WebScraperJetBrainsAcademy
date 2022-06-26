import requests
from bs4 import BeautifulSoup
import string
import os
import shutil

page_total = input()
article_type = input()
for page in range(1, int(page_total) + 1):
    r = requests.get(f"https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={page}")
    if os.path.exists(f'Page_{page}'):
        shutil.rmtree(f'Page_{page}')
    os.mkdir(f'Page_{page}')
    os.chdir(f'Page_{page}')
    if r:
        content = r.content
        soup = BeautifulSoup(content, 'html.parser')
        current = soup.find("li", class_='app-article-list-row__item')
        next = current.find_next("li", class_='app-article-list-row__item')
        while next is not None:
            # process current article
            type = current.find('span', attrs={'data-test': 'article.type'}).find("span").string
            href = current.find('h3').find('a')['href']
            title = current.find('h3').find('a').string
            if type == article_type:
                if string.punctuation in title:
                    title = title.replace(string.punctuation, "")
                with open('_'.join(title.split(" ")) + '.txt', 'w') as file:
                    rq = requests.get('https://nature.com' + href)
                    sp = BeautifulSoup(rq.content, 'html.parser')
                    write_content = sp.find('div', attrs={'class': 'c-article-body'})
                    file.write(write_content.text)
            current = next
            next = next.find_next("li", class_='app-article-list-row__item')
    else:
        print(f"The URL returned {r.status_code}!")
    os.chdir('..')

