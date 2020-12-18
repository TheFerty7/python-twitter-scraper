# python-twitter-scraper
A twitter scraper written in python using BeautifulSoup, Selenium, and SQLite.
Stores individual tweet urls for given user in a SQLite3 database.
Requires Firefox and GeckoDriver for Selenium.


TO DO LIST (in no particular order):
1. Change scroll method to speed up url collection
2. Proper logging
3. Individual tweet parsing (likes, retweets, replies)
4. Add ability to scroll until end of timeline
5. Add different web drivers
6. Add different database types (maybe)
7. Add ability to choose time frame
8. Add ability to view/browse the database
9. Add ability to distinguish between retweets and user tweets 
10. Add ability to update an account instead of having to reparse everything
