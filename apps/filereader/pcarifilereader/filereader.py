"""
Copyright (c) 2015-present, Philippine-California Advanced Research Institutes-
The Village Base Station Project (PCARI-VBTS). All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import csv
import json
from collections import OrderedDict
import os.path


class FileReader(object):
    name = "pcarifilereader"
    version = "1.0"
    author = "pcari.vbts@gmail.com"

    def __init__(
            self,
            name='INQUIRE',
            keyword='INQUIRE',
            number='200',
            args=None):

        self.name = name
        self.keyword = keyword
        self.number = number
        self.files = args['files']

    def instructions(self):
        # sources = '|'.join(self.files.iterkeys())
        instructions = "To use %s app, text %s <keyword> to %s. " \
                       " Example: %s DOCTORS send to %s" % (self.name, self.keyword,
                                                            self.number, self.keyword, self.number)
        return instructions

    @staticmethod
    def error_msg():
        return "Sorry, we're not able to process your request at the moment."

    def read_csv(self, filename):
        result = []
        try:
            with open(filename, "rb") as f:
                reader = csv.reader(f)
                for row in reader:
                    result.append('\\n'.join(row))
                return '\\n'.join(result)
        except Exception as e:
            return self.error_msg()

    def read_file(self, filename):
        result = []
        try:
            with open(filename, 'rb') as f:
                for row in f:
                    result.append(row)
                return '\\n'.join(result)
        except IOError as e:
            return self.error_msg()

    def read_json(self, filename):
        result = []
        try:
            with open(filename, 'r') as f:
                try:
                    data = json.load(f, object_pairs_hook=OrderedDict)
                    for item in data:
                        for filepath, value in item.iteritems():
                            result.append('%s ' % value)
                        result.append('')
                    return '\\n'.join(result)
                except BaseException:
                    return 'No results found.'
        except Exception as e:
            return self.error_msg()

    def run(self, file_key):
        if file_key and file_key.upper() in self.files.iterkeys():

            filename = self.files[file_key.upper()]
            ext = os.path.splitext(filename)[1].lower()
            if ext == '.csv':
                return self.read_file(filename)
            elif ext == '.txt':
                return self.read_file(filename)
            elif ext == '.json':
                return self.read_json(filename)
            else:
                return self.error_msg()
        else:
            return self.instructions()
