#!/usr/env python3
# -*- coding: utf-8

import re

"""
1956 books
1213 about
6451 polit
6451 religion
6451 inpr
6451 pmain
6451 lmain
5488 relat
13655 status


"""

def getMainInLife(x):
    if x == 1:
        return 'семья и дети'
    elif x == 2:
        return 'карьера и деньги'
    elif x == 3:
        return 'развлечения и отдых'
    elif x == 4:
        return 'наука и исследования'
    elif x == 5:
        return 'совершенствование мира'
    elif x == 6:
        return 'саморазвитие'
    elif x == 7:
        return 'красота и искусство'
    elif x == 8:
        return 'слава и влияние'

def getMainInPeople(x):
    if x == 1:
        return 'ум и креативность'
    elif x == 2:
        return 'доброта и честность'
    elif x == 3:
        return 'красота и здоровье'
    elif x == 4:
        return 'власть и богатство'
    elif x == 5:
        return 'смелость и упорство'
    elif x == 6:
        return 'юмор и жизнелюбие'


def getRelation(x):
    if x == 1:
        return "не женат/не замужем"
    elif x == 2:
        return "есть друг/есть подруга"
    elif x == 3:
        return "помолвлен/помолвлена"
    elif x == 4:
        return "женат/замужем"
    elif x == 5:
        return "всё сложно"
    elif x == 6:
        return "в активном поиске"
    elif x == 7:
        return "влюблён/влюблена"
    elif x == 8:
        return "в гражданском браке"
    elif x == 0:
        return "не указано"

def main():
    file_name = 'books'
    file_namee = 'hr/books'
    f = open(file_name+".txt", "r")
    books = f.read().lower()
    #clear = books.replace("none", "").split(',')
    clear = re.findall(r'\w+\w+\w+\w+', books)

    set_clear = set(clear)

    statistics = ''
    for i in set_clear:
        if i.strip(' []'):
            #k = int(i.strip(' ]['))
            s = "%s: %d\n" % (i, clear.count(i))
            statistics += s

    f = open(file_namee+".txt", 'w')
    f.write(str(statistics))
    f = open(file_namee+".txt", 'r')
    s = f.read().strip().split('\n')
    stat = []
    for i in s:
        buf = i.split(":")
        if buf:
            d = []
            d.append(buf[0])
            d.append(int(buf[1]))
            stat.append(d)
    stat.sort(key=lambda k: k[1], reverse=True)

    f = open(file_namee+".txt", 'w')
    for i in stat:
        f.write(str(i))
        f.write('\n')
    """
    set_info = set(info)

    statistics = ''
    for i in set_info:
        s = "%s: %d\n" % (i, info.count(i))
        statistics += s

    f = open("books_statistics.txt", 'w')
    f.write(str(statistics))
    """

    """
    f = open("name_statistics.txt", 'r')
    s = f.read().strip().split('\n')
    stat = []
    for i in s:
        buf = i.split(":")
        if buf:
            d = []
            d.append(buf[0])
            d.append(int(buf[1]))
            stat.append(d)
    stat.sort(key=lambda k: k[1], reverse=1)

    f = open("name_statistics_sorted.txt", 'w')
    for i in stat:
        f.write(str(i))
        f.write('\n')
    """

if __name__ == '__main__':
    main()
