#!/usr/env python3
# -*- coding: utf-8
#
#   +1. авторизация
#   +2. считать данные профиля
#   +3. количество и статус друзей
#   4. проверка и чтение новых сообщений
#   5. проверка уведоблений
#

import requests
import argparse
import json
import time


URI_API_VK_METHOD = 'https://api.vk.com/method/'
GETING_TOKEN = 'https://oauth.vk.com/authorize?client_id=4798804&scope=notify,friends,photos,audio,video,docs,notes,pages,status,offers,questions,wall,groups,messages,notifications,stats,ads,offline&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token'


def get_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument('-l', '--log', required=False, help='log level [DEBUG, WARNING]')
    args = vars(ap.parse_args())
    if not args['log'].upper() in ['DEBUG', 'WARNING']:
        ap.error("Please specify a correct log level.")
    return args


def call_api(method, params):
    """
        method -- exml: (users.get)
        params -- dic with params as in http requests
        :returns response of request to method with params
    """
    url = URI_API_VK_METHOD + method
    response = requests.post(url, data=params)
    return response


def read_token(file_name='token.secure'):
    file = open(file_name, 'r')
    s = file.read()
    return s


def process_response(response):
    if 'error' not in response:
        if 'response' in response:
            return response['response']
    else:
        err = response.get('error')
        msg = err.get('error_msg')
        print(msg)
        return


def main():
    token = read_token()
    params = {'access_token': token, 'v': '5.62'}
    # получаем список идентификаторов мои "друзей"
    method = 'friends.get'
    params['user_id'] = '218406555'
    params['order'] = 'name'
    resp = call_api(method, params)
    resp = json.loads(resp.text)
    friend_ids = resp['response']['items']

    all_ids = []
    """
    for i in friend_ids:
        params['user_id'] = str(i)
        resp = call_api(method, params)
        respt = json.loads(resp.text)
        respt = process_response(respt)
        if respt:
            if 'items' in respt:
                ids = respt['items']
                all_ids.extend(ids)
                print(respt.keys())
                print(len(all_ids))

    f = open('ids', 'w')
    f.write(str(all_ids))
    print(len(all_ids))
    """

    #  читаем идентификаторы друзей и друзей друзей
    f = open('ids', 'r')
    s = f.read()
    s = s.strip('[]').replace("'", "").replace(" ", "").split(',')
    s = [int(item) for item in s]
    # делим по тыщам, из-за ограничений 'users.get'
    #   и вытягиваем из них инфу
    length = len(s)
    qty = 1000
    thauthends = length // qty
    print(length, thauthends)


    info = []
    about = []
    polit = []
    religion = []
    inspir = []
    pmain = []
    lmain = []

    relat = []

    status = []
    for i in range(0, thauthends):
        ids1000 = s[i * qty:(i+1) * qty]
        # получааем кучу инфы об этих людях
        method = 'users.get'
        params['user_ids'] = str(ids1000)
        params['fields'] = 'books, about, personal, relation, status'
        resp = call_api(method, params)
        respt = json.loads(resp.text)
        users = process_response(respt)
        for u in users:
            field = u.get('books')
            if field:
                info.append(field)

                field = u.get('about')
            if field:
                about.append(field)

            field = u.get('personal')
            if field:
                p = field.get('political')
                polit.append(p)
            field = u.get('personal')
            if field:
                r = field.get('religion')
                religion.append(r)
            field = u.get('personal')
            if field:
                ins = field.get('inspired_by')
                inspir.append(ins)
            field = u.get('personal')
            if field:
                pm = field.get('people_main')
                pmain.append(pm)
            field = u.get('personal')
            if field:
                lm = field.get('life_main')
                lmain.append(lm)

            field = u.get('relation')
            if field:
                relat.append(field)
            field = u.get('status')
            if field:
                status.append(field)

        print(i, " from 0 -> ", thauthends)
        time.sleep(0.01)

    f = open('stats/books.txt', 'w')
    print(len(info), "books")
    f.write(str(info))

    f = open('stats/about.txt', 'w')
    print(len(about), "about")
    f.write(str(about))
    f = open('stats/political.txt', 'w')
    print(len(polit), "polit")
    f.write(str(polit))
    f = open('stats/religion.txt', 'w')
    print(len(religion), "religion")
    f.write(str(religion))
    f = open('stats/inspired_by.txt', 'w')
    print(len(inspir), "inpr")
    f.write(str(inspir))
    f = open('stats/people_main.txt', 'w')
    print(len(pmain), "pmain")
    f.write(str(pmain))
    f = open('stats/life_main.txt', 'w')
    print(len(lmain), "lmain")
    f.write(str(lmain))
    f = open('stats/relation.txt', 'w')
    print(len(relat), "relat")
    f.write(str(relat))
    f = open('stats/status.txt', 'w')
    print(len(status), "status")
    f.write(str(status))

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
