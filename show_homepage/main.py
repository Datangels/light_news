import json
from google.cloud import storage
from bs4 import BeautifulSoup

storage_client = storage.Client()
bucket_name = 'newspaper_map'
bucket = storage_client.get_bucket(bucket_name)


start_html = """				
				<html>
					<head>
						<style>
						</style>
						<script>
							function show_continent(continent) {
								document.getElementById("demo").innerHTML = continent;
							}	
						</script>
					</head>
					<body>"""


end_html = """
						<p id="demo"></p>
					</body>
				</html>
				"""


def show_continents(country_map):
	output = ''
	for continent in json.loads(country_map).keys():
		output = output + """<button id="button" onclick="show_continent('""" + continent + """')">""" + continent + """</button>"""
	return output


def show_homepage(request):
	blob = bucket.get_blob('country_map.json')
	country_map = blob.download_as_string().decode("utf-8")
	
	output = start_html
	output = output + show_continents(country_map)
	return BeautifulSoup(output + end_html).prettify()

			
if __name__ == "__main__":
	print(show_homepage("M"))