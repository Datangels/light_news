import json
from google.cloud import storage

storage_client = storage.Client()
bucket_name = 'corriere_it__homepages'
bucket = storage_client.get_bucket(bucket_name)


show_corriere_article_url = 'https://us-central1-lightnews-212422.cloudfunctions.net/show_corriere_article?file='


def show_corriere(request):
	
	output = """<html>
					<title>Corriere Della Sera</title>
					<head>
						<style>
							body{
							    font-size: 14px;
							    color: #2f2f2f;
							    background-color: #f9f7f1;
							}
							div.saving{
							    font-size: 30px;
							    color: #30a035;
							}
							div.article{
								border-style: groove;
								border-color: grey;
							}
						</style>
					</head>
					<body>"""

	output_end = "</body></html>"
	
	blobs = bucket.list_blobs()
	last_file = [i for i in blobs][-1]
	articles = json.loads(last_file.download_as_string().decode("utf-8"))
	output = output + '<div class="saving">Saved ' + articles['saving'] + ' data.</div>'
	for article in articles['articles']:
		category = articles['articles'][article]['category']
		if category:
			title = articles['articles'][article]['title']
			description = articles['articles'][article]['description']
			link = articles['articles'][article]['link'].replace('/', '_')
			
			output = output + '<div class="article">'
			output = output + '<div class="category">' + str(category) + '</div>'
			output = output + '<div class="title"><a href="' + show_corriere_article_url + str(link) + '">' + str(title) + '</a></div>'
			output = output + '<div class="description">' + str(description) + '</div>'
			output = output + '</div>'
		
	return output + output_end


if __name__ == "__main__":
	print(show_corriere("M"))
 