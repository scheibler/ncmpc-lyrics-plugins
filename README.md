Lyrics plugins for ncmpc
============================

This repository contains lyrics plugins for the MPD client program ncmpc:

*   00-hd.sh: Searches for lyrics at your local hard disk. File comes from ncmpc package.
*   01-lyricwiki.py: Searches lyricwiki web site
*   02-dark-lyrics-com.py: Searches for metal and hard rock lyrics at www.darklyrics.com
*   03-lyricsmania-com.py: Searches for German lyrics at lyricsmania.com

To install the lyrics plugins, you must clean ncmpc's lyrics folder first:

```
sudo rm /usr/lib/ncmpc/lyrics/*
```

Then clone this repository:

```
sudo git clone https://github.com/scheibler/ncmpc-lyrics-plugins.git /usr/lib/ncmpc/lyrics/
```

Alternatively you can clone into a user space folder and link the script files to the lyrics plugin folder.

The latter three plugins need the document conversion software [pandoc](http://pandoc.org/):

```
sudo aptitude install pandoc
```

Then start ncmpc and change to the lyrics page by pressing "7". Besides that, you also can use the
plugins without ncmpc. For example:

```
/usr/lib/ncmpc/lyrics/02-dark-lyrics-com.py "artist name" "song name"
```

