import scrapy
from demo_project.items import JokeItem
from scrapy.loader import ItemLoader

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
start_urls = []
k = 0


# This file can crawl data from 5 popular categories dynamically.

class DebateSpider(scrapy.Spider):
    name= 'debate1'

    start_urls = [
    'https://www.debate.org/opinions/?sort=popular'
    # 'https://www.debate.org/opinions/do-you-agree-with-the-black-lives-matter-movement-1'
    ]
    
    # has_next = response.css('.load-more').extract()
    
    # if has_next:
    #     next_page = response.meta.get('next_page', 1) + 1
    #     url = response.urljoin(response.css('script').re_first("'(\?searchId.*page=)'") + str(next_page))
    
    #     yield Request(url , meta={'next_page': next_page})
    

    def parse(self, response):
        #parse pages here.

        # if response.xpath('//div[@class="arguments args-yes"]').get() is not None:
        # for debate in response.xpath('//*[@id="yes-arguments"]') :    

        # for getting dynamic pages
        global title1,k,start_urls
        for debate in response.xpath("/html/body/div[2]/div[4]/div[1]/div/div/ul/li"):
            title1 = debate.xpath("/html/body/div[2]/div[4]/div[1]/div/div/ul/li/span/p/a/@href").extract()
       
        if k == 0:
            for i in range(6):
                str = 'https://www.debate.org' + title1[i]
                start_urls.append(str)
        print(start_urls)

        #   for i in range(2):

        if k <= 5:
            next_page = start_urls[k]
            print("bhai k ki value ha ",k)
            yield response.follow(next_page, callback = self.parse)
        k = k + 1
        


        if k!=0:
            for debate in response.xpath("/html/body/div[2]/div[4]/div/div/div/div[4]/div[1]/ul/li"):
                
                # yes ke liye
                # print(response.xpath('//*[@id="yes-arguments"]').)
                # title1 = []
                # print("*******************")
                title1 = debate.xpath('//div[@class="arguments args-yes"]/ul/li/h2/a/text()').extract()
                # if title1 is None:
                #     print("Bhai data hi nhi hai isme ")
                title21 = debate.xpath('//div[@class="arguments args-yes"]/ul/li/h2/text()').extract()
                # print(title21)
                desc_yes = debate.xpath('p/text()').extract()
                list_B.append(desc_yes)
                # print(title1)
                
                # print(len(list_B))
                print("*******************")

        # for href in response.xpath('//*[@id="col-wi"]/div/div[5]/a/@href'):
        #     yield response.follow(href, self.parse)

            # //*[@id="col-wi"]/div/div[5]

            




        #     title_1 = debate.xpath('.//a/@href').extract()
        #     # title_1 = debate.xpath('/html/body[@class="debate vsc-initialized"]/div[@id='pg']/div[@id='pg-wi2']/div[@id='col-w']/div[@id='col-wi']/div[@class='pg-body home-layout cf']/div[@id="debate"]/div[@id="yes-arguments"]/ul/li[@class='hasData'][1]/h2/a').extract_first()
        #     list_A.append(title_1)
        #     desc_yes = debate.xpath('p/text()').extract()
        #     list_B.append(desc_yes)
        
        # print (len(list_A), len(list_B))
        
        # print("---------------")
            
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

        # # for debate1 in zip(title_1,desc_yes,desc_no):
        # for i in range(2):
        #     # print("Hey ya")
        #     scraped_info = {
        #     'title1' : list_A[i],
        #     'desc_yes' : list_B[i],
        #     'desc_no' : list_D[i]
        #     }
        
        #     yield scraped_info

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

                # def parse(self, response):
        # all_books = response.xpath('//article[@class="product_pod"]')
        
        # all_books= response.xpath("/html/body[@class='debate vsc-initialized']/div[@id='pg']/div[@id='pg-wi2']/div[@id='col-w']/div[@id='col-wi']/div[@class='pg-body home-layout cf']/div[@class='debate-more-holder']/a[@class='debate-more-btn']").extract_first()

        # for book in all_books:
        #     print("lets see")
        #     book_url = book.xpath("/html/body[@class='debate vsc-initialized']/div[@id='pg']/div[@id='pg-wi2']/div[@id='col-w']/div[@id='col-wi']/div[@class='pg-body home-layout cf']/div[@class='debate-more-holder']/a[@class='debate-more-btn']").extract_first()
        #     yield scrapy.Request(book_url, callback=self.parse_book)
