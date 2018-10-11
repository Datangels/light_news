import sys
import json
import time
import datetime
import newspaper
from newspaper import Article
from newspaper import fulltext
from google.cloud import storage


'''
https://us-central1-lightnews-212422.cloudfunctions.net/get_homepage?
	url=https://www.timeslive.co.za/&
	newspaper=timeslive&
	country=sudafrica
'''


def get_homepage(request):

	print('Starting processing newspaper...')
	params = {
		'url': request.args.get('url'),
		'newspaper': request.args.get('newspaper'),
		'country': request.args.get('country')
	}
	
	bucket = manage_bucket(params['country'] + '__' + params['newspaper'])

	timestamp = generate_timestamp()
	
	print('Extracting articles...')
	paper = newspaper.build(params['url'])
	articles = extract_articles(paper)
	articles['saving'] = calculate_saving(paper, articles['articles'])
	
	response = {
		'params': params,
		'status': 'success',
		'timestamp': timestamp
	}
	
	articles['response'] = response
	
	print('Saving data...')
	send_output_to_storage(bucket, timestamp, articles)
	
	return json.dumps(response)


def manage_bucket(bucket_name):
	storage_client = storage.Client()
	try:
		return storage_client.get_bucket(bucket_name)
	except:
		return storage_client.create_bucket(bucket_name)


def generate_timestamp():
	ts = time.time()
	return datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
	

def extract_articles(paper):
	articles= {'articles': {}}
	for i, item in enumerate(paper.articles):
		articles['articles'][i] = {
			'url': item.url
		}
	return articles


def calculate_saving(paper, articles):
    size_response = sys.getsizeof(paper.html)
    size_output = sys.getsizeof(articles)
    return format(100 * (1 - float(size_output) / float(size_response)), '.2f') + '%'


def send_output_to_storage(bucket, timestamp, articles):
	blob = bucket.blob(timestamp + '.json')
	blob.upload_from_string(json.dumps(articles))


if __name__ == "__main__":
	print(get_homepage(
		{
			'url': 'https://www.straitstimes.com/',
			'newspaper': 'straitstimes',
			'country': 'Singapore'
		}))
