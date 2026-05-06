from app.views import Routes

routes = Routes()
app = routes.create_app()

if __name__ == '__main__':
    app.run()
