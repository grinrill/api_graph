from bottle import Bottle, request
import json
from html_telegraph_poster import TelegraphPoster

app = Bottle()

graph = TelegraphPoster()

print('hhhhhhhh')

@app.route('/create_api_token', method=['GET', 'POST'])
def create_api_token():
	kwargs = {i: None for i in ['short_name', 'author_name', 'author_url']}

	args_raw = request.params.decode().dict
	args = {i: args_raw[i][0] for i in args_raw}

	kwargs.update(args)
	kwargs = {i: kwargs[i] for i in ['short_name', 'author_name', 'author_url']}

	if kwargs['author_name'] == None:
		return '400 need author_name' #418 :)

	return graph.create_api_token(**kwargs)

@app.route('/post', method=['GET', 'POST'])
def post():
	kwargs = {i: None for i in ['title', 'author', 'text']}

	args_raw = request.params.decode().dict
	args = {i: args_raw[i][0] for i in args_raw}

	if 'access_token' in args_raw:
		access_token = args_raw['access_token'][0]
	else:
		print('returned')
		return '400 need access_token.\nYou can get it with /create_api_token?short_name=<short_name>[&author_name=<author_name>&author_url=<author_url>]'

	kwargs.update(args)
	kwargs = {i: kwargs[i] for i in ['title', 'author', 'text']}

	for i in ['title', 'author', 'text']:
		if kwargs[i] == None:
			return f'field "{i}" cant be empty' #418 :)

	graph = TelegraphPoster(access_token)
	return graph.post(**kwargs)


app.run(host='0.0.0.0', port=8080)
