from app import app

if __name__ == "__app__":
    app.run(debug=True)

# For WSGI deployment
def application(environ, start_response):
    return app(environ, start_response)