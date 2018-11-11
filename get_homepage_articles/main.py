import json
from google.cloud import storage

storage_client = storage.Client()
bucket_homepage = storage_client.get_bucket('newspapers_articles')
bucket_articles = storage_client.get_bucket('newspapers_articles___articles')

def get_homepage_articles(data, context):
	print('Creating files for new articles...')
	
	file_name = data['name']

	blob = bucket_homepage.get_blob(file_name)
	blob_json = json.loads(blob.download_as_string().decode("utf-8"))
	
	country = blob_json['params']['country']
	newspaper = blob_json['params']['newspaper']
	url = blob_json['params']['url']
	articles = blob_json['articles']
		
	print('Iterating articles...')
	for article in articles:
		article_url = articles[article]['url']
		article_url_cleaned = article_url.replace('/', '_')
		article_file_name = country + '__' + newspaper + '/' + article_url_cleaned
		if not bucket_articles.get_blob(article_file_name):
			blob_article = bucket_articles.blob(article_file_name)
			blob_article.upload_from_string(json.dumps({
				'url': article_url
			}))

	print('Success')


if __name__ == "__main__":
	get_homepage_articles({
		'name': 'italy__corriere/homepages/2018_11_10_18_35_35.json'
	}, '')
