# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'

    cast_link_extractor = LinkExtractor( 
        allow="https://www.themoviedb\.org/tv/60059-better-call-saul.+")

    actor_link_extractor = LinkExtractor( 
        allow="https://www.themoviedb\.org/person.+",
        restrict_css = "ol.people.credits:not(.crew)")
    
    start_urls = ['https://www.themoviedb.org/tv/60059-better-call-saul']

    def parse(self, response): # Done
        links = self.cast_link_extractor.extract_links(response)
        target = links[1] # hard coded
        yield Request(target.url, callback = self.parse_full_credits)

    def parse_full_credits(self, response): # NO MORE THAN 5 LINES
        links = self.actor_link_extractor.extract_links(response)

        for link in links:
            yield Request(link.url, callback = self.parse_actor_page)
        
        # this works, but doesn't get full link
        # credits = response.css("ol.people.credits")[0]
        # credit_list = credits.css("li")
        # for credit in credit_list:
        #     target = credit.css("a")[0].attrib['href']

    def parse_actor_page(self, response): # NO MORE THAN 15 LINES
        
        # actor name: response.css("div.title a::text").get()

        # movies: movie1 = response.css("table.credit_group a.tooltip")
        # for each movie, movie name: movie1.css("a bdi::text").get()

        pass
