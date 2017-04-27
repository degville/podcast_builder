#!/usr/bin/env bash
# Simple script to combine the podcast building scripts
# and upload the resultant files to a server. 

YELLOW='\e[1;33m'
RED='\e[0;31m'
NC='\e[0m' # No Color
SERVER='localhost:/home' # <- Change this

echo -e "${YELLOW}Generating audio files...${RED}"
./build_audio.py

if [ $? -ne 1 ];
then 
	echo -e "${YELLOW}Success${NC}"
else
	echo -e "${YELLOW}Audio generation failed.${NC}"
	exit
fi
	
echo -e "${YELLOW}Generating HTML...${RED}"
./build_html.py > wp_post.html

if [ $? -ne 1 ];
then
	echo -e "${YELLOW}Success${NC}"
else
	echo -e "${YELLOW}HTML generation failed.${NC}"
	exit
fi

echo -e "${YELLOW}Generating RSS...${RED}"
./build_rss.py

if [ $? -ne 1 ];
then
	echo -e "${YELLOW}Success${NC}"
else
	echo -e "${YELLOW}RSS generation failed.${NC}"
	exit
fi

echo -e "${YELLOW}Copying RSS to server.${NC}"
scp ../rss/podcast_*.rss irc.linuxvoice.com:/home/graham/
echo -e "${YELLOW}Copying audio to server.${NC}"
scp ../audio/lv_*.mp3 ../audio/lv_*.ogg ../audio/lv_*.opus ${SERVER}

echo -e "${YELLOW}Success. Podcast generated.${NC}"
