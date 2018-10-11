import json
from google.cloud import storage
storage_client = storage.Client()


def return_homepage(request):

	print('Starting returning newspaper articles...')
	
	params = {
		'country': request.args.get('country').lower(),
		'newspaper': request.args.get('newspaper')
	}
	
	bucket_name = params['country'] + '__' + params['newspaper']
	bucket = storage_client.get_bucket(bucket_name)
	
	blobs = bucket.list_blobs()
	last_file = [i for i in blobs][-1]
	articles = last_file.download_as_string().decode("utf-8")
	return articles


if __name__ == "__main__":
	print(return_homepage({
		'country': 'nigeria',
		'newspaper': 'punchng'
		}))