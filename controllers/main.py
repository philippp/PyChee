import os
import lib.RSS
import rfc822
from lib import controller

class main(controller.Controller):

  def index(self):
    stories = self.get_stories()
    return self.render("main",
                       stories = stories)
    
  def get_stories(self):
    c = lib.RSS.TrackingChannel()
    c.parse("http://100bedsforhaitiblog.blogspot.com/feeds/posts/default?alt=rss")
    news_items = []
    guids = []
    for item in c.items():
      news_item = {}
      try:
        for k, v in item[1][0].iteritems():
          news_item[k[1]] = v
        news_items.append(news_item)
      except Exception:
        pass
    news_items = sorted(news_items,
                        key = lambda s : rfc822.mktime_tz(rfc822.parsedate_tz(s['pubDate'])),
                        reverse=True)
    return news_items
