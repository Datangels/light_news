import sys
import json
import time
import datetime
import requests
from google.cloud import storage

'''
Extract all the articles from www.corriere.it XML and save in bucket
'''


storage_client = storage.Client()
bucket_name = 'corriere_it__homepages'
bucket = storage_client.get_bucket(bucket_name)


def get_corriere(request):
	timestamp = generate_timestamp()
	response = get_response()
	articles = extract_articles(response)
	saving = calculate_saving(response, articles)
	articles['saving'] = saving
	send_output_to_storage(timestamp, articles)
	return 'success'


def generate_timestamp():
	ts = time.time()
	return datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
	

def get_response():
	return str(requests.get('https://www.corriere.it/rss/homepage.xml').text.encode('latin-1'), 'utf-8')


def extract_articles(response):
	output = {'articles': {}}
	articles = [i.split('</item')[0] for i in response.split('<item>')]
	for i, item in enumerate(articles):
		if i < 10:
			try:
				title = item.split('<title>')[1].split('</title>')[0]
			except:
				title = '/'
			try:
				description = item.split('<description>')[1].split('</description>')[0].split('/&gt;&lt;p&gt;')[1].split('&lt;/p&gt;')[0]
			except:
				description = '/'
			try:
				link = item.split('<link>')[1].split('</link>')[0]
			except:
				link = '/'
			output['articles'][i] = {
				'title': title,
				'description': description,
				'link': link,
				'category': get_category(link)
			}
	return output


def get_category(link):
	try:
	    if 'www.corriere.it' in link:
	        return link.split('/')[3]
	    else:
	        return link.split('/')[2].split('.')[0]
	except:
		pass


def calculate_saving(response, articles):
    size_response = sys.getsizeof(response)
    size_output = sys.getsizeof(articles)
    return format(100 * (1 - float(size_output) / float(size_response)), '.2f') + '%'



def send_output_to_storage(timestamp, articles):
	blob = bucket.blob(timestamp + '.json')
	blob.upload_from_string(json.dumps(articles))


if __name__ == "__main__":
	print(get_corriere("M"))