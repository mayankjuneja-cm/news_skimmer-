import xml.etree.ElementTree as ET
import requests
from datetime import datetime, timedelta

# import nltk
# nltk.download('vader_lexicon')
# from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA


# sia = SIA()
NEWS = []

class GoogleNews():
    def __init__(self,
        title=None,
        link=None,
        guid=None,
        pubDate=None,
        description=None,
        source=None
    ):
        self.title = title
        self.link = link
        self.guid = guid
        self.pubDate = pubDate
        self.description = description
        self.source = source
        self.polarity = 0

    def cal_pol_score(self):
        # self.polarity = sia.polarity_scores(self.title)["compound"]
        self.polarity = 0.1

    def get_from_xml(self, xml_parser):
        self.title = xml_parser.find('title').text
        self.link = xml_parser.find('link').text
        self.guid = xml_parser.find('guid').text
        self.pubDate = xml_parser.find('pubDate').text
        self.description = xml_parser.find('description').text
        self.source = xml_parser.find('source').text
        self.pubDate = datetime.strptime(xml_parser.find('pubDate').text, '%a, %d %b %Y %H:%M:%S GMT')

    def __repr__(self):
        return f"({self.polarity}){self.title} by {self.source}"

class NewsOfIntreast:
    def __init__(self, topic, loc, latest=None):
        topic = topic.replace(" ", "%20")
        self.URL = "https://news.google.com/rss/search?q={}&hl=en-{}&gl={}&ceid={}:en".format(topic, loc, loc, loc)
        print(self.URL)
        self.news = []

        self.latest = latest

        self.fetch_news()
        self.segregate()

    def fetch_news(self, latest=None):
        response = requests.get(self.URL)

        content = ET.fromstring(response.content)

        for i in content.iter('item'):
            if (
                self.latest and (
                    datetime.strptime(i.find('pubDate').text, '%a, %d %b %Y %H:%M:%S GMT') 
                    < self.latest
                )
            ):
                continue   
            gn = GoogleNews()
            gn.get_from_xml(i)
            gn.cal_pol_score()

            self.news.append(gn)

    def segregate(self):
        positive = []
        negative = []
        neutral = []

        for new in self.news:
            if new.polarity < 0:
                negative.append(new)
            elif new.polarity > 0:
                positive.append(new)
            else:
                neutral.append(new)

        self.group = {
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
        }

# noi = NewsOfIntreast("cement", "US", datetime.today() - timedelta(days=1))