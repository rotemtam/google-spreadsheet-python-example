import requests
import ConfigParser
from simplejson import loads
from helpers import *


if __name__ == '__main__':

	# load and check config file
	cfg = ConfigParser.ConfigParser()
	cfg.read("credentials.ini")
	checkConfig(cfg)
	spr_client = generateClient(cfg)

	# query github's search api to find other repos which are about google spreadsheets in python
	response = requests.get("https://api.github.com/search/repositories?q=google-spreadsheets-python")
	list_of_projects = []

	# create the header row
	list_of_projects.append(['project name', 'full project name', 'project url'])
	data = loads(response.content)

	# Organize the results into a list of lists
	for item in data['items']:
		list_of_projects.append( [item['name'], item['full_name'], item['html_url']])

	# clear all cells
	clearData(spr_client,cfg.get('gdata','spreadsheet'), cfg.get('gdata','worksheet'), min_row='1')

	# write data to spreadsheet
	writeData(spr_client, cfg.get('gdata','spreadsheet'), cfg.get('gdata','worksheet'), list_of_projects, 1)
