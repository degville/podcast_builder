# Podcast builder

Some crude Python scripts used to build the Linux Voice podcast.

In the 'scripts' directory are:
- **podcast.yaml**: this file contains the metadata used by the other scripts. It
  includes details on the contents of the latest podcast.
- **build_audio.py**: encodes the mixed WAV recording of the podcast into Ogg
  Vorbis, mp3 and Opus files, embedded with metadata.
- **build_html.py**: generates the HTML post for the WordPress linuxvoice.com site.
- **build_rss.py**: generates the episode metadata for the RSS files that listeners
  subscribe to.
