import json
from google.cloud import storage

storage_client = storage.Client()

def get_homepage_articles(data, context):
	print('Creating files for new articles...')
	file_name = data['name']
	bucket_name = data['bucket']
	
	bucket_homepage = manage_bucket(bucket_name)
	bucket_articles = manage_bucket(bucket_name + '___articles')
	
	blob_articles = bucket_homepage.get_blob(file_name)
	articles = json.loads(blob_articles.download_as_string().decode("utf-8"))
	print('Extracted ' + str(len(articles['articles'])) + ' articles from '+ file_name)
	
	new_articles = 0
	old_articles = 0
		
	for article in articles['articles']:
		url = articles['articles'][article]['url']
		url_cleaned = url.replace('/', '_')
		if not bucket_articles.get_blob(url_cleaned):
			blob_article = bucket_articles.blob(url_cleaned)
			blob_article.upload_from_string(json.dumps({
				'url': url
			}))
			new_articles += 1
		else:
			old_articles += 1

	print('New articles: ' + str(new_articles))
	print('Old articles: ' + str(old_articles))

def manage_bucket(bucket_name):
	storage_client = storage.Client()
	try:
		return storage_client.get_bucket(bucket_name)
	except:
		return storage_client.create_bucket(bucket_name)


if __name__ == "__main__":
	get_homepage_articles({
		'bucket': 'sudafrica__timeslive__co_za',
		'name': '2018_09_23_17_18_30.json'
	}, '')
