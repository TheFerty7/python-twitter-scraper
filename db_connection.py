import sqlite3
from sqlite3 import Error

#Creates the local database if needed.
def database_init(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print(e)
	finally:
		if conn:
			conn.close()

#Creates a connection to the database and returns the connection obj
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

#Close the connection to the database
def close_connection(conn):
	if conn:
		conn.close()

#Create a table using given SQL
def create_table(conn, sql):
	try:
		c = conn.cursor()
		c.execute(sql)
	except Error as e:
		print(e)

def insert_username(conn, username):
	try:
		c = conn.cursor()
		sql = """ INSERT INTO usernames(username) VALUES (?) """
		c.execute(sql, (username, ))
		conn.commit()
		return c.lastrowid
	except Error as e:
		print(e)

#Gets the specified username, returns the id or None
def get_id_by_username(conn, username):
	try:
		c = conn.cursor()
		sql = """ SELECT id FROM usernames WHERE username = ? """
		c.execute(sql, (username, ))

		row = c.fetchone()
		if row is not None:
			return int(row[0])
		else:
			print("Doesnt exist, creating entry")
			return None

	except Error as e:
		print(e)

#Inserts one tweet url with a username_id
def insert_one_tweet_url(conn, tweet_url, username_id):
	try:
		c = conn.cursor()
		sql = """ INSERT INTO tweeturls(tweeturl, username_id) VALUES (?, ?) """
		c.execute(sql, (tweet_url, username_id))
		conn.commit()
	except Error as e:
		print(e)

#inserts a list of tweet urls associated with the given username_id
#Warning: if one fails to insert due to unique constraints, the whole batch fails
def insert_many_tweet_urls(conn, list_of_tweets, username_id):
	try:
		c = conn.cursor()
		sql = """ INSERT INTO tweeturls(tweeturl, username_id) VALUES (?, {0}) """.format(username_id)
		c.executemany(sql, list(zip(list_of_tweets))) #Converts each object in the list to a tuple like this: (value, )
		conn.commit()
	except Error as e:
		print(e)

#inserts tweet urls one by one from list
def insert_loop_tweet_urls(conn, list_of_tweets, username_id):
	c = conn.cursor()
	sql = """ INSERT INTO tweeturls(tweeturl, username_id) VALUES (?, {0}) """.format(username_id)
	for tweet_url in list_of_tweets:
		try:
			c.execute(sql, (tweet_url, ))
			
		except Error as e:
			#probably a unique error
			continue

	conn.commit()


#Inital DB setup, creates tables
#Returns connection
def setup_database():
	database = r"tweets.sqlite3"
	database_init(database)

	sql_create_usernames_table = """CREATE TABLE IF NOT EXISTS usernames (
										id integer PRIMARY KEY,
										username text NOT NULL
									); """

	sql_create_tweeturls_table = """CREATE TABLE IF NOT EXISTS tweeturls (
										id integer PRIMARY KEY,
										tweeturl text NOT NULL,
										username_id integer NOT NULL,
										UNIQUE(tweeturl, username_id),
										FOREIGN KEY (username_id) REFERENCES usernames (id)
									); """

	conn = create_connection(database)

	if conn is not None:
		try:
			create_table(conn, sql_create_usernames_table)

			create_table(conn, sql_create_tweeturls_table)
		except Error as e:
			print(e)

	else:
		print("Error connection not found.")

	return conn