#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys, argparse, requests
from pyquery import PyQuery

BASE_DATA_URL = "http://media-kitlv.nl/index.php?option=com_memorixbeeld&view=record&format=topviewxml&tstart=0&id="

def get_image_datafile_id(page_url):
	r = requests.get(page_url)
	pq = PyQuery(r.content)
	datafile_id = pq("div.detailresult").attr("id")
	return datafile_id[3:]

def get_image_datafile(datafile_id):
	global BASE_DATA_URL
	xml_url = BASE_DATA_URL + datafile_id
	r = requests.get(xml_url)
	xml = r.content
	return xml

def main(argv):
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', action='store', dest='url', help='Set page URL', required=True)
	results = parser.parse_args()

	page_url = results.url

	datafile_id = get_image_datafile_id(page_url)
	xml = get_image_datafile(datafile_id)

if __name__ == '__main__':
	main(sys.argv[1:])
