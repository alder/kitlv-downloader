#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys, argparse, requests, os
from pyquery import PyQuery

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

if __name__ == '__main__':
	main(sys.argv[1:])
