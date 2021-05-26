from src import create_app, db
from src.database.models import User, Watchlist
# import config
app = create_app()

if __name__ == '__main__':
    # db.create_all()
    app.run()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Watchlist': Watchlist}
