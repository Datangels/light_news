import sys
import json
import time
import datetime
from newspaper import Article
from google.cloud import storage


def get_article(data, context):

	timestamp = generate_timestamp()

	print('Getting article text...')
	file_name = data['name']
	bucket_name = data['bucket']
	
	bucket_articles = manage_bucket(bucket_name)
	blob_article = bucket_articles.get_blob(file_name)
	
	print('Extracting text from url...')
	article_info = get_article_info(blob_article)
	article_url = article_info['url']
	
	article = Article(article_url)
	article.download()
	
	article_parsed = get_article_text(article)
	article_text = article_parsed.text
	article_info['text'] = article_text	
	article_info['saving'] = calculate_saving(article.html, article_text)
	article_info['timestamp'] = timestamp
	
	blob_article.upload_from_string(json.dumps(article_info))
	
	print('Text succesfully extracted')


def manage_bucket(bucket_name):
	storage_client = storage.Client()
	try:
		return storage_client.get_bucket(bucket_name)
	except:
		return storage_client.create_bucket(bucket_name)
		

def generate_timestamp():
	ts = time.time()
	return datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')


def get_article_info(blob_article):
	return json.loads(blob_article.download_as_string().decode('utf-8'))


def get_article_text(article):
	article.parse()
	return article


def calculate_saving(article_page, article_text):
    size_article_page = sys.getsizeof(article_page)
    size_article_text = sys.getsizeof(article_text)
    return format(100 * (1 - float(size_article_text) / float(size_article_page)), '.2f') + '%'


if __name__ == "__main__":
	get_article({
		'name': 'https:__punchng.com_18-year-old-okada-rider-killed-during-collision-with-camel_',
		'bucket': 'nigeria__punchng___articles'
	}, '')
