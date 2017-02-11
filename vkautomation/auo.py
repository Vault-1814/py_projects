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
import urllib
import os
import re

URI_API_VK_METHOD = 'https://api.vk.com/method/'
GETING_TOKEN = 'https://oauth.vk.com/authorize?client_id=4798804&scope=notify,friends,photos,audio,video,docs,notes,pages,status,offers,questions,wall,groups,messages,notifications,stats,ads,offline&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token'
PATH_PHOTOS = 'fotos/'

def read_token(file_name='token.secure'):
    file = open(file_name, 'r')
    s = file.read()
    return s

token = read_token()
params = {'access_token': token, 'v': '5.62'}


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





def process_response(response):
    if 'error' not in response:
        if 'response' in response:
            return response['response']
    else:
        err = response.get('error')
        msg = err.get('error_msg')
        print(msg)
        return 404

def downloadProfileAlbums(user_ids):

    """downloads profile album photos and puts for folders for each user_id"""
    for cnt, j in enumerate(user_ids):
        # my id. for test only
        #j = '218406555'
        method = 'photos.get'
        params['owner_id'] = str(j)
        params['album_id'] = 'profile'
        params['rev'] = 1
        params['extended'] = 1
        params['count'] = 1000
        resp = call_api(method, params)
        respt = json.loads(resp.text)
        photos = process_response(respt)
        if photos != 404:
            try:
                os.mkdir(PATH_PHOTOS + str(j))
            except:
                print('user data exists!')
                time.sleep(0.5)
                continue
            f = open(PATH_PHOTOS + str(j) + '/response.txt', 'w')
            json.dump(respt, f, indent=4)
            f.close()
            print(j, photos['count'])
            ps = photos['items']
            count = 0
            for item in ps:
                uri = ''
                if item.get('photo_2560'):
                    uri = item['photo_2560']
                elif item.get('photo_1280'):
                    uri = item['photo_1280']
                elif item.get('photo_807'):
                    uri = item['photo_807']
                elif item.get('photo_604'):                    
                    uri = item['photo_604']
                if uri:
                    try:
                        testfile = urllib.request.URLopener()
                        # alternative method for nameing files    
                        m = re.search(r"/[a-zA-Z0-9_-]+.jpg", uri)
                        photo = m.group()
                        photo_name = "%s%s%s" % (PATH_PHOTOS, j, photo)
                        # in next methd 0.jpg is main photo
                        #photo_name = "%s%s/%d.jpg" % (PATH_PHOTOS, j, count)
                        testfile.retrieve(uri, photo_name) 
                        progress = 100 * cnt / len(user_ids)
                        print("{0:.2f}% ".format(progress), uri, photo_name)
                    except:
                        print('something error in urllib or regexp.')
                    count += 1

def main():
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

    downloadProfileAlbums(s)

    info = []
    about = []
    polit = []
    religion = []
    inspir = []
    pmain = []
    lmain = []
    relat = []
    status = []


 

    """
    for i in range(0, thauthends):
        ids1000 = s[i * qty:(i+1) * qty]
        # получааем кучу инфы об этих людях
        method = 'users.get'
        params['user_ids'] = str(ids1000)
        params['fields'] = 'photo_max_orig'
        resp = call_api(method, params)
        respt = json.loads(resp.text)
        users = process_response(respt)
        for u in users:
            uri = u.get('photo_max_orig')
            print(uri)
            info.append(uri)
            testfile = urllib.request.URLopener()
            testfile.retrieve(uri, 'fotos/' + uri[len(uri)-14:len(uri)]) 
            #wget.download(uri)    

        print(i, " from 0 -> ", thauthends)
        time.sleep(0.01)
    
    f = open('uri_fotos.txt')
    """


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
