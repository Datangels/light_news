import json
from google.cloud import storage
storage_client = storage.Client()


def return_article(request):

	print('Starting returning article...')
	
	params = {
		'country': request.args.get('country').lower(),
		'newspaper': request.args.get('newspaper'),
		'article': request.args.get('article')
	}
	
	bucket_name = params['country'] + '__' + params['newspaper'] + '___articles'
	bucket = storage_client.get_bucket(bucket_name)
	
	blob_article = bucket.get_blob(params['article'].replace('/', '_'))
	return blob_article.download_as_string().decode('utf-8')	


if __name__ == "__main__":
	print(return_article({
		'country': 'nigeria',
		'newspaper': 'punchng',
		'article': 'https://punchng.com/18-year-old-okada-rider-killed-during-collision-with-camel/'
		}))
