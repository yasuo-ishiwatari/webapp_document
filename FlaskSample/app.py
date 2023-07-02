# $env:FLASK_APP = "app"
# $env:FLASK_DEBUG=1
# $env:FLASK_RUN_PORT = 
# flask run
from flask import Flask,render_template,request,redirect,url_for
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,EmailField,SubmitField,validators
from werkzeug.security import generate_password_hash,check_password_hash



LOGIN_ID = "login"
LOGIN_USER = "ichiro"
PASSWORD = "pass1234"

password_hash = generate_password_hash(PASSWORD,method='sha256')
print(password_hash)

app = Flask(__name__)

app.secret_key = 'database_sample%%&&&_key'

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self,user_id):
        self.id = user_id

class LoginForm(FlaskForm):
    name = StringField('ユーザー名', \
                validators=[validators.DataRequired(),validators.length(min=3,max=15)], \
                name='username',id='username')
    mail = EmailField('メールアドレス',
                validators=[validators.DataRequired()],
                name='email',id='email')
    password = PasswordField('パスワード',
                validators=[validators.DataRequired(),validators.length(min=8,max=16)],
                name='password',id='password')
    submit = SubmitField('ログイン')
    
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/page2")
def page2():
    return render_template('page2.html')

@app.route("/page3")
def page3():
    return render_template('page3.html')

# =======================================================================

form_values = {}
form_values["string_input"] = ""
form_values["password_input"] = ""
form_values["radioA_input"] = "A1"
form_values["radioB_input"] = "B1"
form_values["checkbox1_input"] = ""
form_values["checkbox2_input"] = ""
form_values["date"] = "2000-01-01"
form_values["email"] = ""
form_values["number"] = "6"
form_values["range"] = "50"
form_values["select"] = "RED"
form_values["select2"] = ""


# =======================================================================

@app.route("/form_sample",methods=['GET','POST'])
def form_sample():
    global form_values

    colors = []
    colors.append("BLACK")
    colors.append("WHITE")
    colors.append("RED")
    colors.append("BLUE")
    colors.append("YELLOW")
    colors.append("GREEN")
    colors.append("BROWN")
    colors.append("ORANGE")
    colors.append("GRAY")

    pages = ["TOP","page2","page3"]


    if request.method=='POST':
        form_values['string_input'] = request.form.get('string_input')
        form_values['password_input'] = request.form.get('password_input')
        print("password input = {}".format(form_values['password_input']))
        form_values['radioA_input'] = request.form.get('radioA_input')
        form_values['radioB_input'] = request.form.get('radioB_input')    
        form_values["checkbox1_input"] = request.form.get('checkbox1')
        form_values["checkbox2_input"] = request.form.get('checkbox2')
        print("file name = {}".format(request.form.get('file_input')))
        form_values["date"] = request.form.get('date')
        form_values["email"] = request.form.get('email')
        form_values["number"] = request.form.get('number')
        form_values["range"] = request.form.get('range')
        print("test = {}".format(request.form.get('textarea')))
        form_values["select"] = request.form.get('color_select')

        next_page = request.form.get('page_select')

        if next_page == "TOP":
            return redirect(url_for('index'))

        if next_page == "page2":
            return redirect(url_for('page2'))

        if next_page == "page3":
            return redirect(url_for('page3'))                


    else:
        form_values['string_input'] = "空欄"
        form_values['password_input'] = ""
        form_values['radioA_input'] = "A1"
        form_values['radioB_input'] = "B1"
        form_values["checkbox1_input"] = ""
        form_values["checkbox2_input"] = ""
        form_values["date"] = "2000-01-01"
        form_values["email"] = ""
        form_values["number"] = "6"
        form_values["range"] = "50"
        form_values["select"] = "RED"
        form_values["select2"] = ""
            

    return render_template('form_sample.html',form_values=form_values,colors=colors,pages=pages)

@app.route("/embed_sample",methods=['GET','POST'])
def embed_sample():
    
    command = ""
    msg = ""

    fruits = ["apple","orange","grape"]

    if request.method == 'POST':
        command = "P"
        msg = "Post Command 受信"    
    else:
        command = "G"
        msg = "GET Command 受信"   

    return render_template('embed_sample.html', command=command,msg=msg,fruits=fruits)

@app.route("/login_sample",methods=['GET','POST'])
def login_sample():
    form2 = LoginForm()
    if request.method == 'POST':
        if form2.validate_on_submit():
            username = request.form.get('username')
            email = request.form.get('mail')
            password = request.form.get('password')
            print(username,email,password)    
            
            if username == LOGIN_USER and check_password_hash(password_hash,password):
                user = User(username)
                login_user(user)
                return redirect(url_for('member'))

    return render_template('login_sample.html',form2=form2)

@app.route('/member')
@login_required
def member():

    return render_template('memberpage.html')

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login_sample'))  


@app.route('/logout_sample')
@login_required
def logout_sample():
    logout_user()
    return redirect(url_for('index'))   
