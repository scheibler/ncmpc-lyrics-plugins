#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#  Load lyrics from lyrics.wikia.com
#  Author: Eric Scheibler   (email[at]eric-scheibler[dot]de)
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import requests, argparse, sys
from xml.dom import minidom
from subprocess import Popen, PIPE, STDOUT

def download_page(url):
    r = requests.get(url)
    r.encoding = "utf-8"
    return r.text.encode("utf-8")


def extract_url_from_xml_data(xml_contents):
    xml = minidom.parseString(xml_contents)
    for url_node in xml.getElementsByTagName('url'):
        for url in url_node.childNodes:
            return url.nodeValue

def html_to_text(html_content):
    p = Popen(["pandoc", "-f", "html", "-t", "plain"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    return p.communicate(input=html_content)[0]


# create parser object
parser = argparse.ArgumentParser(description="Lyrics parser for http://lyrics.wikia.com")
parser.add_argument("artist", nargs="?", default="", help="Song artist")
parser.add_argument("title", nargs="?", default="", help="Song title")
args = parser.parse_args()
if args.artist == "":
    print "Song artist missing"
    sys.exit(1)
if args.title == "":
    print "Song title missing"
    sys.exit(1)

# query url of actual lyrics page
url = "http://lyrics.wikia.com/api.php?action=lyrics&fmt=xml&func=getSong&artist=%s&song=%s" \
        % (requests.utils.quote(args.artist), requests.utils.quote(args.title))
url = extract_url_from_xml_data(download_page(url))
if not bool(url):
    print("Found no url")
    sys.exit(1)
elif "action=edit" in url:
    print("Found no result")
    sys.exit(69)

# get lyrics
lyric_lines = []
song_part_found = False
for line in html_to_text(download_page(url)).split("\n"):
    if song_part_found:
        if "External links" in line:
            break
        else:
            lyric_lines.append(line)
    else:
        if "music Gracenote" in line:
            song_part_found = True
print("%s - %s\n%s\n%s" \
        % (args.artist, args.title, '-' * (len(args.artist) + 3 + len(args.title)), '\n'.join(lyric_lines)))
