import feedparser
import db
import hashlib
from time import strftime

class Fetch():

    # Initialze the Fetch class with the feed url
    #   additionally, parse out the URL and get a parsed feed
    def __init__(self,feedURL=None):

        if feedURL == None or len(feedURL.strip()) == 0:
            raise KeyError('Please supply a feedURL')

        self.feedURL = feedURL
        self.parsedFeed = feedparser.parse(feedURL)

    # Return information about the feed itself
    def get_feed_details(self):

        thisFeed = self.parsedFeed['feed']

        # Declare an object
        obj = {}

        # If the required keys exist, add them
        obj['feed_url'] = self.feedURL

        obj['title'] = obj['description'] = obj['link'] = None

        if thisFeed.has_key('title'):
            obj['title'] = thisFeed['title']

        if thisFeed.has_key('subtitle'):
            obj['description'] = thisFeed['subtitle']

        if thisFeed.has_key('link'):
            obj['link'] = thisFeed['link']

        # Return the object
        return obj


    # Return a list of dictionaries of the entries in the feed
    def get_entries(self):

        # declare an empty entities list
        entries = []

        # TODO: create feed if it doesn't exist
        feed_id = db.get_feed_id(self.feedURL)

        # go through the list of entities present in the feed
        for entry in self.parsedFeed['entries']:

            # Declare an empty dict 
            obj = {}

            obj['feed_id'] = feed_id

            obj['title'] = obj['description'] = obj['link'] = obj['guid'] = obj['pubdate'] = None

            # If the keys exist, drop them in to the object
            if entry.has_key('title'):
                obj['title'] = entry['title']

            if entry.has_key('description'):
                obj['description'] = entry['description']

            if entry.has_key('link'):
                obj['link'] = entry['link']

            if entry.has_key('published'):
                # convert the datetime to mysql format
                pub_datetime = entry['published_parsed']
                obj['pubdate'] = strftime('%Y-%m-%d %H:%M:%S',pub_datetime)

            # guid is a part of the newer rss specification, it doesn't exists we'll just use a link
            if entry.has_key('guid'):
                obj['guid'] = entry['guid']
            else:
                obj['guid'] = obj['link']

            # the hash of the guid is used to check for duplicates
            obj['guid_hash'] = hashlib.md5(obj['guid']).hexdigest()

            # append the created object to the list of entries
            entries.append(obj)

        # return the entries
        return entries
