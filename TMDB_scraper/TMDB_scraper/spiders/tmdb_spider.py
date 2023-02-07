# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider
from scrapy.http import Request

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    start_urls = ['https://www.themoviedb.org/tv/60059-better-call-saul']

    cast_link_extractor = LinkExtractor(allow="https://www.themoviedb\.org/tv/60059-better-call-saul.+")

    actor_link_extractor = LinkExtractor(allow="https://www.themoviedb\.org/person.+",
        restrict_css = "ol.people.credits:not(.crew)")

    def parse(self, response):
        '''
        DOCSTRING
        '''
        links = self.cast_link_extractor.extract_links(response)
        target = links[1] # hard coded
        yield Request(target.url, callback = self.parse_full_credits)

    def parse_full_credits(self, response):
        '''
        DOCSTRING
        '''
        links = self.actor_link_extractor.extract_links(response)
        for link in links:
            yield Request(link.url, callback = self.parse_actor_page)

    def parse_actor_page(self, response):
        '''
        DOCSTRING
        '''
        name = response.css("div.title a::text").get()
        works = response.css("table.credit_group a.tooltip")
        for work in works:
            yield {"actor": name,"movie_or_TV_name": work.css("a bdi::text").get()}
