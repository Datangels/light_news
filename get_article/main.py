import sys
import json
import time
import datetime
from newspaper import Article
from google.cloud import storage

storage_client = storage.Client()
bucket = storage_client.get_bucket('newspapers_articles___articles')

def get_article(data, context):
	
	file_name = data['name']

	blob = bucket.get_blob(file_name)
	blob_json = json.loads(blob.download_as_string().decode("utf-8"))
	
	article_url = blob_json['url']
	article = Article(article_url)
	article.download()
	article.parse()

	blob_json['text'] = article.text
	blob_json['saving'] = calculate_saving(article.html, article.text)
	blob_json['timestamp'] = str(datetime.datetime.now())
	
	blob.upload_from_string(json.dumps(blob_json))


def calculate_saving(article_page, article_text):
    size_article_page = sys.getsizeof(article_page)
    size_article_text = sys.getsizeof(article_text)
    return format(100 * (1 - float(size_article_text) / float(size_article_page)), '.2f') + '%'


if __name__ == "__main__":
	get_article({
		'name': 'italy__corriere/articles/http:__visionifuture.corriere.it_2013_09_05_tv-oled-e-ultra-hd-confronto-ravvicinato_'
	}, '')
