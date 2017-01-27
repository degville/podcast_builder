#!/usr/bin/env python3

import yaml
import html
import datetime
import os
from mutagen.mp3 import MP3

def yaml_loader(filepath):
	"""Loads a yaml file"""
	with open(filepath, "r") as file_descriptor:
		data = yaml.load(file_descriptor)
	return data

def return_link(url):
	html_text = html.unescape('<a href="')
	html_text += url
	html_text += html.unescape('">')
	html_text += url
	html_text += html.unescape('</a>')
	return html_text

def return_text_link(text, url):
	html_text = html.unescape('<a href="')
	html_text += url
	html_text += html.unescape('">')
	html_text += text
	html_text += html.unescape('</a>')
	return html_text

def format_general(data):
	preamble = data.get('general')

	html_general = 'Podcast Season ' + str(preamble['season']) + ' Episode ' + str(preamble['episode'])
	html_general += html.unescape('\n\n<p><img \
style="float:left;padding-top:2px;" \
src="http://www.linuxvoice.com/wp-content/uploads/2013/09/rss.png" \
/><strong>&nbsp;Podcast RSS feeds:</strong> <a href="/podcast_ogg.rss">Ogg \
Vorbis</a>, <a href="/podcast_mp3.rss">MP3</a> and <a \
href="/podcast_opus.rss">Opus</a>.</p>\n\n')
	html_general += html.unescape('<h3>Title: ' + preamble['title'] + '</h3>')
	html_general += html.unescape('\n<p>In this episode: ' + preamble['overview'] + '.</p>')
	html_general += html.unescape('\n<!--more-->\n\n<h3>What\'s in the show:</h3>\n')

	return html_general

def format_news(data):
	news = data.get('news')

	html_news = html.unescape('<ul>\n<li>News:<ul>\n<li>\n')
	for item_name, item_value in news.items():
		html_news += item_name.rsplit(' ',2)[0] 
		html_news += ' ' 
		html_news += return_text_link((item_name.rsplit(' ',2)[1] + ' ' + item_name.rsplit(' ',2)[2]), item_value)
		html_news += '. ' 

	html_news += html.unescape('\n</li></ul></li>')
	return html_news

def format_find(data_name, data_value):
	html_data = html.unescape('<li>')
	html_data += data_name + ' ('
	html_data += return_link(data_value)				
	html_data += ').'
	html_data += html.unescape('</li>\n')
	return html_data

def format_finds(data):
	finds = data.get('finds')

	html_finds = html.unescape('<li>Finds of the Fortnight: <ul>\n')
	
	irc_finds = finds.get('irc')
	if (irc_finds):
		html_finds += html.unescape('<li>A selection of finds from from our <a \
href="http://webchat.freenode.net/?channels=linuxvoice">#linuxvoice</a> IRC \
channel on Freenode.</li>\n<li> <ul> \n')
		
		for item_name, item_value in irc_finds.items():
			html_finds += format_find(item_name, item_value)
		html_finds += html.unescape('</ul> </li>\n')

	graham_finds = finds.get('graham')
	if (graham_finds):
		html_finds += html.unescape('<li>Graham:<ul>\n')
		for item_name, item_value in graham_finds.items():
			html_finds += format_find(item_name, item_value)
		html_finds += html.unescape('</ul> </li>\n')

	ben_finds = finds.get('ben')
	if (ben_finds):
		html_finds += html.unescape('<li>Ben:<ul>\n')
		for item_name, item_value in ben_finds.items():
			html_finds += format_find(item_name, item_value)
		html_finds += html.unescape('</ul> </li>\n')

	mike_finds = finds.get('mike')
	if (mike_finds):
		html_finds += html.unescape('<li>Mike:<ul>\n')
		for item_name, item_value in mike_finds.items():
			html_finds += format_find(item_name, item_value)
		html_finds += html.unescape('</ul> </li>\n')

	andrew_finds = finds.get('andrew')
	if (andrew_finds):
		html_finds += html.unescape('<li>Andrew:<ul>\n')
		for item_name, item_value in andrew_finds.items():
			html_finds += format_find(item_name, item_value)
		html_finds += html.unescape('</ul> </li>\n')

	html_finds += html.unescape('</ul> </li>\n')
	return html_finds

