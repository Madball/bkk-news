# Basic usage
- Authenticate via Google by calling /auth (GET) and visiting the authentication URL in the response
- Send the received token via Bearer auth in request header
- List all articles at /news (GET)
- Create a new article at /article (POST). Send parameters as a JSON object
- Update an existing article at /article/:id (PUT). Send parameters as a JSON object
- Delete an existing article at /article/:id (DELETE)

# JSON article example
```
{
	"title": "Title of article",
	"body": "Lorem ipsum dolor ..",
	"picture_url": "https://example.com/demo.jpeg"
}
```

# Google auth
Returns consent screen URL in response when _/auth_ endpoint is called. Later flow not implemented yet.
