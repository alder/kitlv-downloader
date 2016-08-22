#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys, argparse, requests, os, xmltodict, shutil
from pyquery import PyQuery
from PIL import Image

BASE_DATA_URL = "http://media-kitlv.nl/index.php?option=com_memorixbeeld&view=record&format=topviewxml&tstart=0&id="
WORK_DIR = ""

def get_image_datafile_id(page_url):
	r = requests.get(page_url)
	pq = PyQuery(r.content)
	datafile_id = pq("div.detailresult").attr("id")
	return datafile_id[3:]

def get_filtered_image_title(page_url):
	r = requests.get(page_url)
	pq = PyQuery(r.content)
	filtered_image_title = pq("h1.contentheading").text()
	filter_chars = ["\\", "/", " ", ",", "."]
	for char in filter_chars:
		filtered_image_title = filtered_image_title.replace(char, "-")
	return filtered_image_title

def get_image_datafile(datafile_id):
	global BASE_DATA_URL
	xml_url = BASE_DATA_URL + datafile_id
	r = requests.get(xml_url)
	xml = r.content
	return xml

def parse_image_data(xml):
	parsed_data = xmltodict.parse(xml)
	image_data = {"tileurl": parsed_data["viewer"]["config"]["tileurl"]}
	image_data.update(parsed_data["viewer"]["topviews"]["topview"]["tjpinfo"])

	return image_data

def download_image_pieces(image_data):
	global WORK_DIR
	numfiles = int(image_data["numfiles"])+1
	for i in range (1, numfiles):
		url = image_data["tileurl"] + image_data["filepath"] + "&" + str(i)
		print("Downloaded {0} of {1}:".format(i, numfiles), url)
		r = requests.get(url, stream=True)
		with open(os.path.join(WORK_DIR, str(i)+".jpg"), 'wb') as f:
			r.raw.decode_content = True
			shutil.copyfileobj(r.raw, f)

def combine_images(image_data):
	global WORK_DIR

	for layer in image_data['layers']['layer']:
		width = int(layer['@width'])
		height = int(layer['@height'])
		new_image = Image.new('RGB', (width, height))
		start_x = 0
		start_y = 0
		cur_width = 0
		cur_height = 0
		img_num = int(layer['@starttile'])
		for i in range(1, int(layer['@rows'])+1):
			for j in range(1, int(layer['@cols'])+1):
				paste_image = Image.open(os.path.join(WORK_DIR, str(img_num)+".jpg"))
				new_image.paste(paste_image, (start_x, start_y))
				img_num+=1
				cur_width, cur_height = paste_image.size
				start_x += cur_width
			start_y += cur_height
			start_x = 0


		new_image.save(os.path.join(WORK_DIR, WORK_DIR+"_{0}x{1}.jpg".format(width, height)))
		print("Save {0} layer of {1} with size {2}x{3}".format(layer['@no'], len (image_data['layers']['layer']), width, height))

def main(argv):
	global WORK_DIR

	parser = argparse.ArgumentParser()
	parser.add_argument('-u', action='store', dest='url', help='Set page URL', required=True)
	results = parser.parse_args()

	page_url = results.url

	datafile_id = get_image_datafile_id(page_url)
	WORK_DIR = get_filtered_image_title(page_url)
	if not os.path.exists(WORK_DIR):
		os.makedirs(WORK_DIR)
	xml = get_image_datafile(datafile_id)
	image_data = parse_image_data(xml)
	download_image_pieces(image_data)
	combine_images(image_data)

if __name__ == '__main__':
	main(sys.argv[1:])
