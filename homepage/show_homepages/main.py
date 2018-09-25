import json
from google.cloud import storage

storage_client = storage.Client()
bucket_name = 'newspaper_map'
bucket = storage_client.get_bucket(bucket_name)

show_corriere_article_url = 'https://us-central1-lightnews-212422.cloudfunctions.net/show_corriere_article?file='

def show_corriere(request):

	blob = bucket.get_blob('country_map.json')
	country_map = json.loads(blob.download_as_string().decode("utf-8"))

	output = '''
		<html>
			<body>
				<p>This example uses the HTML DOM to assign an "onclick" event to a p element.</p>
				
				<p id="europa">Europa.</p>
				
				<script>
				
					document.getElementById("europa").onclick = function() {show_countries(''' + str(country_map["Europa"]) + ''')};
					
					function show_countries(country) {
						
						alert("CIAO");

						// for (var i = 0; i < map_countries.length; i++) {
						// 	var div = document.createElement('div');
						// 	var x = document.getElementsByClassName("example");
						// 	x.appendChild(div);
						// }
					}
					
				</script>		
			</body>
		</html>
		'''
	return output
			
if __name__ == "__main__":
	print(show_corriere("M"))