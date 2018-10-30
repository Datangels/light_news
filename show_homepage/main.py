import json
from google.cloud import storage

storage_client = storage.Client()
bucket_name = 'newspaper_map'
bucket = storage_client.get_bucket(bucket_name)

blob = bucket.get_blob('country_map.json')
country_map = blob.download_as_string().decode("utf-8")
country_map_json = json.loads(country_map)


html = """				
		<html>
			<head>
				<style>
				</style>
				<script>
															
					var country_map = """ + country_map + """;
					
					function show_continents() {
						for (var continent in country_map) {
						    var button_continent = document.createElement("button");
							button_continent.setAttribute('onclick', 'show_countries("' + continent + '")')   
							button_continent.id = "button_continent";
						    button_continent.textContent = continent;
						    document.getElementById("buttons_continents").appendChild(button_continent);
						}
					}

					function show_countries(continent) {
						delete_childs("buttons_countries");
						delete_childs("buttons_newspapers");
						delete_childs("articles");
						for (var country in country_map[continent]) {
						    var button_country = document.createElement("button");
							button_country.setAttribute('onclick', 'show_newspapers("' + continent + '", "' + country + '")')   
							button_country.id = "button_country";
						    button_country.textContent = country;
						    document.getElementById("buttons_countries").appendChild(button_country);
						}
					}
					
					function show_newspapers(continent, country) {
						delete_childs("buttons_newspapers");
						delete_childs("articles");
						for (var newspaper in country_map[continent][country]) {
						  	var button_newspaper = document.createElement("button");
							button_newspaper.setAttribute('onclick', 'show_articles("' + country + '", "' + newspaper + '")')  
							button_newspaper.id = "button_newspaper";
						    button_newspaper.textContent = newspaper;
						    button_newspaper.type="button"
						    document.getElementById("buttons_newspapers").appendChild(button_newspaper);
						}
					}

					function show_articles(country, newspaper) {
						delete_childs("articles");
						var url = 'https://us-central1-lightnews-212422.cloudfunctions.net/return_homepage?country=' + country + '&newspaper=' + newspaper; 
						fetch(url)
						    .then((res) => res.json())
						    .then(output => {
						    	var saving = output.saving;
								var div_saving = document.createElement('div');
								div_saving.setAttribute('id', 'saving');
								div_saving.textContent = 'Data saved: ' + saving;
								document.getElementById('articles').appendChild(div_saving);
                                for(var i in output.articles) {
                                    var url = output.articles[i]['url'];
                                    var div_article = document.createElement('div');
                                    div_article.setAttribute('id', url);
                                    var a_article = document.createElement('a');
                                    a_article.setAttribute('href', '#');
									a_article.setAttribute('onclick', 'show_article("' + country + '", "' + newspaper + '", "' + url + '")')  
                                    a_article.textContent = url;
                                    div_article.appendChild(a_article);
                                    document.getElementById('articles').appendChild(div_article);
                                }							    
						    } 
						)
					}
					
					function show_article(country, newspaper, article) {
						var url = 'https://us-central1-lightnews-212422.cloudfunctions.net/return_article?country=' + country + '&newspaper=' + newspaper + '&article=' + article; 
						fetch(url)
						    .then((res) => res.json())
						    .then(output => {
								var timestamp = output["timestamp"];
                                var div_timestamp = document.createElement('div');
                                div_timestamp.textContent = timestamp;
                                document.getElementById(article).appendChild(div_timestamp);
						    	
                                var saving = output["saving"];
                                var div_saving = document.createElement('div');
                                div_saving.textContent = saving;
                                document.getElementById(article).appendChild(div_saving);
                                
                                var text = output["text"];
                                var div_article = document.createElement('div');
                                div_article.textContent = text;
                                document.getElementById(article).appendChild(div_article);
						    } 
						)
					}
		
					function delete_childs(id) {
						var childs =  document.getElementById(id);
						while (childs.hasChildNodes()) {
							childs.removeChild(childs.lastChild);
						}
					}
					
					window.onload = show_continents;
					
				</script>
			</head>
			<body>
				<p id="buttons_continents"></p>
				<p id="buttons_countries"></p>
				<p id="buttons_newspapers"></p>		
				<p id="articles"></p>
			</body>
		</html>"""


def show_homepage(request):
	return html

			
if __name__ == "__main__":
	print(show_homepage("M"))