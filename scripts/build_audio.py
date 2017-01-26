#!/usr/bin/env python3

import yaml
import subprocess

def yaml_loader(filepath):
	"""Loads a yaml file"""
	with open(filepath, "r") as file_descriptor:
		data = yaml.load(file_descriptor)
	return data

def convert_ogg(data):

	pdata = data.get('general')
	oggargs=['oggenc']

	filename = 'lv_s' + str(pdata['season']).zfill(2) + 'e' + str(pdata['episode']).zfill(2)
	title = 's' + str(pdata['season']).zfill(2) + 'e' + str(pdata['episode']).zfill(2) + ': '
	title += pdata['title']

	oggargs.append('../audio/' + filename + '.wav')
	oggargs.append('--output')
	oggargs.append('../audio/' + filename + '.ogg')
	oggargs.append('-q 4')
	oggargs.append('--artist')
	oggargs.append('Linux Voice')
	oggargs.append('--title')
	oggargs.append(title)
	oggargs.append('--album')
	oggargs.append('Season ' + str(pdata['season']).zfill(2))
	oggargs.append('--date')
	oggargs.append(str(pdata['date'].year))
	oggargs.append('--comment')
	oggargs.append(pdata['overview'])
	oggargs.append('--genre')
	oggargs.append('podcast')

	subprocess.run(oggargs)
	
def convert_opus(data):

	pdata = data.get('general')
	opusargs=['opusenc']

	filename = 'lv_s' + str(pdata['season']).zfill(2) + 'e' + str(pdata['episode']).zfill(2)
	title = 's' + str(pdata['season']).zfill(2) + 'e' + str(pdata['episode']).zfill(2) + ': '
	title += pdata['title']

	opusargs.append('--bitrate')
	opusargs.append('45')
	opusargs.append('--artist')
	opusargs.append('Linux Voice')
	opusargs.append('--title')
	opusargs.append(title)
	opusargs.append('--album')
	opusargs.append('Season ' + str(pdata['season']).zfill(2))
	opusargs.append('--date')
	opusargs.append(str(pdata['date'].year))
	opusargs.append('--genre')
	opusargs.append('podcast')
	opusargs.append('--picture')
	opusargs.append('../images/podcast_image.png')
	opusargs.append('../audio/' + filename + '.wav')
	opusargs.append('../audio/' + filename + '.opus')

	subprocess.run(opusargs)

def convert_ffmpeg(data):

	pdata = data.get('general')
	ffmpegargs =['ffmpeg']

	filename = 'lv_s' + str(pdata['season']).zfill(2) + 'e' + str(pdata['episode']).zfill(2)
	title = 's' + str(pdata['season']).zfill(2) + 'e' + str(pdata['episode']).zfill(2) + ': '
	title += pdata['title']

	ffmpegargs.append('-loop')
	ffmpegargs.append('1')
	ffmpegargs.append('-i')
	ffmpegargs.append('../images/podcast_image.png')
	ffmpegargs.append('-i')
	ffmpegargs.append('../audio/' + filename + '.wav')
	ffmpegargs.append('-c:v')
	ffmpegargs.append('libx264')
	ffmpegargs.append('-c:a')
	ffmpegargs.append('aac')
	ffmpegargs.append('-tune')
	ffmpegargs.append('stillimage')
	ffmpegargs.append('-strict')
	ffmpegargs.append('experimental')
	ffmpegargs.append('-b:a')
	ffmpegargs.append('256k')
	ffmpegargs.append('-shortest')
	ffmpegargs.append('../audio/' + filename + '.mp4')

	subprocess.run(ffmpegargs)

def convert_mp3(data):

	pdata = data.get('general')
	lameargs=['lame']

	filename = 'lv_s' + str(pdata['season']).zfill(2) + 'e' + str(pdata['episode']).zfill(2)
	title = 's' + str(pdata['season']).zfill(2) + 'e' + str(pdata['episode']).zfill(2) + ': '
	title += pdata['title']

	lameargs.append('-V2')
	lameargs.append('../audio/' + filename + '.wav')
	lameargs.append('../audio/' + filename + '.mp3')
	lameargs.append('-V 4')
	lameargs.append('--ta')
	lameargs.append('Linux Voice')
	lameargs.append('--tt')
	lameargs.append(title)
	lameargs.append('--tl')
	lameargs.append('Season ' + str(pdata['season']).zfill(2))
	lameargs.append('--ty')
	lameargs.append(str(pdata['date'].year))
	lameargs.append('--tc')
	lameargs.append(pdata['overview'])
	lameargs.append('--tg')
	lameargs.append('podcast')
	lameargs.append('--ti')
	lameargs.append('../images/podcast_image.png')

	subprocess.run(lameargs)

if __name__ == "__main__":
	filepath = "podcast.yaml"
	data = yaml_loader(filepath)
	
	convert_mp3(data)
	convert_ogg(data)
	convert_opus(data)
#	convert_ffmpeg(data)

