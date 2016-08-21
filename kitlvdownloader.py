#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys, argparse, requests
from pyquery import PyQuery

def get_image_datafile_id(page_url):
	r = requests.get(page_url)
	pq = PyQuery(r.content)
	datafile_id = pq("div.detailresult").attr("id")
	return datafile_id[3:]

def main(argv):
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', action='store', dest='url', help='Set page URL', required=True)
	results = parser.parse_args()

	page_url = results.url

	datafile_id = get_image_datafile_id(page_url)

if __name__ == '__main__':
	main(sys.argv[1:])
