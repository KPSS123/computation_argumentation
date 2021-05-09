import scrapy
from scrapy.http import FormRequest,JsonRequest
import urllib
import json
from scrapy import Item, Field, Request, Spider
#from demo_project.items import JokeItem
#from scrapy.loader import ItemLoader

start_urls = []
debate_id = []
pro_argument = []
cons_argument = []
k = 0
scraped_info = {}

class DebateSpider(scrapy.Spider):
    name= 'pretext'

    start_urls = [
    'https://www.debate.org/opinions/?sort=popular'
    #taking the popular category URL
    ]

    def parse(self, response):

        global k,start_urls,pro_argument,cons_argument,scraped_info
            
        if k == 0:
            # only for 1 time  
            
            for debate in response.xpath("/html/body/div[2]/div[4]/div[1]/div/div/ul/li"):
                title1 = debate.xpath("/html/body/div[2]/div[4]/div[1]/div/div/ul/li/span/p/a/@href").extract()
                # Extracting the values in popular catrgories so as to fetch data for top5 opinions
                object1 = response.xpath("/html/body/div[2]/div[4]/div[1]/div/div/ul/li/@did").extract()
                            
            for i in range(6):
                str = 'https://www.debate.org' + title1[i]
                # print(str)
                start_urls.append(str)
                debate_id.append(object1[i].upper())
                # creating the URLs for scrappying data
            
            k = k + 1
            print("k ki value after plus 1 ",k)
            yield response.follow(start_urls[k-1], callback = self.parse)   

        if k != 0:
            #  for parsing data from each url
            scraped_info = {}
            print("first section k ki value ", k)

            page_title = response.css('span.q-title::text').get()

            for annonce in response.css('.hasData'):
                strobject_yes = ""
                strobject_yes = "{{title : \"{}\" , body : {}}}".format(annonce.css('h2::text').extract_first(),annonce.css('p::text').extract_first())
                pro_argument.append(strobject_yes)

            for debate in response.xpath("/html/body/div[2]/div[4]/div/div/div/div[4]/div[2]/ul/li"):
                    # No
                strobject_No = ""
                strobject_No = "{{ title : \"{}\" , body : {}}}".format(debate.xpath('h2/a/text()').extract_first(),debate.xpath('p/text()').extract_first())
                cons_argument.append(strobject_No)
            
            if response.xpath("/html/body/div[2]/div[3]/a[3]/text()") is not None:
                main_category = response.xpath('/html/body/div[2]/div[3]/a[3]/text()').extract_first()

            scraped_info = {
            'topic' : page_title, 
            'category': main_category,
            'pro_arguments': pro_argument,
            'con_arguments': cons_argument
            }
            
            if k > 1:
                yield scraped_info
            
        if k <= 4:
            # It will create new URL for diff opinions
            k = k + 1
            yield response.follow(start_urls[k-1], callback = self.parse)
            # Calling the 5 URL one by one


