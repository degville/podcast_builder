#!/usr/bin/env python3

import yaml
import html
import os
import datetime
import time
import fileinput
from email import utils
from mutagen.mp3 import MP3

def yaml_loader(filepath):
	"""Loads a yaml file"""
	with open(filepath, "r") as file_descriptor:
		data = yaml.load(file_descriptor)
	return data

def format_episode(data, audioformat):
	
	pdata = data.get('general')
	podcast_filename = 'lv_s' + str(pdata['season']).zfill(2) + 'e' + str(pdata['episode']).zfill(2)
	
	pdate = pdata['date']
	pdatetuple = pdate.timetuple()
	pdatetimestamp = time.mktime(pdatetuple)
	pdate_rfc2822 = utils.formatdate(pdatetimestamp)

	podcast_duration = str(datetime.timedelta(seconds=int(MP3('../audio/' + podcast_filename + '.mp3').info.length)))

	raw_rss = html.unescape('\n<item>\n')
	raw_rss += html.unescape('<title>'+ 'Season ' + str(pdata['season']) + ' Episode ' + str(pdata['episode']) + '</title>\n')
	raw_rss += html.unescape('<itunes:author>' + pdata['presenters'] + '.</itunes:author>\n')
	raw_rss += html.unescape('<itunes:subtitle>Title: ' + pdata['title'] + '</itunes:subtitle>\n')
	raw_rss += html.unescape('<description>\nIn this episode: ' + pdata['overview'] + '.\n</description>\n')
	raw_rss += html.unescape('<enclosure url="http://www.linuxvoice.com/episodes/')
	raw_rss += html.unescape(podcast_filename + '.' + audioformat + '" length="')
	raw_rss += html.unescape(str(os.path.getsize(str('../audio/' + podcast_filename + '.' + audioformat))))
	if audioformat in ['ogg']:
		raw_rss += html.unescape('" type="audio/ogg"/>\n')
	if audioformat in ['mp3']:
		raw_rss += html.unescape('" type="audio/mp3"/>\n')
	if audioformat in ['opus']:
		raw_rss += html.unescape('" type="audio/ogg; codecs=opus"/>\n')
	
	
	
	raw_rss += html.unescape('<pubDate>' + str(pdate_rfc2822) + '</pubDate>\n')
	raw_rss += html.unescape('<itunes:duration>' + podcast_duration + '</itunes:duration>\n')
	raw_rss += html.unescape('<itunes:keywords>' + pdata['tags'] + '</itunes:keywords>\n')
	raw_rss += html.unescape('<guid>http://www.linuxvoice.com/podcast-season-' + str(pdata['season']) + '-episode-' + str(pdata['episode']) + '</guid>\n')
	raw_rss += html.unescape('</item>')

	return raw_rss

def insert_episode(rssdata, audioformat):

	nextline = False

	podcast_filename = 'podcast_' + audioformat + '.rss'
	for line in fileinput.input('../rss/' + podcast_filename,inplace=True):
		if nextline == True:
			print (rssdata)
			nextline = False
		if line.startswith('<!-- Paste latest Linux Voice podcast here -->'):
			nextline = True

		print (line, end='')
	

if __name__ == "__main__":
	filepath = "podcast.yaml"
	data = yaml_loader(filepath)
	
	insert_episode (format_episode(data, 'mp3'),'mp3')
	insert_episode (format_episode(data, 'opus'),'opus')
	insert_episode (format_episode(data, 'ogg'),'ogg')
