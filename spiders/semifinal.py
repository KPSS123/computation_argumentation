
import scrapy
from scrapy.http import FormRequest,JsonRequest
import urllib
import json
from scrapy import Item, Field, Request, Spider
import json
from lxml import etree
from scrapy.selector import Selector 
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup

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
pagenumber = 2

class DebateSpider(scrapy.Spider):
    name= 'second_link'

    # start_urls = [
    # 'https://www.debate.org/opinions/?sort=popular'
    # #taking the popular category URL
    # ]
    start_urls = [
    'https://www.debate.org/opinions/do-you-agree-with-the-black-lives-matter-movement-1'
    ]

    def parse(self, response):

        global title1,k,start_urls,m,l,list_A,list_B

        for debate in response.xpath("/html/body/div[2]/div[4]/div/div/div/div[4]/div[1]/ul/li"):
                # yes ke liye
                title_1 = debate.xpath('.//@href').extract()
                list_A.append(title_1)
                desc_yes = debate.xpath('p/text()').extract()
                list_B.append(desc_yes)
            
                # print (len(list_A), len(list_B))

            # load more arguments
            # body_object = "{{debateId: \"{}\" , pageNumber: 2, itemsPerPage: 10, ysort: 5, nsort: 5 }}".format(debate_id[k-1])
            # print(body_object)
            # print("-************")

        # response = HtmlResponse(url='https://www.debate.org/opinions/~services/opinions.asmx/GetDebateArgumentPage',
        #                     # method='POST',
        #                     body='{debateId: "DF5F0C8D-BDA6-4C05-9C50-07FCD527D8BE", pageNumber: "2", itemsPerPage: "10", ysort: "5", nsort: "5"}',
        #                     headers={'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json; charset=UTF-8'})
        
        # Selector(response = response).xpath('//span/text()').extract()

        yield scrapy.Request(url='https://www.debate.org/opinions/~services/opinions.asmx/GetDebateArgumentPage',
                            method='POST',
                            body='{debateId: "DF5F0C8D-BDA6-4C05-9C50-07FCD527D8BE", pageNumber: "2", itemsPerPage: "10", ysort: "5", nsort: "5"}',
                            headers={'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json; charset=UTF-8'},callback=self.parse_tag)
        #  change page number in body to get diff pages data


    def parse_tag(self, response):
		        #retrieve the tag name

        global pagenumber        
        data = ""
        print("lalalalalalalla1222222")
        data = json.loads(response.text)
        object_new = data['d']

        # print("**************")
        # print(object_new)
        # print("^^^^^^^^^^^^^^^^^^^^")

        x = object_new.split("ddo.split")

        # with open(object_new) as fp:
        soup_yes = BeautifulSoup(x[0], 'html.parser')
        soup_no = BeautifulSoup(x[1], 'html.parser')
        # soup = BeautifulSoup(object_new, "html.parser")

        for el_p in soup_yes.find_all("p"):
            print(el_p.get_text())

        # for el in soup_yes.find_all("h2"):
        #     print(el.get_text())

        # for el_no in soup_no.find_all("h2"):
        #     print(el_no.get_text())

        # if x[2] == 'needmore':
        if "needmore" in x[2]:

            pagenumber = pagenumber + 1
            body_object = "{{debateId: \"DF5F0C8D-BDA6-4C05-9C50-07FCD527D8BE\" , pageNumber: {}, itemsPerPage: 10, ysort: 5, nsort: 5 }}".format(pagenumber)
            print(body_object)
            yield scrapy.Request(url='https://www.debate.org/opinions/~services/opinions.asmx/GetDebateArgumentPage',
                                method='POST',
                                # body='{debateId: "DF5F0C8D-BDA6-4C05-9C50-07FCD527D8BE", pageNumber: \"{}\", itemsPerPage: "10", ysort: "5", nsort: "5"}'),
                                body=body_object,
                                headers={'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json; charset=UTF-8'},callback=self.parse_tag)
        
        # for el1 in soup.find_all("p"):
        #     print(el1.get_text())

        # print(response.meta)
        # tag_name = response.meta['depth']
        # print(tag_name)
        # #use css function to parse the html and find the tags that contains the quotes
        # quotes_html_tags = response.css('.col-md-8 .quote')
        # for quote_html_tag in quotes_html_tags:
        #     #retrieve the text of the tag
        #     quote_txt = quote_html_tag.css('.text ::text').get()
        #     #return a tag object
        #     # yield {"tag": tag_name, "text": quote_txt}	

    def parse_new(self, response):

        print("bhai new function hai ye")
        data = json.loads(response.text)
        # print(data)
        sel = Selector(xml_response)
        print(json.dumps(data, sort_keys=True, indent=4))

        for debate in response.xpath("/html/body/div[2]/div[4]/div/div/div/div[4]/div[1]/ul/li"):
            # yes ke liye
            print("Yes ki liye")
            title_1 = debate.xpath('.//@href').extract()
            list_A.append(title_1)
            desc_yes = debate.xpath('p/text()').extract()
            list_B.append(desc_yes)
        
            print (len(list_A), len(list_B))

        # res = ""
        # for key in data.keys() :
        #     res.append(test_dict[key])

        # print("The list of values is : " +  str(res))
        # selector = scrapy.Selector(text=data['response'], type="html")
        # print(selector)
        # obj = selector.xpath('//title/text()').extract()
        # htmlText = json.loads(response.text)['htmlinjson']
        # resultPage = etree.HTML(htmlText)
        # obj = selector.xpath('//title/text()').extract()
        # print (resultPage.xpath('/html/body/div[2]/div[4]/div/div/div/div[4]/div[2]/ul/li/h2/a/text()'))
        # print(obj)
