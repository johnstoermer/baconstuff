import math
import time
import requests
from lxml import html
import re
import json
from multiprocessing import Pool

def addActor(actor_id):
    movies = []
    url = 'https://www.imdb.com/name/nm'
    #adding the actor_id to url
    zeroes = 6 - math.floor(math.log10(actor_id)) #finding the number of zeroes in the actor_id
    for i in range(0, zeroes):
        url += '0'
    url += str(actor_id) + '/'
    #
    page = requests.get(url)
    tree = html.fromstring(page.content)
    name = tree.xpath('//*[@id="overview-top"]/h1/span[1]/text()')[0]
    birthday = int(tree.xpath('//*[@id="name-born-info"]/time/a[2]/text()')[0])
    movies = tree.xpath('//*[starts-with(@id, "actor-tt")]/b/a/text()')
    dict = {}
    dict['Birthday'] = birthday
    dict['Movies'] = movies
    return [dict, name]

def addMovie(movie_id):
    start = time.time()
    url = 'https://www.imdb.com/title/tt'
    #adding the movie_id to url
    zeroes = 6 - math.floor(math.log10(movie_id)) #finding the number of zeroes in the movie_id
    for i in range(0, zeroes):
        url += '0'
    url += str(movie_id) + '/'
    #
    page = requests.get(url)
    end = time.time()
    print(str(end - start))
    tree = html.fromstring(page.content)
    title = tree.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[2]/div[2]/h1/text()')[0].replace('\xa0', '')
    print(title)
    rating = float(tree.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[1]/div[1]/div[1]/strong/span/text()')[0])
    reviews = int(tree.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[1]/div[1]/a/span/text()')[0].replace(',', ''))
    date = int(tree.xpath('//*[@id="titleYear"]/a/text()')[0])
    count = 2
    cast = []
    while True:
        try:
            cast.append(tree.xpath('//*[@id="titleCast"]/table/tr[{}]/td[2]/a/text()'.format(count))[0][1:-2]) #calling [0] on an empty array will cause an error and break
            count += 1
        except:
            break
    count = 1
    genres = []
    while True:
        try:
            genres.append(tree.xpath('//*[@id="titleStoryLine"]/div[3]/a[{}]/text()'.format(count))[0][1:]) #calling [0] on an empty array will cause an error and break
            count += 1
        except:
            break
    dict = {}
    dict['Rating'] = rating
    dict['Reviews'] = reviews
    dict['Genres'] = genres
    dict['Cast'] = cast
    dict['Date'] = date
    return [dict, title]


def generateJSON(dict):
    with open('baconator.json', 'w', encoding='utf-8') as fp:
        json.dump(dict, fp, ensure_ascii=False, indent=4, sort_keys=True)
        print('Generated JSON')

def main():
    dict = {'Actors': {}, 'Movies': {}}
    with Pool(10) as p:
        d = p.map(addActor, range(1, 100))
        p.close()
        p.join()
        for a in d:
            dict['Actors'][str(a[1])] = a[0]
    with Pool(10) as p:
        d = p.map(addMovie, range(1, 100))
        p.close()
        p.join()
        for a in d:
            dict['Movies'][str(a[1])] = a[0]
    generateJSON(dict)

if __name__ == '__main__':
    main()
