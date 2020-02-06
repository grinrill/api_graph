from bottle import Bottle, request
import json
from html_telegraph_poster import TelegraphPoster

app = Bottle()

graph = TelegraphPoster()

print('hhhhhhhh')

@app.get('/create_api_token')
def create_api_token():
	kwargs = {i: None for i in ['short_name', 'author_name', 'author_url']}

	args_raw = request.params.decode().dict
	args = {i: args_raw[i][0] for i in args_raw}

	kwargs.update(args)
	kwargs = {i: kwargs[i] for i in ['short_name', 'author_name', 'author_url']}

	if kwargs['author_name'] == None:
		return '400 need author_name' #418 :)

	return graph.create_api_token(**kwargs)


@app.get('/post')
def post():
	kwargs = {i: None for i in ['title', 'author', 'text']}

	args_raw = request.params.decode().dict
	args = {i: args_raw[i][0] for i in args_raw}

	if 'access_token' in args_raw:
		access_token = args_raw['access_token'][0]
	else:
		return '''400 need access_token.
		You can get it with /create_api_token?short_name=<short_name>[&author_name=<author_name>&author_url=<author_url>]'''
	graph = TelegraphPoster(access_token)

	kwargs.update(args)
	kwargs = {i: kwargs[i] for i in ['title', 'author', 'text']}

	for i in ['title', 'author', 'text']:
		if kwargs[i] == None:
			return f'field "{i}" cant be empty' #418 :)

	print(graph)
	post = graph.post(**kwargs)
	post['state'] = vars(graph)
	return post


@app.get('/edit')
def edit():
	kwargs = {i: None for i in ['title', 'author', 'text']}

	args_raw = request.params.decode().dict
	args = {i: args_raw[i][0] for i in args_raw}

	if 'access_token' in args_raw:
		access_token = args_raw['access_token'][0]
	else:
		return '''400 need access_token.
		You can get it with /create_api_token?short_name=<short_name>[&author_name=<author_name>&author_url=<author_url>]'''
	graph = TelegraphPoster(access_token)

	if 'state' in args_raw:
		params = args_raw['state'][0]
		for k, v in json.loads(params).items():
			graph.__setattr__(k, v)
	else: 
		return '''400 need state.
		You can get it with /post?title=<title>&author=<author>&text=<text>&access_token=<access_token>'''

	# if 'tph_uuid' in args_raw:
	# 	graph.tph_uuid = args_raw['tph_uuid'][0]
	# else:
	# 	return '''400 need tph_uuid.
	# 	You can get it with /post?title=<title>&author=<author>&text=<text>&access_token=<access_token>'''
	
	# if 'path' in args_raw:
	# 	graph.path = args_raw['path'][0]
	# else:
	# 	return '''400 need path.
	# 	You can get it with /post?title=<title>&author=<author>&text=<text>&access_token=<access_token>'''

	# if 'page_id' in args_raw:
	# 	graph.page_id = args_raw['page_id'][0]
	# else:
	# 	return '''400 need page_id.
	# 	You can get it with /post?title=<title>&author=<author>&text=<text>&access_token=<access_token>'''
	
	kwargs.update(args)
	kwargs = {i: kwargs[i] for i in ['title', 'author', 'text']}

	print(graph.path)
	return graph.edit(**kwargs)

app.run(host='0.0.0.0', port=8080)