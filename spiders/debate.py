import scrapy
from demo_project.items import JokeItem
from scrapy.loader import ItemLoader

class DebateSpider(scrapy.Spider):
    name= 'debate'

    start_urls = [
    'https://www.debate.org/opinions/do-you-agree-with-the-black-lives-matter-movement-1'
    ]

    def parse(self, response):
        # i = 0
        # for debate in response.xpath("/html/body/div[2]/div[4]/div/div/div/div[4]/div[1]"):
            # //*[@id="yes-arguments"]
        # for debate in response.xpath("/html/body/div[2]/div[4]/div/div/div/div[4]/div[1]/ul/li"):
        # for debate in reponse.xpath("/html/body/div[2]/div[4]/div/div/div/div[4]")
            
        for debate in response.xpath("/html/body/div[2]/div[4]/div/div/div/div[4]/div[1]/ul/li"):
            # yes ke liye
            # name = debate.xpath("a/text()").get
            # link = debate.xpath(".//@href").get
            title = debate.xpath('a/@href').extract()
            # link = debate.xpath('a/@href').extract()
            desc = debate.xpath('p/text()').extract()
            print (title, desc )
        
        print("---------------")
            
        for debate in response.xpath("/html/body/div[2]/div[4]/div/div/div/div[4]/div[2]/ul/li"):
            # No ke liye
            title2 = debate.xpath('a/@href').extract()
            # link = debate.xpath('a/@href').extract()
            desc2 = debate.xpath('p/text()').extract()

                # /html/body/div[2]/div[4]/div/div/div/div[4]/div[1]/ul/li[1]/h2

            print (title2, desc2 )

            yield {
                # 'pro_Newtext': debate.xpath("/html/body/div[2]/div[4]/div/div/div/div[4]/div[1]/ul/li[%d]/p"%i).extr
                # 'title':title,
                # 'desc':desc,
                'title2':title2,
                'desc2':desc2,
            }

        next_page= response.xpath("/html/body/div[2]/div[4]/div/div/div/div[5]/a/@href").extract_first()
        if next_page is not None:
            # print("kaise ho beta")
            next_page_link= response.urljoin(next_page) 
            yield scrapy. Request(url=next_page_link, callback=self.parse)