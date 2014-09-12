#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests, argparse, sys
from subprocess import Popen, PIPE, STDOUT

base_url = "http://www.darklyrics.com"

def download_page(url):
    r = requests.get(url)
    r.encoding = "utf-8"
    p = Popen(["pandoc", "-f", "html", "-t", "markdown"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    return p.communicate(input=r.text.encode("utf-8"))[0]

parser = argparse.ArgumentParser(description="Lyrics parser for www.darklyrics.com")
parser.add_argument("artist", nargs="?", default="", help="Song artist")
parser.add_argument("title", nargs="?", default="", help="Song title")
args = parser.parse_args()
if args.artist == "":
    print "Song artist missing"
    sys.exit(1)
if args.title == "":
    print "Song title missing"
    sys.exit(1)

file = open("/tmp/lyrics_out", "a")
file.write("%s -- %s\n" % (args.artist, args.title))
file.close()

# load results page
result_page = download_page("%s/search?q=%s+%s" % (base_url, \
        args.artist.replace(" ","+"), args.title.replace(" ","+")))
song_url = ""
song_id_on_page = ""
song_part_found = False
for line in result_page.split("\n"):
    if line.startswith("### Songs:"):
        song_part_found = True
        continue
    if song_part_found and "](" in line:
        song_artist = line.strip()[1:].split("](")[0].strip().split(" - ")[0]
        if song_artist.lower() == args.artist.lower():
            song_url = line[:line.__len__()-1].split("](")[1]
            song_id_on_page = song_url.split("#")[-1]
            break
if song_url == "":
    sys.exit(2)

# parse songtext website
result_page = download_page("%s/%s" % (base_url, song_url))
song_name = ""
lyrics = ""
lyrics_start = False
empty_line_detected = False
for line in result_page.split("\n"):
    if song_name == "" and \
            "(#%s)" % song_id_on_page in line:
        song_name = line.split("](")[0].replace("[","").strip()
        lyrics = "%s\n" % song_name
        lyrics += "-" * song_name.__len__() + "\n"
        continue
    if "# %s" % song_name in line:
        lyrics_start = True
        continue
    if lyrics_start and ( \
            "### " in line or \
            "Thanks to " in line or \
            "Submits, comments" in line):
        break
    if lyrics_start:
        line = line.replace("\\", "").strip()
        if line == "":
            if empty_line_detected == False:
                lyrics += "\n"
                empty_line_detected = True
        else:
            lyrics += "%s\n" % line
            empty_line_detected = False

print lyrics[:lyrics.__len__()-1]
sys.exit(0)
