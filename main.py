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
	else:
		with_replies = False

	retweets = False
	if input('Do you want to include retweets? (y/n): ') == 'y':
		retweets = True
	else:
		retweets = False

	pages_to_scroll = int(input('Number of pages to scroll: '))

	#TODO: select driver type, need to add more drivers
	driver_type = input('Which driver do you want to use? (firefox, chrome): ')

	username_id = db_connection.get_id_by_username(conn, username)
	if username_id is None:
		username_id = db_connection.insert_username(conn, username)

	set_of_tweets = scraper.start_scrape(username, pages_to_scroll, driver_type, with_replies, retweets)
	db_connection.insert_loop_tweet_urls(conn, list(set_of_tweets), username_id)

if __name__ == '__main__':
	print('Starting up!')
	#TODO: maybe allow a choice of alternative database types or location? MongoDB?
	conn = db_connection.setup_database()
	start_parse(conn)
	print('Exiting')
	db_connection.close_connection(conn)
	exit()

