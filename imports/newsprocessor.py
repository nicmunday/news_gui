#!/usr/bin/env python3
import feedparser
from datetime import datetime, date
import time

class NewsProcessor:
    def __init__(self):
        self.feed = feedparser.parse(
            "http://feeds.bbci.co.uk/news/rss.xml")
        self.stories = self.feed.entries

        self.now = datetime.now()

        self.today = datetime.combine(date.today(),
                                      datetime.min.time())

        now_str = self.now.\
            strftime("Now: %a %d %b %H:%M  |||  Pub: ")
        
        self.final_string = now_str + datetime.\
            fromtimestamp(time.mktime(
            self.feed.feed.updated_parsed)).\
            strftime("%a %d %b %H:%M")


    def all_stories(self):
        result_stories = []
        for x in range(len(self.stories)):
            entry = f"{x + 1}: {self.stories[x]['title']}"
            pub = datetime.fromtimestamp(time.mktime(
                self.stories[x]['published_parsed']))
            summm = self.stories[x].get("summary_detail", {}).get(
                "value", "")
            result_stories.append({"story": entry, "pub_string":
                f"Pub: {pub.strftime('%a %d %b  %H:%M')} \n "
                f"======","pub": pub,"link": self.stories[x].
                                  link,"summary": summm})

        result_stories.reverse()
        return result_stories

    def stories_in_range(self, start, end):
        result_stories = []
        if start <= end:
            for num in range(end-1, start-2, -1):
                story = f"{num+1}: {self.stories[num]['title']}"
                pub = datetime.fromtimestamp(time.mktime(
                    self.stories[num]['published_parsed']))
                summ = self.stories[num].get(
                    "summary_detail", {}).get("value", "")
                
                result_stories.append(
                    {"story": story, "pub_string":
                        f"Pub: {pub.strftime('%a %d %b  %H:%M')} "
                        f"\n ======","pub":pub, "link":
                        self.stories[num].link, "summary": summ})
            return result_stories

        else:
            return self.all_stories()


    def stories_before(self, compare_date, storylist):
        if not storylist:
            storylist = self.all_stories()
        resultlist = [story for story in storylist
                      if story['pub'] < compare_date]
        return resultlist



    def stories_after(self, compare_date, storylist):
        if not storylist:
            storylist = self.all_stories()
        resultlist = [story for story in storylist
                      if story['pub'] > compare_date]
        return resultlist

    def new_stories(self, storylist):
        last_accessed = False
        if not storylist:
            storylist = self.all_stories()

        try:
            with open(
                    "imports/text_files/"
                    "newsaccessed.txt") as reader:
                line = reader.readline().strip()
                if line != "":
                   last_accessed = datetime.\
                        fromisoformat(line)

        except FileNotFoundError:
            with open(
                    "imports/text_files/"
                    "newsaccessed.txt", "w") as writer:
                writer.write(str(datetime.now()))

        if not last_accessed:
            return storylist
        else:
            resultlist = [story for story in storylist
                          if story['pub'] > last_accessed]
            return resultlist

    def today_stories(self, storylist):
        if not storylist:
            storylist = self.all_stories()
        return self.stories_after(self.today, storylist)

    def not_today_stories(self, storylist):
        if not storylist:
            storylist = self.all_stories()
        return self.stories_before(self.today, storylist)
