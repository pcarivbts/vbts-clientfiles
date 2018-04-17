"""
Copyright (c) 2015-present, Philippine-California Advanced Research Institutes-
The Village Base Station Project (PCARI-VBTS). All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import tweepy


class Twits(object):
    name = "pcaritwits"
    version = "1.0"
    author = "pcari.vbts@gmail.com"

    def __init__(
            self,
            name='TWITTER',
            keyword='TWEET',
            number='200',
            args=None):

        #         TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
        #         TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
        #
        #         TWITTER_TOKEN = os.environ.get('TWITTER_TOKEN')
        #         TWITTER_TOKEN_SECRET = os.environ.get('TWITTER_TOKEN_SECRET')

        TWITTER_CONSUMER_KEY = args['TWITTER_CONSUMER_KEY']
        TWITTER_CONSUMER_SECRET = args['TWITTER_CONSUMER_SECRET']

        TWITTER_TOKEN = args['TWITTER_TOKEN']
        TWITTER_TOKEN_SECRET = args['TWITTER_TOKEN_SECRET']

        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY,
                                   TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_TOKEN,
                              TWITTER_TOKEN_SECRET)

        self.api = tweepy.API(auth, timeout=60)
        self.name = name
        self.keyword = keyword
        self.number = number
        self.locations = args['locations']
        self.max_number_of_tweets = int(args['Shos'])
        self.include_rts = args['include_rts']

    @staticmethod
    def clean_string(text):

        text = text.encode('ascii', errors='ignore').replace('\n', '\\n')
        return text

    def instructions(self, action=None):
        if action == "TRENDING":
            instructions = "Text %s TRENDING <location> and send to %s.\nLocations: %s" % (
                self.keyword, self.number, '|'.join(self.locations.iterkeys()))
        elif action == "HANDLE":
            instructions = "Text %s HANDLE <twitter_account> and send to %s." \
                           " Example: %s HANDLE cnn" % \
                           (self.keyword, self.number, self.keyword)
        elif action == "SEARCH":
            instructions = "Text %s SEARCH <keyword> and send to %s." \
                           " Example: %s HANDLE du30" % \
                           (self.keyword, self.number, self.keyword)
        else:
            instructions = "You entered an invalid keyword. " \
                           "To use %s app, text %s HANDLE <screen_name> or " \
                           "%s SEARCH keyword or %s TRENDING location then send " \
                           "to %s." % \
                           (self.name, self.keyword, self.keyword,
                            self.keyword, self.number)

        return instructions

    def tweets_by_keyword(self, keyword):
        if keyword:
            try:
                tweets = self.api.search(q=keyword)
                result = '\n'.join(["%s: %s" % (tweet.author.screen_name, tweet.text)
                                    for tweet in tweets][0:self.max_number_of_tweets])
                return self.clean_string(result)

            except tweepy.TweepError as e:
                return self.instructions()
        else:
            return self.instructions()

    def tweets_by_handle(self, handle):
        if handle:
            try:
                tweets = self.api.user_timeline(
                    screen_name=handle,
                    max_number_of_tweets=self.max_number_of_tweets,
                    include_rts=True)
                result = '\n'.join(["%s: %s" % (tweet.author.screen_name, tweet.text)
                                    for tweet in tweets])
                return self.clean_string(result)

            except tweepy.TweepError as e:
                return self.instructions()
        else:
            return self.instructions()

    def trending_by_location(self, woeidkey):
        if woeidkey and woeidkey in self.locations.iterkeys():
            try:
                trends1 = self.api.trends_place(
                    self.locations[woeidkey])[0]["trends"]
                trends = [trend['name'] for trend in trends1]
                tweets = trends[0:self.max_number_of_tweets]
                result = "%s TRENDS:\n" % woeidkey
                result += '\n'.join(tweets)
                return self.clean_string(result)

            except tweepy.TweepError as e:
                print e
                return self.instructions("TRENDING")
        else:
            return self.instructions("TRENDING")

    def run(self, action, param):
        action = action.upper()
        param = param.upper()

        if action == 'HANDLE':
            return self.tweets_by_handle(param)

        elif action == 'TRENDING':
            return self.trending_by_location(param)

        elif action == 'SEARCH':
            return self.tweets_by_keyword(param)

        else:
            return self.instructions(action)
