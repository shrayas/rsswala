import conf
import MySQLdb

db = MySQLdb.connect(user=conf.MYSQL_USER,passwd=conf.MYSQL_PASS,db=conf.MYSQL_DB)

def create_new_feed(data):
  c = db.cursor()

  c.execute("""INSERT INTO 
  feeds(feed_url,title,description,link)
  VALUES(%s,%s,%s,%s)""",
  (data['feed_url'],data['title'],data['description'],data['link']))

  db.commit()

  return c.lastrowid

def add_new_item(data):
  c = db.cursor()

  # also supports multi insert
  c.executemany("""INSERT INTO 
  items(feed_id,title,description,link,guid,pubdate)
  VALUES(%d,%s,%s,%s,%s,%s)""",
  (data))

def get_feed_id(feed_url):
  c = db.cursor()

  c.execute("SELECT id FROM feeds WHERE feed_url = %s",(feed_url,))
  return c.fetchone()[0];

if __name__ == "__main__":
   #data = {'feed_url':'http://rssulr222222','title':'here\'s the title111','description':'here\'s a big badass description','link': 'http://link_url'}
   data = {'link': 'http://techcrunch.com', 'description': 'Startup and Technology News', 'feed_url': 'http://techcrunch.com/feed/', 'title': 'TechCrunch'}
   items = [
           {
               'description':'asdfasdf',
               'pubdate':'2013-01-01',
               'title':'asdasdasd',
               'feed_id':2,
               'link':'http://www.a.com',
               'guid':'qq881ndnbqbq99'
           },
           {
               'description':'qwerasdfasdf',
               'pubdate':'2013-01-01',
               'title':'asdasdasd',
               'feed_id':2,
               'link':'http://www.a.com',
               'guid':'qq881ndnbqbq99xxaa'
           }
           ]
  # create_new_feed(data)

   add_new_item(items)
  # print get_feed_id("http://rssulr");
