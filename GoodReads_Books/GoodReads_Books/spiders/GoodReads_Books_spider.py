
from scrapy import Spider, Request
from GoodReads_Books.items import GoodreadsBooksItem
import re

class GoodReads_booksSpider(Spider):
	name = 'GoodReads_Books_spider'
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
		book_urls = ['https://www.goodreads.com' + link for link in book_tail_links]

		for url in book_urls:
			yield Request(url=url, meta={'url': url}, callback=self.parse_detail_page)

	def parse_detail_page(self, response):
		url = response.meta['url'] 
		title = response.xpath('//*[@id="bookTitle"]/text()').extract_first().strip()
		author = response.xpath('//*[@id="bookAuthors"]/span[2]/div/a/span/text()').extract_first()
		rating = float(response.xpath('//*[@id="bookMeta"]/span[3]/span/text()').extract_first())
		num_ratings = int(response.xpath('//*[@id="bookMeta"]/a[2]/span/text()').extract_first().strip().replace(',',''))
		#num_pages = int(re.findall('\d+',response.xpath('//*[@id="details"]/div[1]/span[2]/text()').extract_first())[0])

		if (response.xpath('//*[@id="details"]/div[1]/span[3]/text()') != []):
			try:
				num_pages = int(re.findall('\d+',response.xpath('//*[@id="details"]/div[1]/span[3]/text()').extract_first())[0])
			except TypeError:
				num_pages = -1
			except IndexError:
				num_pages = -2
		elif (response.xpath('//*[@id="details"]/div[1]/span[2]/text()') != []):
			try:
				num_pages = int(re.findall('\d+',response.xpath('//*[@id="details"]/div[1]/span[2]/text()').extract_first())[0])
			except TypeError:
				num_pages = -3
			except IndexError:
				num_pages = -4
		elif (response.xpath('//*[@id="details"]/div[1]/span/text()') != []):
			try:
				num_pages = int(re.findall('\d+',response.xpath('//*[@id="details"]/div[1]/span/text()').extract_first())[0])
			except TypeError:
				num_pages = -5
			except IndexError:
				num_pages = -6
		else:
			num_pages = 0

		if (response.xpath('//*[@id="details"]/div[2]/text()') != []):
			try:
				year_published = int(re.findall('\d\d\d\d',response.xpath('//*[@id="details"]/div[2]/text()').extract_first())[0])
			except TypeError:
				year_published = -1
			except ValueError:
				year_published = -2
			except IndexError:
				year_published = -3
		elif (response.xpath('//*[@id="details"]/div[1]/text()') != []):
			try:
				year_published = int(re.findall('\d\d\d\d',response.xpath('//*[@id="details"]/div[1]/text()').extract_first())[0])
			except TypeError:
				year_published = -4
			except ValueError:
				year_published = -5
			except IndexError:
				year_published = -6
		else:
			year_published = 0

		
		#genre_detail = response.xpath('/html/body/div[2]/div[3]/div[3]/div[2]/div[5]/div[6]/div/div[2]/div').extract_first()
		#genre_detail_list = re.findall('">(.*)</a>',genre_detail)[:-1]
		#for i in range(0,(len(genre_detail_list)/2)):
			#genre_i = genre_detail_list[i]
			#genre_vote_i = int(re.findall('\d+',genre_detail_list[i+1])[0])
		item = GoodreadsBooksItem()
		item['title'] = title
		item['author'] = author
		item['rating'] = rating
		item['num_ratings'] = num_ratings
		item['num_pages'] = num_pages
		item['year_published'] = year_published
		item['url'] = url
		yield item





















