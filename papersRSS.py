from utils.base import *
import sys
from bs4 import BeautifulSoup


class PapersWithCode(RSSGenerator):
    def __init__(self, save='feeds/paperswithcode.xml', url=r'https://paperswithcode.com/', frequency=1, rssname='PapersWithCode', translator=False
                 ):
        '''
        :param save: the path with the .xml file save
        :param frequency: the fresh frequency. 1 means 1fresh/day
        :param rssname: the feed name
        :param translator: if need translator(now not using)
        :param url: the web base url
        '''
        super(PapersWithCode, self).__init__(rssname=rssname, url=url, save=save, frequency=frequency,description=None)
        self.translator = translator

    def generate(self):
        while 1:
            item = self.rule()
            try:
                rss = PyRSS2Gen.RSS2(
                    title=self.rssname,
                    link=self.url,
                    description=self.description,
                    lastBuildDate=datetime.datetime.now(),
                    items=item
                )
            except KeyError or AttributeError:
                self.setdetail(rssname=self.url, description=self.url)
                continue
            with open(self.savepath, 'w+', encoding='utf-8') as file:
                rss.write_xml(file, encoding="utf-8")
            print(f'{datetime.datetime.now()} has freshed!' )
            time.sleep(timeofday/1)

    def __analyseresponse(self):
        r = requests.get(self.url)
        bs = BeautifulSoup(r.text, 'html.parser')
        contents = bs.findAll(name="div", attrs={'class': 'row infinite-item item'})
        return contents

    def __getimgurl(self, imgcontent):
        ipat = re.compile('(?<=url).*?(?=;)')
        imgcontent = imgcontent.find(attrs={'class': 'col-lg-3 item-image-col'})
        url = re.search(ipat, str(imgcontent))
        url = eval(url.group(0))
        return os.path.join(self.url, url)

    def __gettitle(self, textcontent):
        texts = textcontent.find(attrs={'class': 'col-lg-9 item-content'})
        title = texts.h1
        return title.text

    def __getoutline(self, textcontent):
        texts = textcontent.find(attrs={'class': 'col-lg-9 item-content'})
        outline = texts.find(attrs={'class': 'item-strip-abstract'})
        return outline.text

    def __getconurl(self, textcontent):
        textcontent = textcontent.find(attrs={'class': 'col-lg-3 item-image-col'})
        conurl = textcontent.a['href']
        return conurl

    def __processtime(self, textcontent):
        texts = textcontent.find(attrs={'class': 'col-lg-9 item-content'})
        try :
            publishtime = texts.find(name='span', attrs={'class': 'author-name-text item-date-pub'}).text
            day, month, year = publishtime.split(' ')
            return datetime.datetime(day=int(day), month=datemap[month], year=int(year))
        except:
            publishtime = datetime.datetime.now()
            return publishtime



    def rule(self):
        '''
        the rss rule based on the web you feed .
        :return: a list of the RSS object's paramas items.
        '''
        items = []
        contents = self.__analyseresponse()
        for i in contents:
            imgurl = os.path.join(self.url, self.__getimgurl(i))
            title = self.__gettitle(i)
            outline = self.__getoutline(i)
            contenturl = os.path.join(self.url, self.__getconurl(i))
            date = self.__processtime(i)
            items.append(
                PyRSS2Gen.RSSItem(
                    title=title,
                    link=contenturl,
                    # image = imgurl,
                    description=outline,
                    guid=PyRSS2Gen.Guid(contenturl),
                    pubDate=date))
        return items

if __name__ == '__main__':
    test = PapersWithCode()
    test.generate()
