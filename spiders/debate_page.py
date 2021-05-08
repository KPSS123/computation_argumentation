import scrapy
# from demo_project.items import JokeItem
# from scrapy.loader import ItemLoader
from scrapy.http import JsonRequest

title_1 = []
desc_yes = []
title2 = []
desc_no = []
title = []
list_A = []
list_B = []
list_C = []
list_D = []
list_E = []


class DebateSpider(scrapy.Spider):
    name= 'debate_page'

    start_urls = [
    'https://www.debate.org/opinions/do-you-agree-with-the-black-lives-matter-movement-1'
    ]
    

    def parse(self, response):

        for debate in response.xpath("/html/body/div[2]/div[4]/div/div/div/div[4]/div[1]/ul/li"):
            # yes ke liye
            title_1 = debate.xpath('.//@href').extract()
            list_A.append(title_1)
            desc_yes = debate.xpath('p/text()').extract()
            list_B.append(desc_yes)
        
        print (len(list_A), len(list_B))
        
        print("---------------")
            
        # for debate1 in response.xpath("/html/body/div[2]/div[4]/div/div/div/div[4]/div[2]/ul/li"):
        #     # No ke liye
        #     title2 = debate1.xpath('.//@href').extract()
        #     list_C.append(title2)
        #     desc_no = debate1.xpath('p/text()').extract()
        #     list_D.append(desc_no)
        #     title = debate1.xpath('a/text()').extract()
        #     list_E.append(title)
        #     # print (len(title2), len(desc_no), len(title))
        
        # print (len(list_C), len(list_D), len(list_E))

        # print("---------------*****")

        # for debate1 in zip(title_1,desc_yes,desc_no):
        for i in range(2):
            # print("Hey ya")
            scraped_info = {
            'title1' : list_A[i],
            'desc_yes' : list_B[i]
            # 'desc_no' : list_D[i]
            }
        
            yield scraped_info

        # next_page= response.xpath("/html/body/div[2]/div[4]/div/div/div/div[5]/a/@href").extract_first()
        # print(next_page)
        # if next_page is not None:
        #     print("kaise ho beta")
        #     next_page_link= response.urljoin(next_page) 
        #     yield scrapy. Request(url=next_page_link, callback=self.parse)


        # if response.xpath("//a/@rel='next'\").get() == '1'):
        #     print("next page mkj")
        #     next_page = response.xpath('//a[@rel='next']/@href').get()
        #     yield response.follow(url=next_page , callback=self.parse) 

        data = {
            # 'debateId': 'DF5F0C8D-BDA6-4C05-9C50-07FCD527D8BE',
            'page': '5',
        }
        yield JsonRequest(url='https://www.debate.org/opinions/do-you-agree-with-the-black-lives-matter-movement-1', data=data)
