import json
from newspaper import Article
from google.cloud import storage


def get_article(data, context):

	print('Getting article text...')
	file_name = data['name']
	bucket_name = data['bucket']
	
	bucket_articles = manage_bucket(bucket_name)
	blob_article = bucket_articles.get_blob(file_name)
	
	print('Extracting text from url...')
	article_info = get_article_info(blob_article)
	article_url = article_info['url']
	article = get_article_text(article_url)
	article_text = article.text
	article_info['text'] = article_text
	
	blob_article.upload_from_string(json.dumps(article_info))
	
	print('Text succesfully extracted')


def manage_bucket(bucket_name):
	storage_client = storage.Client()
	try:
		return storage_client.get_bucket(bucket_name)
	except:
		return storage_client.create_bucket(bucket_name)


def get_article_info(blob_article):
	return json.loads(blob_article.download_as_string().decode('utf-8'))


def get_article_text(article_link):
	article = Article(article_link)
	article.download()
	article.parse()
	return article


if __name__ == "__main__":
	get_article({
		'name': 'sudafrica__timeslive__co_za___articles/https:__www.timeslive.co.za_sunday-times_lifestyle_fashion-and-beauty_2018-09-22-how-the-rise-of-the-insta-barbie-has-changed-the-global-beauty-industry_'
	}, '')
