"""
	Usage:
		python run.py

"""


from fbCrawler import FacebookCrawler
import secrets



if __name__ == '__main__':
	auth_user = secrets.AUTH_USER
	password = secrets.USER_PWD
	
	print('Starting session')
	crawler = FacebookCrawler(auth_user,password)
	example_user = secrets.EXAMPLE_USER
	print('Retrieving user..')
	user = crawler.get_user(example_user)
	for post in user.posts[0:10]:
		print(post.date)
		print(post.text)