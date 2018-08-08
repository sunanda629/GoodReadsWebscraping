from scrapy import Spider, Request
from GoodReads_bookshelf.items import GoodreadsBookshelfItem
import re
import math

class GoodReads_bookshelfSpider(Spider):
	name = 'GoodReads_bookshelf_spider'
	allowed_urls = ['https://www.goodreads.com/']
	start_urls = [
	"https://www.goodreads.com/group/bookshelf/64233-addicted-to-ya",
	"https://www.goodreads.com/group/bookshelf/4170-the-sword-and-laser",
	"https://www.goodreads.com/group/bookshelf/1865-scifi-and-fantasy-book-club",
	"https://www.goodreads.com/group/bookshelf/88432-the-perks-of-being-a-book-addict",
	"https://www.goodreads.com/group/bookshelf/35559-nothing-but-reading-challenges",
	"https://www.goodreads.com/group/bookshelf/58421-2018-reading-challenge",
	"https://www.goodreads.com/group/bookshelf/8115-the-history-book-club",
	"https://www.goodreads.com/group/bookshelf/52937-around-the-world-in-80-books",
	"https://www.goodreads.com/group/bookshelf/77596-crazy-for-young-adult-books",
	"https://www.goodreads.com/group/bookshelf/85934-new-adult-book-club",
	"https://www.goodreads.com/group/bookshelf/73843-ya-buddy-readers-corner",
	"https://www.goodreads.com/group/bookshelf/87303-goodreads-choice-awards-book-club",
	"https://www.goodreads.com/group/bookshelf/72929-lovers-of-paranormal",
	"https://www.goodreads.com/group/bookshelf/84674-crime-mysteries-thrillers",
	"https://www.goodreads.com/group/bookshelf/189072-everyone-has-read-this-but-me---the-catch-up-book-club",
	"https://www.goodreads.com/group/bookshelf/40148-catching-up-on-classics-and-lots-more",
	"https://www.goodreads.com/group/bookshelf/174195-around-the-year-in-52-books",
	"https://www.goodreads.com/group/bookshelf/742-christian-fiction-devourers",
	"https://www.goodreads.com/group/bookshelf/78579-young-adult-contemporary-romance",
	"https://www.goodreads.com/group/bookshelf/121247-drop-everything-and-read"]

	def parse(self, response):
		#Group_Name = response.xpath('//*[@id="pageHeader"]/h1/a/text()').extract_first()
		book_tail_links = response.xpath('//td[@width="30%"]/a/@href').extract()
		for i in range(0, len(book_tail_links)):
			Group_Name = response.xpath('//*[@id="pageHeader"]/h1/a/text()').extract_first()
			book_link = 'https://www.goodreads.com' + book_tail_links[i]
			title = response.xpath('//td[@width="30%"]/a/text()').extract()[i]
			author = response.xpath('//td[@width="10%"]/a/text()').extract()[i]

			item = GoodreadsBookshelfItem()
			item['Group_Name'] = Group_Name
			item['book_link'] = book_link
			item['title'] = title
			item['author'] = author

			yield item

		#https://www.goodreads.com/group/bookshelf/73843-ya-buddy-readers-corner?page=1
		#result_urls = ['https://www.goodreads.com/group/show_tag/bookclub?page={}'.format(x) for x in range(1,100)]
		'''page_detail = response.xpath('/html/body/div[1]/div[3]/div[1]/div[1]/div[4]/span/text()').extract_first()
		page_detail = page_detail.strip()
		page_detail = page_detail.replace(',','')
		page_array = re.findall('\d+',page_detail)
		total_pages = math.ceil(int(page_array[2])/int(page_array[1]))

		if str(response) == '<200 https://seatgeek.com/venues/music-hall-of-williamsburg/tickets>':
			book_list_urls = ['https://seatgeek.com/venues/music-hall-of-williamsburg/tickets?page={}'.format(x) for x in range(1, total_pages+1)]
			
			# Brooklyn Steel
		elif str(response) == '<200 https://seatgeek.com/venues/brooklyn-steel-1/tickets>':
			book_list_urls = ['https://seatgeek.com/venues/brooklyn-steel-1/tickets?page={}'.format(x) for x in range(1, total_pages+1)]
 			
 			# Aisle 5
		elif str(response) == '<200 https://seatgeek.com/venues/aisle-5-1/tickets>':
			book_list_urls = ['https://seatgeek.com/venues/aisle-5-1/tickets?page={}'.format(x) for x in range(1, total_pages+1)]

			# Fête Music Hall
		elif str(response) == '<200 https://seatgeek.com/venues/fete-music-hall-2/tickets>':
			book_list_urls = ['https://seatgeek.com/venues/fete-music-hall-2/tickets']

			# Gasa Gasa                     17
		elif str(response) == '<200 https://seatgeek.com/venues/gasa-gasa/tickets>':
 			book_list_urls = ['https://seatgeek.com/venues/gasa-gasa/tickets']

 		result_pages = book_list_urls

 		for url in result_pages:
 			yield Request(url=url, callback=self.parse_result_page)

 	def parse_result_page(self, response):'''
 		

