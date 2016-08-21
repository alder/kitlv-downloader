#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys, argparse

def main(argv):
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', action='store', dest='url', help='Set page URL', required=True)
	results = parser.parse_args()

	page_url = results.url


if __name__ == '__main__':
	main(sys.argv[1:])
