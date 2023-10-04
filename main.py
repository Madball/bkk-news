from dotenv import load_dotenv
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from sqlalchemy.sql.expression import func
from typing import Annotated
from os import getenv
import google_auth_oauthlib.flow
import uvicorn

from db import open_db, Article

# Read configuration parameters
load_dotenv()

# List of authentication tokens from Google
auth_states = []

if __name__ == '__main__':
	# Read config
	host_name = getenv('HOST_NAME')
	host_port = int(getenv('HOST_PORT', 7888))

	# Start application
	app = FastAPI()


	def check_auth():
		pass


	@app.get('/')
	async def home(state: str | None = None):
		return JSONResponse({'message': 'To be implemented '})


	@app.get('/auth')
	async def google_auth():
		# Setup Google auth
		flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json', scopes=['openid'])
		flow.redirect_uri = f'http://{host_name}:{host_port}'
		authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')

		return JSONResponse({'url': authorization_url})


	@app.get('/news')
	async def news():
		db = open_db()
		articles = db.query(Article).order_by(Article.created_at).all()

		return JSONResponse([item.as_dict() for item in articles])


	@app.post('/article')
	async def article_add(title: Annotated[str, Body()], body: Annotated[str, Body()], picture_url: Annotated[str | None, Body()] = None):
		# data=request.json()
		db = open_db()
		article = Article()
		article.author = 'none'
		article.title = title
		article.body = body
		article.picture_url = picture_url
		db.add(article)
		db.commit()

		return JSONResponse(article.as_dict())


	@app.put('/article/{article_id}')
	async def article_update(article_id: int, title: Annotated[str, Body()], body: Annotated[str, Body()], picture_url: Annotated[str | None, Body()] = None):
		db = open_db()
		article = db.query(Article).filter(Article.id == article_id).first()
		article.title = title
		article.body = body
		article.picture_url = picture_url
		article.updated_at = func.now()
		db.commit()

		return JSONResponse(article.as_dict())


	@app.delete('/article/{article_id}')
	async def article_delete(article_id: int):
		db = open_db()
		db.query(Article).filter(Article.id == article_id).delete()
		db.commit()

		return JSONResponse({'message': 'Item deleted'})


	# Serve the website
	uvicorn.run(app, host=host_name, port=host_port)
