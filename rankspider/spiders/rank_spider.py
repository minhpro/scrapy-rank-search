import scrapy
from ..items import RankItem

queryString = "https://www.google.co.jp/search?q={keyword}&start={start}&num={num}"

CANDIDATE_PATHS = ['/html/body/div/div/div/div[1]/a', '/html/body/div/div/div[1]/a', '/html/body/div/div/div/div/div[1]/a'] 


class GoogleRankSpider(scrapy.Spider):
    name = 'GoogleRankSpider'
    
    def __init__(self, id, keyword, target_site, start, num, *args, **kwargs):
        super(GoogleRankSpider, self).__init__(*args, **kwargs)
        self.id = id
        self.keyword = keyword
        self.target_site = target_site
        self.start = start
        self.start_urls = [queryString.format(keyword = keyword, start = start, num = num)]


    def parse(self, response):
        # filename = 'response.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        i = int(self.start)
        items = []
        for path in CANDIDATE_PATHS:
            items = response.xpath(path)
            if items and len(items) > 0:
                break

        if not items or len(items) == 0:
            yield RankItem(id = self.id, error='page error', rank=0, url='')
    
        for item in items:
            link = item.xpath("@href").get()
            if "url?q=" in link:
                link = link.split("/url?q=", 1)[1]
            link = link.split("&")[0]
            if link is not None:
                i += 1
                yield RankItem(id=self.id, error='', rank=i, url= link)
