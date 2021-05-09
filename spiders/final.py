import scrapy
from scrapy.http import FormRequest,JsonRequest
import urllib
import json
from scrapy import Item, Field, Request, Spider
#from demo_project.items import JokeItem
#from scrapy.loader import ItemLoader

title_1 = []
object1 = []
desc_yes = []
title2 = []
desc_no = []
title = []
list_A = []
list_B = []
list_C = []
list_D = []
start_urls = []
debate_id = []
i = 0
k = 0
j = True
l = 0
m = 0

class DebateSpider(scrapy.Spider):
    name= 'final'

    start_urls = [
    'https://www.debate.org/opinions/?sort=popular'
    #taking the popular category URL
    ]

    def parse(self, response):

        global title1,k,start_urls,m,l


        if k == 0:
            # only for 1 time  
            
            for debate in response.xpath("/html/body/div[2]/div[4]/div[1]/div/div/ul/li"):
                title1 = debate.xpath("/html/body/div[2]/div[4]/div[1]/div/div/ul/li/span/p/a/@href").extract()
                # Extracting the values in popular catrgories so as to fetch data for top5 opinions

                object1 = response.xpath("/html/body/div[2]/div[4]/div[1]/div/div/ul/li/@did").extract()
                # for extracting the debator id
        # print("Yo yo yo")
        # data1 = object[1].upper()
        # print(data1)
                            
            for i in range(6):
                str = 'https://www.debate.org' + title1[i]
                print(str)
                start_urls.append(str)
                debate_id.append(object1[i].upper())
            print(start_urls)
                # creating the URLs for scrappying data

        if k == 0:
            print("zero wali value k ki value ha ",k)
            # next_page = start_urls[k]
            k = k + 1
            print("k ki value after plus 1 ",k)
        yield response.follow(start_urls[k-1], callback = self.parse)        

        if k != 0:
            #  for parsing data from each url
            print("first section k ki value ", k)
            print (response.xpath('//p//text()').get())
            #  for page1
            # parsing logic likna hai 
            #  page 2 ke data ko parse
            print("---------------")
            m = m+1

        if l != 1 :
            
            l = l + 1
            # load more arguments
            body_object = "{{debateId: \"{}\" , pageNumber: 2, itemsPerPage: 10, ysort: 5, nsort: 5 }}".format(debate_id[k-1])
            print(body_object)
            print("-************")
            yield scrapy.Request(url='https://www.debate.org/opinions/~services/opinions.asmx/GetDebateArgumentPage',
                                method='POST',
                                # body='{debateId: "DF5F0C8D-BDA6-4C05-9C50-07FCD527D8BE", pageNumber: 2, itemsPerPage: 10, ysort: 5, nsort: 5}',
                                body=body_object,
                                # body='{ pageNumber: 2, itemsPerPage: 10, ysort: 5, nsort: 5}',
                                headers={'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json; charset=UTF-8'},callback=self.parse)
        #  change page number in body to get diff pages data
            

        if ((k <= 5) and (m % 2 != 0)):
            # It will create new URL for diff opinions
            #  picard , black and agge aggee
            print("k ki value ha ",k)
            # next_page = start_urls[k]
            k = k + 1
            l = 0
        
        yield response.follow(start_urls[k-1], callback = self.parse)
            #Calling the 5 URL one by one

    # def parse_new(self, response):

    #     # print (response.text)
    #     # print (response.xpath('//body//p//text()').extract_first())
    #     print (response.xpath('//p//text()').extract_first())
    #     print("---------------")


