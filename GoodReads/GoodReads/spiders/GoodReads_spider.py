from scrapy import Spider, Request
from GoodReads.items import GoodreadsItem
import re
from datetime import datetime

class GoodReadsSpider(Spider):
    name = 'GoodReads_spider'
    allowed_urls = ['https://www.goodreads.com/']
    #start_urls = ['https://www.goodreads.com/group/topic/1-books-literature']
    start_urls = ['https://www.goodreads.com/group/show_tag/bookclub']

    def parse(self, response):
        #rows = response.xpath('//div[@class="elementList"]')
        result_urls = ['https://www.goodreads.com/group/show_tag/bookclub?page={}'.format(x) for x in range(1,100)]
        #actual range is 15048
        #for page_n of bookclub_groups
            #for each_group of page_n
                 #extract desired_items
        #for i in range(0, len(rows)+1):
            #x = rows[i].xpath('//span[@class="greyText"]').extract()[i]
            #member_cnt = int(re.findall('\d+', x)[0])
            #Group_Name2.append(rows[i].xpath('//a[@class="groupName"]/text()').extract()[i])
            #last_activity = re.findall('(Last Activity )(.*)', x)[0][1]
                #if re.findall('20..',last_activity) == []:
                #    year = 2018
                #else:
                #    year = int(re.findall('20..',last_activity)[0])

                #item = GoodreadsItem()
                #item['Group_Name'] = Group_Name
                #item['member_cnt'] = member_cnt
                #item['last_activity'] = last_activity
                #item['year'] = year
                #yield item

        for url in result_urls:
            yield Request(url=url, callback=self.parse_result_page)

        #meta={'Group_Name': Group_Name, 'member_cnt': member_cnt, 'last_activity': last_activity, 'year': year}


    def parse_result_page(self, response):
        detail_urls = response.xpath('//div[@class="elementList"]/a/@href').extract()
        detail_urls = ['https://www.goodreads.com' + link for link in detail_urls] 
        #Group_Name2 = response.meta['Group_Name2']
        '''Group_Name = response.meta['Group_Name']
        member_cnt = response.meta['member_cnt']
        last_activity = response.meta['last_activity']
        year = response.meta['year']

        item = GoodreadsItem()
        item['Group_Name'] = Group_Name
        item['member_cnt'] = member_cnt
        item['last_activity'] = last_activity
        item['year'] = year
        yield item'''
        for url in detail_urls:
            yield Request(url=url, callback=self.parse_detail_page)

          #  print(len(detail_urls))
           # print('=' * 50)
        
    def parse_detail_page(self, response):
        #Group_Name2 = response.meta['Group_Name2']
        member_cnt_text = response.xpath('/html/body/div[2]/div[3]/div[1]/div[2]').extract_first()
        member_cnt = int(re.findall("Members \((.+)\)",member_cnt_text)[0])
        if member_cnt == 1:
            return
        else:
            Group_Name = response.xpath('/html/body/div[2]/div[3]/div[1]/div[2]/h1/text()').extract_first()
            details = response.xpath('//*[@id="groupBox"]').extract_first()
            group_details = re.findall('<div class="infoBoxRowTitle">(.*)</div>',details)
            xpath = ""
            location = "NA"
            group_type = "NA"
            tags = ""
            category = ""
            for i in range(0,len(group_details)):
                if group_details[i] == 'location':
                    xpath = '//*[@id="groupBox"]/div[' + str(2*(i+1)) + ']/text()'
                    location = response.xpath(xpath).extract()[0].strip()
                if group_details[i] == 'group type':
                    xpath = '//*[@id="groupBox"]/div[' + str(2*(i+1)) +']/text()'
                    group_type = response.xpath(xpath).extract()[0].strip()
                if group_details[i] == 'tags':
                    xpath = '//*[@id="groupBox"]/div[' + str(2*(i+1)) + ']/a/text()'
                    tags_list = response.xpath(xpath).extract()
                    tags = ', '.join(tags_list)
                if group_details[i] == 'category':
                    xpath = '//*[@id="groupBox"]/div[' + str(2*(i+1)) + ']/a/text()'
                    category_list = response.xpath(xpath).extract()
                    category = ', '.join(category_list)

            junk = response.xpath('//*[@id="currentlyReading"]').extract_first()
            if junk is None:
                curr_reading_titles = ""
                curr_reading_authors = ""
                curr_reading_cnt = 0
                avg_time_per_book = 0.0
            else:
                curr_reading_titles = re.findall('<a title=(.*) class="bookTitle" ',junk)
                curr_reading_titles = ", ".join(curr_reading_titles)
                curr_reading_cnt = len(re.findall('<a title=(.*) class="bookTitle" ',junk))
                curr_reading_authors = re.findall('<span itemprop="name">(.*)</span>',junk)
                curr_reading_authors =", ".join(curr_reading_authors)
                start_date = re.findall('class="label">Start date</dt>\n        <dd class="value">\n          (.*)\n',junk)
                end_date = re.findall('Finish date</dt>\n        <dd class="value">\n          (.*)\n',junk)
                time_per_book = []
                avg_time_per_book = 0.0
                for i in range(0,curr_reading_cnt):
                    end_date1 = datetime.strptime(end_date[i], '%B %d, %Y').date()
                    start_date1 = datetime.strptime(start_date[i], '%B %d, %Y').date()
                    time_per_book.append((end_date1 - start_date1).days)
                avg_time_per_book = float(sum(time_per_book))/len(time_per_book)

            all_links = response.xpath('//h2[@class="brownBackground"]/a/@href').extract()
            bookshelf_link_idx = -1
            for i in range(0,len(all_links)):
                if len(re.findall('shelf=',all_links[i])) != 0:
                    bookshelf_link_idx = i
            if bookshelf_link_idx == -1:
                bookshelf_link = ""
            else:
                bookshelf_link = 'https://www.goodreads.com'+ re.findall('(.*)?shelf.*',all_links[bookshelf_link_idx])[0][:-1]
                #bookshelf_link = 'https://www.goodreads.com'+ all_links[bookshelf_link_idx][:-11]

            #Group_Name = response.meta['Group_Name']
            #member_cnt = response.meta['member_cnt']
            #last_activity = response.meta['last_activity']
            #year = response.meta['year']

            item = GoodreadsItem()
            item['Group_Name'] = Group_Name
            item['avg_time_per_book'] = avg_time_per_book
            item['curr_reading_titles'] = curr_reading_titles
            item['curr_reading_authors'] = curr_reading_authors
            #item['Group_Name2'] = Group_Name2
            item['member_cnt'] = member_cnt
            #item['last_activity'] = last_activity
            #item['year'] = year
            item['category'] = category
            item['tags'] = tags
            item['location'] = location
            item['group_type'] = group_type
            item['bookshelf_link'] = bookshelf_link
            yield item

        # Yield the requests to different search result urls, 
        # using parse_result_page function to parse the response.
        #for url in result_urls[:1]:
        #    Group_Name = response.xpath('//a[@class="groupName"]/text()').extract()[2]
        #    x = response.xpath('//span[@class="greyText"]').extract()[0]
        #    member_cnt = int(re.findall('\d+', x)[0])
        #    last_activity = int(re.findall('\d+', x)[1])
        #    yield Request(url=url, callback=self.parse_result_page)


    #def parse_result_page(self, response):
        # This fucntion parses the search result page.

        # We are looking for url of the detail page.
       # detail_urls = response.xpath('//a[@class="groupName"]/@href').extract()
        

        # Yield the requests to the details pages, 
        # using parse_detail_page function to parse the response.
        #for url in detail_urls:
            #yield Request(url=url, callback=self.parse_detail_page)