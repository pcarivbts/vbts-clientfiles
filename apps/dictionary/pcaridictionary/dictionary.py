"""
Copyright (c) 2015-present, Philippine-California Advanced Research Institutes-
The Village Base Station Project (PCARI-VBTS). All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import re
import subprocess


class Dictionary(object):
    name = "pcaridictionary"
    version = "1.0"
    author = "pcari.vbts@gmail.com"

    def __init__(
            self,
            name='DICTIONARY',
            keyword='DICTIONARY',
            number='200',
            args=None):

        self.name = name
        self.keyword = keyword
        self.number = number

    def instructions(self):
        instructions = "To use %s app, text %s DEFINE|SYNONYM|ANTONYM|RANDOM <word> " \
                       "and send to %s. Example: %s DEFINE dictionary " % (self.name,
                                                                           self.keyword, self.number, self.keyword)
        return instructions

    @staticmethod
    def define(word):
        if re.match('\W', word):
            return 'Your input is not a word'
        try:
            cmd = "dict -d wn %s | tail -n +5" % word
            return subprocess.check_output(cmd, shell=True)
        except BaseException:
            return 'Word not found.'

    @staticmethod
    def synonym(word):
        if re.match('\W', word):
            return 'Your input is not a word'
        try:
            cmd = "dict -d moby-thesaurus %s | tail -n +6" % word
            res = subprocess.check_output(cmd, shell=True)
            return "Synonym(s) for %s: %s" % (word, res)
        except BaseException:
            return 'Synonym not found.'

    @staticmethod
    def antonym(word):
        if re.match('\W', word):
            return 'Your input is not a word'
        try:
            cmd = "dict -d wn %s | egrep -o -e '\[ant: \{.+\}+\]' | egrep -o -e '\{.+\}+'" % word
            res = subprocess.check_output(cmd, shell=True)
            res = res.replace("{", "")
            res = res.replace("}", "")
            res = res.replace(", ", "\n")
            return "Antonym(s) for %s: %s" % (word, res)
        except BaseException:
            return 'Antonym not found.'

    @staticmethod
    def random():
        try:
            cmd = "shuf -n1 /usr/share/dictd/wn.index | cut -f1 "
            random_word = subprocess.check_output(cmd, shell=True)
            random_word = random_word[:-1]  # remove generated newline
            cmd = 'dict -d wn "%s" | tail -n 5' % random_word
            return subprocess.check_output(cmd, shell=True)
        except BaseException:
            return "Word not found."

    def run(self, action, word):

        action = action.upper()

        switcher = {
            'DEFINE': self.define(word),
            'SYNONYMS': self.synonym(word),
            'ANTONYMS': self.antonym(word),
            'RANDOM': self.random(),
        }

        func = switcher.get(action.upper(), self.instructions())
        if func:
            func = ' '.join(func.split())

        return func
