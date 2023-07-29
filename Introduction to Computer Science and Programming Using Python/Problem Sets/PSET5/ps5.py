# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: SpaceTimmi
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):

    def __init__(self, guid, title, description, link, pubdate):
        """
        Initializes all the attributes for NewsStory.
        guid, title, description, link and pubdate
        """
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        """
        Returns the Guid of the story/news.
        """
        return self.guid

    def get_title(self):
        """
        Returns the title of the story/news.
        """
        return self.title

    def get_description(self):
        """
        Returns the description of the story/news.
        """
        return self.description

    def get_link(self):
        """
        Returns the link to the story/news.
        """
        return self.link

    def get_pubdate(self):
        """
        Returns the publication date of the story/news.
        """
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        """
        Intializes PhraseTrigger class. It expects a phrase during intialization.
        """
        self.phrase = phrase.lower()


    def is_phrase_in(self, text):
        """
        Takes in one string argument text. It returns True
        if the whole phrase phrase is present in text, False otherwise.
        """
        # Parsing the text to remove all punctuations and multiple whitespaces
        punctuations, text_lst = string.punctuation, list(text.lower())
        remove_punctuations = list(map(lambda char: (" " if char in punctuations else char), text_lst))
        merge_text = "".join(remove_punctuations)
        parsed_text = " ".join(merge_text.split())

        found_index = parsed_text.find(self.phrase)
        if found_index > -1:
            # If the phrase match was found in the parsed text
            end_index = found_index + len(self.phrase)

            if len(parsed_text) == end_index or parsed_text[end_index] == " ":
                # If the match ends the text or is followed by a whitespace, indeed it is a match.
                return True
            else: return False

        else: return False


# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        """
        Intializes PhraseTrigger class.
        It expects a phrase during intialization.
        """
        PhraseTrigger.__init__(self, phrase)


    def evaluate(self, story):
        """
        Takes in a NewStory instance and returns True
        if an alert should be generated for the given news title, or False otherwise.
        """
        title = story.get_title()

        if self.is_phrase_in(title): return True
        else: return False



# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        """
        Intializes DescriptionTrigger class.
        It expects a phrase during intialization.
        """
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        """
        Takes in a NewStory instance and returns True
        if an alert should be generated for the given news description, or False otherwise.
        """
        desc = story.get_description()

        if self.is_phrase_in(desc): return True
        else: return False


# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    def __init__(self, time):
        """Initialize TimeTrigger with the date"""
        self.time = datetime.strptime(time, "%d %b %Y %H:%M:%S").replace(tzinfo=pytz.timezone("EST"))


# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def __init(self, date):
        """
        Takes in a NewStory instance and returns True
        if an alert should be generated for the given news
        if it was before the set time, or False otherwise.
        """
        TimeTrigger.__init__(self, date)

    def evaluate(self, story):
        """
        Takes in a NewStory instance and returns True
        if an alert should be generated for the given news
        if it was before the set time, or False otherwise.
        """
        pubdate = story.get_pubdate()
        if pubdate.tzinfo == None: pubdate = pubdate.replace(tzinfo=pytz.timezone("EST"))
        else: pubdate = pubdate.astimezone(pytz.timezone("EST"))

        #print(self.time.tzinfo, pubdate.tzinfo)

        if self.time > pubdate: return True
        else: return False


class AfterTrigger(TimeTrigger):
    def __init(self, date):
        """
        Takes in a NewStory instance and returns True
        if an alert should be generated for the given news
        if it was after the set time, or False otherwise.
        """
        TimeTrigger.__init__(self, date)

    def evaluate(self, story):
        """
        Takes in a NewStory instance and returns True
        if an alert should be generated for the given news description, or False otherwise.
        """
        pubdate = story.get_pubdate()
        if pubdate.tzinfo == None: pubdate = pubdate.replace(tzinfo=pytz.timezone("EST"))
        else: pubdate = pubdate.astimezone(pytz.timezone("EST"))

        if self.time < pubdate: return True
        else: return False


# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        """
        Initialize the NotTrigger class. It takes another trigger
        """
        self.trigger = trigger

    def evaluate(self, news_item):
        """
        Takes in a news_item, x, and evaluates x with the trigger, T,
        given to the class during construction. It inverts the return of calling T.evaluate(x)
        i.e. if T.evaluate(x) is True, NotTrigger will return False (the inverse of True).
        """
        result = self.trigger.evaluate(news_item)
        return not result

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger_one, trigger_two):
        """
        Initialize the AndTrigger class. It takes two trigger objects.
        """
        self.trigger_one = trigger_one
        self.trigger_two = trigger_two

    def evaluate(self, news_item):
        """
        Returns True if the two triggers given during construction of this class will
        fire for a given news.
        """
        result1 = self.trigger_one.evaluate(news_item)
        result2 = self.trigger_two.evaluate(news_item)
        return (result1 and result2)

# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger_one, trigger_two):
        """
        Initialize the OrTrigger Class. It takes two trigger objects.
        """
        self.trigger_one = trigger_one
        self.trigger_two = trigger_two

    def evaluate(self, news_item):
        """
        Returns True if one of the two triggers given during construction of the class
        will fire for a given news.
        """
        result1 = self.trigger_one.evaluate(news_item)
        result2 = self.trigger_two.evaluate(news_item)
        return (result1 or result2)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """

    valid_stories = list()

    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story): valid_stories.append(story)

    return valid_stories


#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    print(lines) # for now, print it so you see what it contains!



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line
        # triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

