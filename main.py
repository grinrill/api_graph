from bottle import Bottle, request
import json
from html_telegraph_poster import TelegraphPoster
from html_telegraph_poster.html_to_telegraph import _upload_via_api as upload

app = Bottle()

graph = TelegraphPoster()

print('hhhhhhhh')

@app.get('/create_api_token')
@app.post('/create_api_token')
def create_api_token():
	kwargs = {i: None for i in ['short_name', 'author_name', 'author_url']}

	args_raw = request.params.decode().dict
	args = {i: args_raw[i][0] for i in args_raw}

	kwargs.update(args)
	kwargs = {i: kwargs[i] for i in ['short_name', 'author_name', 'author_url']}

	if kwargs['author_name'] == None:
		return '400 need author_name' #418 :)
	if kwargs['short_name'] == None:
		return '400 need short_name' #418 :)

	return graph.create_api_token(**kwargs)


@app.get('/post')
@app.post('/post')
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

@app.get('/edit')
@app.post('/edit')
def edit():
	kwargs = {i: None for i in ['title', 'author', 'text']}

	args_raw = request.params.decode().dict
	args = {i: args_raw[i][0] for i in args_raw}

	if 'access_token' in args_raw:
		access_token = args_raw['access_token'][0]
	else:
		print('returned')
		return '400 need access_token.\nYou can get it with /create_api_token?short_name=<short_name>[&author_name=<author_name>&author_url=<author_url>]'

	if 'path' in args_raw:
		path = f"{args_raw['access_token'][0]}"
	else:
		print('returned')
		return '400 need path.\nYou can get it with /create_api_token?short_name=<short_name>[&author_name=<author_name>&author_url=<author_url>]'


	kwargs.update(args)
	kwargs = {i: kwargs[i] for i in ['title', 'author', 'text']}

	for i in ['title', 'author', 'text']:
		if kwargs[i] == None:
			return f'field "{i}" cant be empty' #418 :)

	res=upload(**kwargs, path=path, access_token=access_token)
	return res

app.run(host='0.0.0.0', port=8080)