import scrapy
from scrapy.http import FormRequest,JsonRequest
import urllib
import json
from scrapy import Item, Field, Request, Spider
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter



start_urls = []
debate_id = []
pro_argument = []
cons_argument = []
k = 0
scraped_info = {}
pro_title = []
cons_title = []
pagenumber = 2
graph_category = []
numberOfArguments = {}

class DebateSpider(scrapy.Spider):
    name= 'debate_crawler'

    start_urls = [
    'https://www.debate.org/opinions/?sort=popular'
    #taking the popular category URL
    ]

    def parse(self, response):

        global k,start_urls,pro_argument,cons_argument,scraped_info,pro_title,cons_title,pagenumber,graph_category,numberOfArguments
            
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
            yield response.follow(start_urls[k-1], callback = self.parse)   

        if k != 0:
            #  for parsing data from each url
            scraped_info = {}

            page_title = response.css('span.q-title::text').get()

            for annonce in response.css('.hasData'):
                strobject_yes = ""
                strobject_yes = "{{title : \"{}\" , body : {}}}".format(annonce.css('h2::text').extract(),annonce.css('p::text').extract())
                pro_argument.append(strobject_yes)

            for debate in response.xpath("/html/body/div[2]/div[4]/div/div/div/div[4]/div[2]/ul/li"):
                    # No
                strobject_No = ""
                strobject_No = "{{ title : \"{}\" , body : {}}}".format(debate.xpath('h2/a/text()').extract(),debate.xpath('p/text()').extract())
                cons_argument.append(strobject_No)
            
            if response.xpath("/html/body/div[2]/div[3]/a[3]/text()") is not None:
                main_category = response.xpath('/html/body/div[2]/div[3]/a[3]/text()').extract_first()

            # to call other pages
            body_object = "{{debateId: \"{}\" , pageNumber: {}, itemsPerPage: 10, ysort: 5, nsort: 5 }}".format(debate_id[k-1],pagenumber)
            
            yield scrapy.Request(url='https://www.debate.org/opinions/~services/opinions.asmx/GetDebateArgumentPage',
                            method='POST',
                            body=body_object,
                            headers={'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json; charset=UTF-8'},callback=self.parse_tag)

            scraped_info = {
            'topic' : page_title, 
            'category': main_category,
            'pro_arguments': pro_argument,
            'con_arguments': cons_argument
            }

  
            if k > 1:
                graph_category.append(main_category)
                count = len(pro_argument) + len(cons_argument)
                numberOfArguments[page_title] = count  
                count = 0
                # yield scraped_info
            
        if k <= 4:
            # It will create new URL for diff opinions
            k = k + 1
            yield response.follow(start_urls[k-1], callback = self.parse)
            # Calling the 5 URL one by one

        else:

            print("printing histogram _____________")
            my_dict = dict(Counter(graph_category))
            key_list = list(my_dict.keys())
            print(key_list)
            y_pos = np.arange(len(key_list))
            val_list = list(my_dict.values())
            print(val_list)

            plt.bar(y_pos, val_list, align='center', alpha=0.5)
            plt.xticks(y_pos, key_list)
            plt.ylabel('Usage')
            plt.title('category_plots')
            plt.savefig("category_plots.png")

            # second histogram creation

            print("printing histogram ((((((((((((")
            my_dict = dict(Counter(numberOfArguments))

            key_list = list(my_dict.keys())
            y_pos = np.arange(len(key_list))
            val_list = list(my_dict.values())

            plt.bar(y_pos, val_list, align='center', alpha=0.5)
            plt.xticks(rotation=90)
            plt.xticks(y_pos, key_list)
            plt.ylabel('Usage')
            plt.title('category_plots_2')
            # plt.show()
            plt.savefig("category_plots_2.png")


    def parse_tag(self, response):
		        #retrieve the tag name

        global pagenumber,pro_title,cons_title,pagenumber
        pro_title = []
        cons_title = []

        data = ""
        data = json.loads(response.text)
        object_new = data['d']

        x = object_new.split("ddo.split")

        # with open(object_new) as fp:
        soup_yes = BeautifulSoup(x[0], 'html.parser')
        soup_no = BeautifulSoup(x[1], 'html.parser')
        # soup = BeautifulSoup(object_new, "html.parser")
        for el_yes in soup_yes.find_all("h2"):
            pro_title.append(el_yes.get_text())

        for el_no in soup_no.find_all("h2"):
            cons_title.append(el_no.get_text())

        for el_p_yes in soup_yes.find_all("p"):
            strobject_yes = "{{title : \"{}\" , body : {}}}".format(pro_title,el_p_yes.get_text())
            pro_argument.append(strobject_yes)

        for el_p_no in soup_yes.find_all("p"):
            strobject_No = "{{ title : \"{}\" , body : {}}}".format(cons_title,el_p_no.get_text())
            cons_argument.append(strobject_No)

        if "needmore" in x[2]:

            pagenumber = pagenumber + 1
            body_object = "{{debateId: \"{}\" , pageNumber: {}, itemsPerPage: 10, ysort: 5, nsort: 5 }}".format(debate_id[k-1],pagenumber)
            yield scrapy.Request(url='https://www.debate.org/opinions/~services/opinions.asmx/GetDebateArgumentPage',
                                method='POST',
                                body=body_object,
                                headers={'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json; charset=UTF-8'},callback=self.parse_tag)
        else:
            pagenumber = 2
