import sys
import json
import time
import datetime
import newspaper
from newspaper import Article
from newspaper import fulltext
from google.cloud import storage

storage_client = storage.Client()
bucket = storage_client.get_bucket('newspapers_articles')

def get_homepage(request):
	print('Starting extracting homepage...')
	
	params = {
		'url': request.args.get('url'),
		'newspaper': request.args.get('newspaper'),
		'country': request.args.get('country')
	}
	
	paper = newspaper.build(params['url'])
	categories = paper.category_urls()
	articles = extract_articles(paper, categories)
	
	articles['saving'] = calculate_saving(paper, articles['articles'])
	articles['params'] = params

	send_output_to_storage(params, bucket, articles)
	
	return json.dumps({'status': 'success'})
	

def extract_articles(paper, categories):
	articles= {'articles': {}}
	counter = 0
	for i, item in enumerate(paper.articles):
		if item.url not in categories:
			if item.url.count('-') > 1:
				if counter < 20:
					counter = counter + 1
					articles['articles'][i] = {
						'url': item.url
					}
	return articles


def calculate_saving(paper, articles):
    size_response = sys.getsizeof(paper.html)
    size_output = sys.getsizeof(articles)
    return format(100 * (1 - float(size_output) / float(size_response)), '.2f') + '%'


def send_output_to_storage(params, bucket, articles):
	blob = bucket.blob(params['country'] + '__' + params['newspaper'] + '/' + str(datetime.datetime.now()) + '.json')
	blob.upload_from_string(json.dumps(articles))


if __name__ == "__main__":
	print(get_homepage(
		{
			'url': 'http://www.corriere.it/',
			'newspaper': 'corriere',
			'country': 'italy'
		}))
