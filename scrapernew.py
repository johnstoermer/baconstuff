import requests
from lxml import html

ACTOR_URL = 'https://www.imdb.com/name/nm'
MOVIE_URL = 'https://www.imdb.com/title/tt'

def getMovies(actor):
    movies = []
    url = ACTOR_URL + actor + '/'
    page = requests.get(url)
    tree = html.fromstring(page.content)
    hrefs = tree.xpath('//*[starts-with(@id, "actor-tt")]/b/a')
    for href in hrefs:
        movies.append(href.attrib['href'][9:16])
    return movies

def getActors(movie):
    actors = []
    url = MOVIE_URL + movie + '/fullcredits'
    page = requests.get(url)
    tree = html.fromstring(page.content)
    count = 2
    while True:
        try:
            href = tree.xpath('//*[@id="fullcredits_content"]/table[3]/tr[{}]/td[2]/a'.format(count))[0]
            actors.append(href.attrib['href'][8:15])
            count += 1
        except:
            break
    return actors

def bacon(actors, layer, actor_to_find):
    next_actors = []
    print('LAYER', layer)
    for actor in actors:
        movies = getMovies(actor)
        for movie in movies:
            print('movie:', movie)
            nactors = getActors(movie)
            for nactor in nactors:
                if nactor == actor_to_find:
                    print('GOTTEM')
                    return layer
                next_actors.append(nactor)
    return bacon(next_actors, layer + 1, actor_to_find)

print(bacon(['1212722'], 0, '0705356'))
