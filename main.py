import bottle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_schema import UserRegistration

app = bottle.Bottle()

engine = create_engine('sqlite:///user_data.db')
UserRegistration.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


@app.route('/register', method='GET')
def register_form():
    return '''
        <form action="/register" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            Email: <input name="email" type="text" />
            <input type="submit" value="Register" />
        </form>
    '''

@app.route('/register', method='POST')
def register():
    user_name = bottle.request.forms.get('username')
    password = bottle.request.forms.get('password')
    email = bottle.request.forms.get('email')

    session = Session()
    user = UserRegistration(username=user_name, password=password, email=email)
    session.add(user)
    session.commit()
    session.close()

    return f'User {username} registered successfully.'

@app.route('/users')
def user_list():
    session = Session()
    users = session.query(UserRegistration).all()
    user_data = [{'id': user.id, 'username': user.username, 'password': user.password, 'email': user.email} for user in users]

    return {'users': user_data}
    session.close()

if __name__ == '__main__':
    bottle.run(app, host='localhost', port=8080, debug=True)