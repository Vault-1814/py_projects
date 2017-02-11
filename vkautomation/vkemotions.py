import time 
import requests
import cv2
import operator
import numpy as np
import glob
import shutil
import os
import re

#import matplotlib.pyplot as plt

_url = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'
_key = 'f2bfb4e44fb543ad9e70a2c219bc2a9f' #Here you have to paste your primary key
_maxNumRetries = 10

PATH_USER_IDS = 'ids'

def read_ids(file_name):
	ids_file = open(file_name, 'r')
	ids_raw = ids_file.read()
	#s = s.strip('[]').replace("'", "").replace(" ", "").split(',')
	ids = ids_raw.strip("[]' ").split(',')
	ids = [int(id) for id in ids]
	return ids

def is_find_faces(img_path, details=False):
	is_find = False
	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
	img = cv2.imread(img_path)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(100, 100), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
	for (x,y,w,h) in faces:
		if details:
			cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = img[y:y+h, x:x+w]
			eyes = eye_cascade.detectMultiScale(roi_gray)
			for (ex,ey,ew,eh) in eyes:
			    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
			img = cv2.resize(img, (300, 300))
			cv2.imshow('w', img)
			cv2.waitKey()
			cv2.destroyAllWindows()
		is_find = True
	return is_find

def copy_face_files(path, folder_src, folder_dst, img_type='.jpg'):
	photos = glob.glob(path + folder_src + '/*.jpg')
	cnt_copied = 0
	for photo in photos:
		if is_find_faces(photo):
			photo_name = re.search('/[a-zA-Z0-9_-]+.jpg', photo)
			shutil.copyfile(photo, path + folder_src + folder_dst + photo_name.group())
			cnt_copied += 1
	return len(photos), cnt_copied

ids = read_ids(PATH_USER_IDS)
for cnt, id in enumerate(ids):
	try:
		os.mkdir('fotos/' + str(id) + '/faces')
		total, copied = copy_face_files('fotos/', str(id), '/faces')
		progress = 100 * cnt / len(ids)
		print("{0:.2f}% ".format(progress), id, copied, 'from', total)
	except:
		print('folder exists!')
