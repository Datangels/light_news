import json
from google.cloud import storage

storage_client = storage.Client()
bucket_name_homepages = 'corriere_it__homepages'
bucket_homepages = storage_client.get_bucket(bucket_name_homepages)

bucket_name_articles = 'corriere_it__articles'
bucket_articles = storage_client.get_bucket(bucket_name_articles)


def get_corriere_articles(data, context):
	print('Starting get_corriere_articles...')
	file_name = data['name']
	blob_articles = bucket_homepages.blob(file_name)
	articles = json.loads(blob_articles.download_as_string().decode("utf-8"))
	print('Extracted ' + str(len(articles['articles'])) + ' articles from '+ file_name)
	for article in articles['articles']:
		link = articles['articles'][article]['link']
		link_cleaned = link.replace('/', '_')
		if not bucket_articles.get_blob(link_cleaned):
			print('Saving ' + link)
			blob_article = bucket_articles.blob(link_cleaned)
			blob_article.upload_from_string(json.dumps({
				'link': link,
				'title': articles['articles'][article]['title'],
				'category': articles['articles'][article]['category'],
				'description': articles['articles'][article]['description']
			}))
		else:
			print('SKIPPED: ' + link)


if __name__ == "__main__":
	get_corriere_articles('', '')
