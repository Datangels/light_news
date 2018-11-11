import json
from google.cloud import storage

storage_client = storage.Client()
bucket = storage_client.get_bucket('newspaper_map')

def add_newspaper(request):

	continent = request.args.get('continent')
	country = request.args.get('country')
	newspaper = request.args.get('newspaper')

	blob_map = bucket.get_blob('country_map.json')
	country_map = blob_map.download_as_string().decode("utf-8")
	country_map_json = json.loads(country_map)

	try:
		country_map_json[continent][country][newspaper] = {}
		blob_map.upload_from_string(json.dumps(country_map_json))
	except:
		try:
			country_map_json[continent][country] = {}
			country_map_json[continent][country][newspaper] = {}
			blob_map.upload_from_string(json.dumps(country_map_json))
		except:
			country_map_json[continent] = {}
			country_map_json[continent][country] = {}
			country_map_json[continent][country][newspaper] = {}
			blob_map.upload_from_string(json.dumps(country_map_json))
		
	
	return 'Success'


if __name__ == "__main__":
	print(add_newspaper({
		'continent': 'Europa',
		'country': 'Scotland',
		'newspaper': 'scotsman'
		}))