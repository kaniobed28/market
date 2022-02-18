import email
from flask import Flask, jsonify,redirect,url_for,render_template,request
from flask_login import login_required, login_user,logout_user,current_user,UserMixin,LoginManager
from flask_sqlalchemy import SQLAlchemy
from numpy import product
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from flask_restful import Api,Resource

app=Flask(__name__)
api = Api(app)


# app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://sql6473290:cyQZPPevB6@sql6.freemysqlhosting.net/sql6473290'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db = SQLAlchemy(app)
app.secret_key = "this is my secrete key"

#Make sure that flask_login and bcrypt are installed
class Users(db.Model, UserMixin):
    """Model for user accounts."""
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String(255),
                         nullable=False,
                         unique=False)
    email = db.Column(db.String(40),
                      unique=False,
                      nullable=False)
    password = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=False)
    phone_number = db.Column(db.Integer,
                         nullable = False)
    profile_pic_path = db.Column(db.String(200),
                         )

    product_ref = db.relationship("Product",backref = 'product_backref')
                                        
    def __repr__(self):
        return '<User {}>'.format(self.username)


class Product(db.Model,UserMixin):
    id = db.Column(db.Integer,
                    primary_key=True
    )
    product_name =  db.Column(db.String(40),
                      unique=False,
                      nullable=False)
    product_desc =  db.Column(db.String(40),
                      unique=False,
                      nullable=False)
    product_location = db.Column(db.String(40),
                      unique=False,
                      nullable=False)
    product_prince = db.Column(db.Integer,
                      unique=False,
                      nullable=False)
    product_image_path =  db.Column(db.String(255),
                      unique=False,
                      nullable=False)
    user_id  = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )

#Position all of this after the db and app have been initialised
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def user_loader(users_id):
    #TODO change here
    return Users.query.get(users_id)

data = {
    "username":"uname",
    'email':"uemail",
    'password':'upassword'
}
class Login(Resource):
    
    def post(self):
        username = request.json['username']
        email = request.json['email']
        password  = request.json['password']
        phone_number  = request.json['phone_number']
        new_user = Users(username = username,email = email,password = password,phone_number = phone_number)
        db.session.add(new_user)
        db.session.commit()
        user_data = Users.query.filter_by(email = email).first()
        login_user(user_data)
        return jsonify({"message":200})

api.add_resource(Login,"/login")

class HomePage(Resource):
    def get(self):
        data = Users.query.all()
        fdata = []
        for user in data:
            # data['username'] = user.username
            # data['password'] = user.password
            # data['email'] = user.email
            # data['phone_number'] = user.phone_number
            username = user.username
            gdata = {
                    username:{
                        "email":user.email,
                        "phone_number":user.phone_number
                        }
            }
            fdata.append(gdata)

        return fdata

api.add_resource(HomePage,"/logout")          


db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        return {"message":"not registered"}
    return render_template('index.html')

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(debug=True)