"""
Copyright (c) 2015-present, Philippine-California Advanced Research Institutes-
The Village Base Station Project (PCARI-VBTS). All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

from __future__ import unicode_literals
from HTMLParser import HTMLParser

import feedparser


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


class Rss(object):
    name = "pcarirss"
    version = "1.0"
    author = "pcari.vbts@gmail.com"

    def __init__(self, name='RSS', keyword='RSS', number='200', args=None):

        print args
        self.name = name
        self.keyword = keyword
        self.number = number
        self.feed_sources = args['feeds']
        self.max_number_of_feeds = int(args['max_number_of_feeds'])

    def instructions(self):

        feed_sources = '|'.join(self.feed_sources.iterkeys())
        instructions = "To use %s app, text %s <keyword> send to %s." \
                       "\\nExample: RSS %s" % (
                           self.name,
                           self.keyword,
                           self.number,
                           feed_sources)
        return instructions

    @staticmethod
    def strip_tags(html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    def feeds_by_source(self, key, source):

        try:
            feed = feedparser.parse(source)
            entries = feed.entries
            result = "RSS %s: \\n" % key
            for i in range(0, self.max_number_of_feeds):
                result += "\\n[%s] %s" % (
                    i + 1,
                    entries[i].title)

            return self.strip_tags(result)
        except Exception as e:
            print Exception
            print e
            return "We were unable to process your request. Please try again later."

    def feeds_with_desc_by_source(self, key, source):

        try:
            feed = feedparser.parse(source)
            entries = feed.entries
            result = "RSS %s:\\n" % key
            for i in range(self.max_number_of_feeds):
                result += "\\n[%s] %s: %s" % (
                    i + 1,
                    entries[i].title,
                    entries[i].summary)

            return self.strip_tags(result)

        except Exception as e:
            print Exception
            print e
            return "We were unable to process your request. Please try again later."

    def run(self, source_key):
        if source_key and source_key.upper() in self.feed_sources.iterkeys():
            key = source_key.upper()
            source = self.feed_sources[key]
            return self.feeds_with_desc_by_source(key, source)
        else:
            return self.instructions()
