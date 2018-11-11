import newspaper

def verify_newspaper(request):
	
	website = request.args.get('website')

	paper = newspaper.build(website )
	
	if len(paper.articles) == 0:
		 return'No articles found'
	else:
		return str(len(paper.articles))


if __name__ == "__main__":
	print(verify_newspaper({
		'website': 'https://www.scotsman.com/'
		}))
