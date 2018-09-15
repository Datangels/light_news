import json
from newspaper import Article
from google.cloud import storage

storage_client = storage.Client()
bucket_name_articles = 'corriere_it__articles'
bucket_articles = storage_client.get_bucket(bucket_name_articles)


def get_corriere_article(data, context):
	print('Starting get_corriere_article...')
	file_name = data['name']
	blob_article = bucket_articles.get_blob(file_name)
	article_info = get_article_info(blob_article)
	article_link = article_info['link']
	print('Extracting text from link: ' + article_link)
	article = get_article(article_link)
	article_text = article.text
	article_info['text'] = article_text
	blob_article.upload_from_string(json.dumps(article_info))
	print('Text succesfully extracted')

def get_article_info(blob_article):
	return json.loads(blob_article.download_as_string().decode('utf-8'))


def get_article(article_link):
	article = Article(article_link)
	article.download()
	article.parse()
	return article


if __name__ == "__main__":
	get_corriere_article('', '')
