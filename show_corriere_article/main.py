import json
from google.cloud import storage


storage_client = storage.Client()
bucket_name_articles = 'corriere_it__articles'
bucket_articles = storage_client.get_bucket(bucket_name_articles)


def show_corriere_article(request):

	output = """<html>
					<title>Corriere Della Sera</title>
					<head>
						<style>
							body {
							  font-size:100%; 
							  line-height:1.5;
							  font-family: 'Merriweather', Georgia, 'Times New Roman', Times, serif;
							}
							div.title{
								font-weight: bold;
							    font-size: 25px;
							}
							div.description{
								font-weight: bold;
							    font-size: 15px;
							}
							div.text{
							    font-size: 20px;
							}
						</style>
					</head>
					<body>"""

	output_end = "</body></html>"

	# file = request['file'] #.args.get('file')
	file = request.args.get('file')
	blob_article = bucket_articles.get_blob(file)
	article_data = json.loads(blob_article.download_as_string().decode('utf-8'))
	link = article_data['link']
	title = article_data['title']
	category = article_data['category']
	description = article_data['description']
	text = article_data['text']

	output = output + '<div class="category">' + category + '</div>'
	output = output + '<div class="title">' + title + '</div>'
	output = output + '<div class="description">' + description + '</div>'
	output = output + '<div class="text">' + text + '</div>'
	output = output + '<div class="link"><a href="' + link + '">' + 'ORIGINAL LINK' + '</a></div>'

	return output + output_end


if __name__ == "__main__":
	print(show_corriere_article({
		'file': 'https:__milano.corriere.it_notizie_cronaca_18_agosto_25_stupro-jesolo-mohamed-l-arrivo-aereo-furti-atti-osceni-ma-non-puo-essere-espulso-40585b48-a89f-11e8-a941-3e0c2a4df45f.shtml'
	}))