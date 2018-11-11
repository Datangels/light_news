import json
from google.cloud import storage

storage_client = storage.Client()
bucket = storage_client.get_bucket('newspapers_articles___articles')

def return_article(request):

	country = request.args.get('country').lower()
	newspaper = request.args.get('newspaper')
	article = request.args.get('article')
	
	blob_article = bucket.get_blob(country + '__' + newspaper + '/' + article.replace('/', '_'))
	blob_article_string = blob_article.download_as_string().decode('utf-8')
	
	return (blob_article_string , 200, {'Access-Control-Allow-Origin': '*'})


if __name__ == "__main__":
	print(return_article({
		'country': 'congo',
		'newspaper': 'groupelavenir',
		'article': 'http:__groupelavenir.org_apres-le-stade-tata-raphael-le-fcc-en-demonstration-de-force-a-mbuji-mayi_'
		}))
