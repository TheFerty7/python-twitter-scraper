import io
import sqlite3
import scraper
import db_connection
from sqlite3 import Error

def start_parse(conn):
	username = input('Username: ')

	with_replies = False
	if input('Do you want to include replies? (y/n): ') == 'y':
		with_replies = True

	retweets = False
	if input('Do you want to include retweets? (y/n): ') == 'y':
		retweets = True

	pages_to_scroll = int(input('Number of pages to scroll: '))

	#TODO: select driver type, currently just assumes Firefox with GekoDriver is available
	username_id = db_connection.get_id_by_username(conn, username)
	if username_id is None:
		username_id = db_connection.insert_username(conn, username)

	set_of_tweets = scraper.start_scrape(username, pages_to_scroll, with_replies, retweets)
	db_connection.insert_many_tweet_urls(conn, list(set_of_tweets), username_id)

if __name__ == '__main__':
	print('Starting up!')
	#TODO: maybe allow a choice of alternative database types or location? MongoDB?
	conn = db_connection.setup_database()
	start_parse(conn)
	print('Exiting')
	db_connection.close_connection(conn)
	exit()

