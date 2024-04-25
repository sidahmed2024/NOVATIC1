from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import datetime
import sqlite3
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, EmailField, TelField
#from flask_wtf import StringField, PasswordField, SubmitFiled
from wtforms.validators import input_required, length, ValidationError
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager= LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 4) Initialize a Flask App to use for the DATABASE
#db.init_app(app)




# 4) important: respect capital
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           input_required(), length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             input_required(), length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'Identifiant est déjà ustisé! choisir un autre identifiant')



class LoginForm(FlaskForm):
    username = StringField(validators=[
                           input_required(), length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             input_required(), length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route("/traitement", methods=["POST", "GET"])
def Traitement():
    if request.method=="POST":
            donnees = request.form
            nom = donnees.get('nom')
            psw = donnees.get('psw')
            if nom == 'Admin1' and psw=='AdminAdmin':
                return render_template("traitement.html", nom_user=nom)
            else:
                return render_template("traitement.html")
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)







#@app.route("/heure")
#def heure():
 #   date_heure=datetime.datetime.now()
  #  h=date_heure.hour
   # m=date_heure.minute
    #s=date_heure.second
    #print(h,m,s)
    #return render_template("heure.html", heure=h, minute=m, seconde=s)

#    liste_eleves=[
    #    {'nom':'abbou', 'prenom':'Sid Ahmed', 'classe':'3M1'},
    #    {'nom':'bouhafs', 'prenom':'Rahma', 'classe':'3S2'},
    #    {'nom':'Reda', 'prenom':'Yassine', 'classe':'1L1'},
    #    {'nom':'Gharbi', 'prenom':'Mohamed', 'classe':'3M2'},
    #    {'nom':'Bekkouch', 'prenom':'Houda', 'classe':'3M1'}
#    ]

#    @app.route("/eleves")
#    def eleves():
    #    classe=request.args.get('c')
    #    if classe:
      #    eleves_selected=[eleve for eleve in liste_eleves if eleve['classe']==classe]
    #    else:
        #    eleves_selected=[]

    #    return render_template("eleves.html",eleves=eleves_selected)
