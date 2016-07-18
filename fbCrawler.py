"""
    Tech notes:
        Intro mechanize (fake browser sessions): http://www.pythonforbeginners.com/cheatsheet/python-mechanize-cheat-sheet

"""

import mechanize
from bs4 import BeautifulSoup
from datetime import date
from elasticsearch import Elasticsearch              # ElasticSearch            Python lib/API for ElasticSearch DB server    https://github.com/elasticsearch/elasticsearch-py


class FacebookCrawler():

    def __init__(self,username,password):

        #Create browser
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)
        cookies = mechanize.CookieJar()
        self.browser.set_cookiejar(cookies)
        self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.41 Safari/534.7')]
        self.browser.set_handle_refresh(False)

        #Log in
        self.browser.open('http://m.facebook.com/')
        self.browser.select_form(nr = 0)

        self.browser.form['email'] = username
        self.browser.form['pass'] = password
        self.browser.submit()

    def get_user(self,username):

        raw_page = self.browser.open('http://m.facebook.com/'+username+'/year/'+str(date.today().year))
        print(raw_page.read())
        posts = self.html_to_posts(raw_page.read())

        user = FacebookUser(username,posts,None)
        return user

    def html_to_posts(self,html):

        parsed_page = BeautifulSoup(html)
        ### URL ###
        # Sometimes webpages redirect us around, this will make sure our URL will be the ACTUAL URL of the page
        aURL = response.url

        ### Title ###
        title = soup.title.string

        ### Description ###
        # Get the description of the page from the meta tag
        # If none available; set the desc to an error message
        try:
            desc = soup.find("meta", {"name":"description"})['content']
        except:
            desc = "A description for this site is not available."

        posts = []
        dates = []

        for abbr in parsed_page.find_all('abbr'):
            dates.append(abbr.get_text())

        index = 0

        for div in parsed_page.find_all('div'):

            if 'class' in div.attrs and 'by' in div['class']:
                posts.append(FacebookPost(dates[index],div.get_text()))

                index += 1
        print('Printing posts')
        print(posts)
        print(dates)
        return posts

    def load_to_es(self):
        es = Elasticsearch()


    def add_to_database(url, title, description, content):
        """
        This function adds the webpage to the ElasticSearch database
        """
        es.index(
            index='webpages',
            doc_type='webpage',
            body={
                "url" : url,
                "title" : title,
                "description" : description,
                "content" : content
            }
        )


class FacebookUser():

    def __init__(self,username,posts,age):
        self.username = username
        self.posts = posts
        self.age = age


class FacebookPost():

    def __init__(self,date,text):

        self.date = date
        self.text = text
