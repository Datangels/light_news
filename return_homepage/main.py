import json
from google.cloud import storage

storage_client = storage.Client()
bucket = storage_client.get_bucket('newspapers_articles')

def return_homepage(request):
	
	country = request.args.get('country').lower()
	newspaper = request.args.get('newspaper')

	prefix_input = country + '__' + newspaper
	blobs = bucket.list_blobs(prefix=prefix_input)
	last_file = [i for i in blobs][-1]
	articles = last_file.download_as_string().decode("utf-8")

	return (articles, 200, {'Access-Control-Allow-Origin': '*'})

if __name__ == "__main__":
	print(return_homepage({
		'country': 'congo',
		'newspaper': 'groupelavenir'
		}))