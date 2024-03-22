from flask import Flask, render_template
from .models import DB, User
from .twitter import add_or_update_user


def add_all_to_db(data):
    for item in data:
        if item:
            DB.session.add(item)


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)

    @app.route("/")
    def root():
        users = User.query.all()
        print(users)
        return render_template('base.html', title="Home", users=users)

    @app.route("/reset")
    def reset():
        DB.drop_all()

        DB.create_all()

        return render_template('base.html', title="Reset")

    @app.route('/populate')
    def populate():
        mock_users = [
            'calebhicks',
            'elonmusk',
            'rrherr',
            'SteveMartinToGo',
            'alyankovic',
            'NASA',
            'jkhowland',
            'Austen',
            'common_squirrel',
            'KenJennings',
            'ConanOBrien',
            'big_ben_clock',
            'IAM_SHAKESPEARE',
        ]

        for mock in mock_users:
            add_or_update_user(mock)

        users = User.query.all()

        return render_template('base.html', title="populate", users=users)

    @app.route('/update')
    def update():
        users = User.query.all()
        usernames = [user.username for user in users]
        print(usernames)

        for username in usernames:
            add_or_update_user(username)

        return render_template('base.html', title='update', users=users)

    return app


# ryan = User(id=1, username='ryan')
# bernie = User(id=2, username='bernie')
# bethany = User(id=3, username='bethany')

# tweet1 = Tweet(id=1, text='tweet number 1', user_id=1, user=ryan)
# tweet2 = Tweet(id=2, text='tweet number 2', user_id=1, user=ryan)
# tweet3 = Tweet(id=3, text='tweet number 3', user_id=2, user=bernie)
# tweet4 = Tweet(id=4, text='tweet number 4', user_id=2, user=bernie)
# tweet5 = Tweet(id=5, text='tweet number 5', user_id=3, user=bethany)
# tweet6 = Tweet(id=6, text='tweet number 6', user_id=3, user=bethany)

# users = [ryan, bernie, bethany]
# tweets = [tweet1, tweet2, tweet3, tweet4, tweet5, tweet6]

# for user, tweet in itertools.zip_longest(users, tweets):
#     add_all_to_db([user, tweet])

# DB.session.commit()