def format_neurons(data):
	neurons = data.get('neurons')

	html_neurons = html.unescape('<li>Vocalise your Neurons:<br><ul>\n')
	counter =0
	if (neurons is not None):
		html_neurons += 'Huge thanks to '
		for item_name, item_value in neurons.items():
			if (counter > 0):
				html_neurons += ' and '
			html_neurons += item_name
			html_neurons += ' for ' + item_value
			counter += 1
		html_neurons += '. '
	html_neurons += html.unescape('If you would like Mike to read out your neurons next time, \
email your thoughts to <a href="mailto:mike@linuxvoice.com">mike@linuxvoice.com</a>.\n</li></ul>\n')

	return html_neurons	

def format_votm(data):
	votm = data.get('votm')
	
	html_votm = html.unescape('<li>Voice of the Masses:<br>\n<ul>\n')
	for item_name, item_value in votm.items():
		html_votm += return_text_link(item_name, item_value)
	
	html_votm += html.unescape('\n</ul></li>')	
	return html_votm

def format_footer(data):
	footer = data.get('general')

	podcast_filename = 'lv_s' + str(footer['season']).zfill(2) + 'e' + str(footer['episode']).zfill(2)
	podcast_duration = str(datetime.timedelta(seconds=int(MP3('../audio/' + podcast_filename + '.mp3').info.length)))

	size_mp3 = os.path.getsize(str('../audio/' + podcast_filename + '.mp3')) >> 20
	size_ogg = os.path.getsize(str('../audio/' + podcast_filename + '.ogg')) >> 20
	size_opus = os.path.getsize(str('../audio/' + podcast_filename + '.opus')) >> 20


	html_footer = html.unescape('\n</ul>\n')
	html_footer += html.unescape('<p><strong>Presenters:</strong> ')
	html_footer += footer['presenters'] + '.</p>\n'

	html_footer += html.unescape('\n<audio controls>\n')
	html_footer += html.unescape('  <source src="/episodes/' + podcast_filename + '.ogg" type="audio/ogg">\n')
	html_footer += html.unescape('  <source src="/episodes/' + podcast_filename + '.opus" type="audio/ogg; codecs=opus">\n')
	html_footer += html.unescape('  <source src="/episodes/' + podcast_filename + '.mp3" type="audio/mpeg">\n')
	html_footer += html.unescape('</audio>\n\n')

	html_footer += html.unescape('<p><strong> <a href="/episodes/'+ podcast_filename + '.ogg">Download as high-quality Ogg Vorbis (' + str(size_ogg) + 'MB)</a></strong></p>\n')
	html_footer += html.unescape('<p><strong> <a href="/episodes/'+ podcast_filename + '.mp3">Download as low-quality MP3 (' + str(size_mp3) + 'MB)</a></strong></p>\n')
	html_footer += html.unescape('<p><strong> <a href="/episodes/'+ podcast_filename + '.opus">Download the smaller yet even more awesome Opus file (' + str(size_opus) + 'MB)</a></strong></p>\n')

	html_footer += html.unescape('Duration: ' + podcast_duration + '\n')
	html_footer += html.unescape('\
\n<p>\
Theme Music by <a href="http://www.bradsucks.net/">Brad Sucks</a>. \
</p>\n\
<p>\n\
Recorded, edited and mixed with <a href="https://ardour.org">Ardour</a> using \
GNU/Linux audio plugins from <a href="http://calf-studio-gear.org">Calf Studio \
Gear</a>.\n\
</p>\n\
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img \
alt="Creative Commons License" style="border-width:0" \
src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This \
work is licensed under a <a rel="license"  \
href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons \
Attribution-ShareAlike 4.0 International License</a>.')


	return html_footer

if __name__ == "__main__":
	filepath = "podcast.yaml"
	data = yaml_loader(filepath)
	
	print (format_general(data))
	print (format_news(data))
	print (format_finds(data))
	print (format_neurons(data))
	print (format_votm(data))
	print (format_footer(data))



