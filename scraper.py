import io
import aiohttp
import logging
import random
import sys
import threading
import time
import queue
import db_connection
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#Start scrape, will load all tweets the specified username into a set.
#username: the username of the account to be scraped
#pages_to_scroll: how far down you want to scroll. TODO: Input 0 or negative for scroll until end
#with_replies: if true, will load the replies page instead of just the users regular tweets/retweets
#retweets: if true, will include retweets. TODO: separate retweets into a different table/list?
#RETURNS: Set<string> of tweets
def start_scrape(username, pages_to_scroll, with_replies = False, retweets = False):

	set_of_tweets = set()

	if pages_to_scroll < 1:
		print('Must be at least 1 page')
		return set_of_tweets

	try:
		firefox_options = webdriver.FirefoxOptions()
		firefox_options.set_headless()
		driver = webdriver.Firefox(firefox_options=firefox_options)
		url = "http://www.twitter.com/" + username
		if with_replies:
			driver.get(url + "/with_replies")
		else:
			driver.get(url)

		i = 0
		time.sleep(3) #Inital load
		while True:
			#Give the page some time to load, otherwise it may not have initalized all the javascript elements
			#slow internet connections may have problems here?
			time.sleep(1)
			soup = BeautifulSoup(driver.page_source, 'lxml')


			timeline = soup.body.find('main').find('section').div.div

			#TODO: Scroll by difference between top and bottom tweets
			#length = timeline.contents[-1].get('style')
			#scroll_length = int(length[length.find("(")+1:length.find(")")-2])
			for item in timeline.contents:
				#Each 'article' is one tweet panel. Includes profile.
				tweet = item.find('article')
				if tweet is None:
					#If there is no article then it is probably an ad or a suggested follow panel. So we skip it.
					continue
				elif retweets:
					a_tag = tweet.find('a', href=lambda value: value and '/status/' in value)
					if a_tag is not None:
						tweet_link = 'twitter.com' + a_tag.get('href')
						print(tweet_link)
						set_of_tweets.add(tweet_link)
				else:
					a_tag = tweet.find('a', href=lambda value: value and value.lower().startswith('/' + username.lower() + '/status'))
					if a_tag is not None:
						tweet_link = 'twitter.com' + a_tag.get('href')
						print(tweet_link)
						set_of_tweets.add(tweet_link)

			#TODO: slowly traverse down the page by different lengths due to inconsistency in tweet sizes.
			driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
			#driver.execute_script("window.scrollBy(0, " + str(scroll_length) + ");")
			if i < pages_to_scroll:
				i = i+1
			else:
				break
	except Error as e:
		print(e)
	finally:
		driver.close()
		return set_of_tweets