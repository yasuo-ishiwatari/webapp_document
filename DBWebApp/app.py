# $env:FLASK_APP = "app"
# $env:FLASK_DEBUG=1
# $env:FLASK_RUN_PORT = 
# flask run
from flask import Flask, render_template,request,redirect,url_for
from flask_login import LoginManager,UserMixin,login_required,login_user,logout_user
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,EmailField,SubmitField,validators
import os
import datetime

from define import Get_Prefect
from define import Get_Year
from define import Get_Month
from define import Get_Day

from database import initDatabase
from database import check_account
from database import add_member_account
from database import get_profile
from database import get_profile_member
from database import get_profile_condition
from database import add_member_profile
from database import update_member_profile
from database import delete_member
from database import ADMIN_USER_NAME

from account import check_new_account

from register import check_register_info
from register import get_age_from_birthday
from register import check_record_condition_info

#--------------------------------
loginUser = ""

register_info = {}
register_info['user'] = ""
register_info['fname'] = ""
register_info['gname'] = ""
register_info['year'] = ""
register_info['month'] = ""
register_info['day'] = ""
register_info['gender'] = "male"
register_info['address'] = ""

record_condition = {}
record_condition['registerd'] = "OFF"
record_condition['registerd_year_start'] = 2000
record_condition['registerd_year_end'] = 2000
record_condition['registerd_month_start'] = 1
record_condition['registerd_month_end'] = 1
record_condition['registerd_day_start'] = 1
record_condition['registerd_day_end'] = 1
record_condition['birth'] = "OFF"
record_condition['birth_year_start'] = 2000
record_condition['birth_year_end'] = 2000
record_condition['birth_month_start'] = 1
record_condition['birth_month_end'] = 1
record_condition['birth_day_start'] = 1
record_condition['birth_day_end'] = 1
record_condition['male'] = "ON"
record_condition['female'] = "ON"
record_condition['address'] = ""
#------------------------------- 


dbEnable = False

app = Flask(__name__)

app.secret_key = b'q2a s34 (3kjaHBGHJ2())z\n\xec]/'
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self,user_id):
        self.id = user_id

@login_manager.user_loader
def user_loader(user_id):
    return User(user_id)        

class LoginForm(FlaskForm):
    name = StringField('ユーザー名',validators=[validators.DataRequired()],id='username',name='username',default='ユーザー名')
    password = StringField('パスワード',validators=[validators.DataRequired()],id='password',name='password',default='パスワード')
    submit = SubmitField('ログイン')

def clear_profile():
    global register_info    
    register_info['user'] = ""
    register_info['fname'] = ""
    register_info['gname'] = ""
    register_info['year'] = ""
    register_info['month'] = ""
    register_info['day'] = ""
    register_info['gender'] = "male"
    register_info['address'] = ""

@app.route('/')
def index():
    global dbEnable
    dbEnable = initDatabase()
    return render_template('index.html',dbEnable=dbEnable)

@app.route('/general',methods=['GET','POST'])
def general_person():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html',SignUp = True,form = form)
    else:
        if form.validate_on_submit():
            username = request.form.get('username')
            password = request.form.get('password')
            print(username,password)

            if username == ADMIN_USER_NAME:
                return render_template('login.html',SignUp = True,form = form)

            res = check_account(username,password)
            if res == False:
                return render_template('login.html',SignUp = True,form = form)
            print("login success")
            global loginUser
            loginUser = username
        
            user = User(username) 
            login_user(user) 
        
            if get_profile_member(username) == None:
                clear_profile()
                return redirect(url_for("register"))            
            print("profile exist")
            return redirect(url_for("info"))
        else:
            return render_template('login.html',SignUp = True,form = form)

@app.route('/admin',methods=['GET','POST'])
def admin_person():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html',SignUp = False, form = form )
    else:
        if form.validate_on_submit():
            username = request.form.get('username')
            password = request.form.get('password')
            print(username,password)

            if username != ADMIN_USER_NAME:
                return render_template('login.html',SignUp = False, form = form)

            if check_account(username,password) == False:
                return render_template('login.html',SignUp = False, form = form)
            print("login success")
            global loginUser
            loginUser = username

            user = User(username) 
            login_user(user)

            return redirect(url_for("record"))
        
        else:
            return render_template('login.html',SignUp = False, form = form )


@app.route('/returntop')
def return_top():
    return redirect(url_for("index"))

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')    
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        password_conf = request.form.get('password_conf')
        print(username,password,password_conf)       
        if check_new_account(username,password,password_conf) == False:
            return render_template('signup.html') 
        if add_member_account(username,password) == False:
            return render_template('signup.html') 

        clear_profile()
        return redirect(url_for("general_person"))

@app.route('/returnlogin')
def return_login():
    return redirect(url_for("general_person"))


@app.route('/register',methods=['GET','POST'])
@login_required
def register():

    if loginUser == ADMIN_USER_NAME:
        logout_user()
        return redirect(url_for('index'))   

    global register_info
    BirthYear = Get_Year()
    BirthMonth = Get_Month()
    BirthDay = Get_Day()
    Prefect = Get_Prefect()
    errmsg = ""
    if request.method == 'GET':
        return render_template('register.html',BirthYear=BirthYear,BirthMonth=BirthMonth,BirthDay=BirthDay,Prefect=Prefect,register_info=register_info,errmsg=errmsg)
    else:
        register_info['user'] = loginUser
        register_info['fname'] = request.form.get('familyname')
        register_info['gname'] = request.form.get('givenname')
        register_info['year'] = request.form.get('year')
        register_info['month'] = request.form.get('month')
        register_info['day'] = request.form.get('day')
        register_info['gender'] = request.form.get('gender')
        register_info['address'] = request.form.get('address')
        print(register_info)
        res,prof_data = check_register_info(register_info)
        print(prof_data)
        if res == "":
            result = add_member_profile(prof_data)
            if result == True:
                return redirect(url_for('info'))
            errmsg = ""    
        else:
            errmsg = res
        
        return render_template('register.html',BirthYear=BirthYear,BirthMonth=BirthMonth,BirthDay=BirthDay,Prefect=Prefect,register_info=register_info,errmsg=errmsg)


@app.route('/info',methods=['GET'])
@login_required
def info():
    if loginUser == ADMIN_USER_NAME:
        logout_user()
        return redirect(url_for('index'))       

    Register_Info = {}

    result = get_profile_member(loginUser)
    if result != None:
        prof = result[0]
        global register_info
        register_info['user'] = loginUser
        register_info['fname'] = prof[3]
        register_info['gname'] = prof[4]
        str_date = "{}".format(prof[5])
        birthday = datetime.datetime.strptime(str_date,'%Y-%m-%d')
        register_info['year'] = "{}".format(birthday.year)
        register_info['month'] = "{}".format(birthday.month)
        register_info['day'] = "{}".format(birthday.day)
        if prof[6] == '1':
            register_info['gender'] = "male"
        else:
            register_info['gender'] = "female"
        register_info['address'] = prof[7]
        print("from database profile table")

    Register_Info['name'] = "{}{}".format(register_info['fname'],register_info['gname'])
    Register_Info['birthday'] = "{}/{}/{}".format(register_info['year'],register_info['month'],register_info['day'])
    Register_Info['age'] = get_age_from_birthday(birthday)
    if register_info['gender'] == "male":
        Register_Info['gender'] = "男性"
    else:
        Register_Info['gender'] = "女性"
    Register_Info['address'] = register_info['address']

    return render_template('info.html',Register_Info = Register_Info)


@app.route('/edit',methods=['GET','POST'])
@login_required
def edit():
    if loginUser == ADMIN_USER_NAME:
        logout_user()
        return redirect(url_for('index')) 

    global register_info
    BirthYear = Get_Year()
    BirthMonth = Get_Month()
    BirthDay = Get_Day()
    Prefect = Get_Prefect()
    errmsg = ""
    if request.method == 'GET':
        return render_template('edit.html',BirthYear=BirthYear,BirthMonth=BirthMonth,BirthDay=BirthDay,Prefect=Prefect,register_info=register_info,errmsg=errmsg)    
    else:
        register_info['fname'] = request.form.get('familyname')
        register_info['gname'] = request.form.get('givenname')
        register_info['year'] = request.form.get('year')
        register_info['month'] = request.form.get('month')
        register_info['day'] = request.form.get('day')
        register_info['gender'] = request.form.get('gender')
        register_info['address'] = request.form.get('address')
        print(register_info)
        res,prof_data = check_register_info(register_info)
        print(prof_data)
        if res == "":
            result = update_member_profile(prof_data)
            if result == True:
                return redirect(url_for('info'))
            errmsg = ""    
        else:
            errmsg = res

        return render_template('edit.html',BirthYear=BirthYear,BirthMonth=BirthMonth,BirthDay=BirthDay,Prefect=Prefect,register_info=register_info,errmsg=errmsg)  

@app.route('/quit')
@login_required
def quit():
    if loginUser == ADMIN_USER_NAME:
        logout_user()
        return redirect(url_for('index'))   
    
    res = delete_member(loginUser)
    if res == True:
        print("login user is deleted")
    else:
        print("login user is not deleted")

    logout_user()
    return redirect(url_for('index'))   


@app.route('/record',methods=['GET','POST'])
@login_required
def record():

    if loginUser != ADMIN_USER_NAME:
        logout_user()
        return redirect(url_for('index'))   

    global record_condition

    if request.method == 'GET':
        record_condition['registerd'] = "OFF"
        record_condition['registerd_year_start'] = ""
        record_condition['registerd_year_end'] = ""    
        record_condition['registerd_month_start'] = ""
        record_condition['registerd_month_end'] = ""
        record_condition['registerd_day_start'] = ""
        record_condition['registerd_day_end'] = ""
        record_condition['birth'] = "OFF"
        record_condition['birth_year_start'] = ""
        record_condition['birth_year_end'] = ""    
        record_condition['birth_month_start'] = ""
        record_condition['birth_month_end'] = ""
        record_condition['birth_day_start'] = ""
        record_condition['birth_day_end'] = ""
        record_condition['male'] = "ON"
        record_condition['female'] = "ON"
        record_condition['address'] = ""
        member_profiles = get_profile()            
    else:
        registerd_enable = request.form.get('registerd_enable')
        if registerd_enable == "on":
            record_condition['registerd'] = "ON"
        else:
            record_condition['registerd'] = "OFF"

        male = request.form.get('male')
        female = request.form.get('female')
        if male != "on" and female != "on":
            male = "on"
            female = "on"

        if male == "on":
            record_condition['male'] = "ON"
        else:
            record_condition['male'] = "OFF"
        if female == "on":
            record_condition['female'] = "ON"
        else:
            record_condition['female'] = "OFF"

        registerd_year_start = request.form.get('registerd_year_start')
        registerd_month_start = request.form.get('registerd_month_start')
        registerd_day_start = request.form.get('registerd_day_start')
        registerd_year_end = request.form.get('registerd_year_end')
        registerd_month_end = request.form.get('registerd_month_end')
        registerd_day_end = request.form.get('registerd_day_end')

        record_condition['registerd_year_start'] = registerd_year_start
        record_condition['registerd_year_end'] = registerd_year_end    
        record_condition['registerd_month_start'] = registerd_month_start
        record_condition['registerd_month_end'] = registerd_month_end
        record_condition['registerd_day_start'] = registerd_day_start
        record_condition['registerd_day_end'] = registerd_day_end

        birth_enable = request.form.get('birth_enable')
        if birth_enable == "on":
            record_condition['birth'] = "ON"
        else:
            record_condition['birth'] = "OFF"

        birth_year_start = request.form.get('birth_year_start')
        birth_month_start = request.form.get('birth_month_start')
        birth_day_start = request.form.get('birth_day_start')
        birth_year_end = request.form.get('birth_year_end')
        birth_month_end = request.form.get('birth_month_end')
        birth_day_end = request.form.get('birth_day_end')

        record_condition['birth_year_start'] = birth_year_start
        record_condition['birth_year_end'] = birth_year_end    
        record_condition['birth_month_start'] = birth_month_start
        record_condition['birth_month_end'] = birth_month_end
        record_condition['birth_day_start'] = birth_day_start
        record_condition['birth_day_end'] = birth_day_end
        
        address = request.form.get('address')
        record_condition['address'] = address

        record_condition_info = check_record_condition_info(record_condition)
        print(record_condition_info) 
        member_profiles = get_profile_condition(record_condition_info)                  

    Records = []

    
    if member_profiles != None:
        idx = 0
        for member_profile in member_profiles:
            record = {}
            record["number"] = "{:0>4}".format(idx+1)
            record["uname"] = member_profile[1]
            record["registerd"] = "{}".format(member_profile[2])
            record["name"] = "{}{}".format(member_profile[3],member_profile[4])
            record["birthday"] = "{}".format(member_profile[5])
            if member_profile[6] == '1':
                record["gender"] = "男性"
            else:
                record["gender"] = "女性"
            record["address"] = member_profile[7]
            Records.append(record)
            idx += 1

    return render_template('record.html',Records = Records,record_condition = record_condition)


@app.route('/logout_general')
@login_required
def logout_general():
     logout_user()
     return redirect(url_for('index'))

@app.route('/logout_admin')
@login_required
def logout_admin():
     logout_user()
     return redirect(url_for('index'))





if __name__=='__main__':
    # ローカルマシンでは、アプリの Web サーバーは、開いていて未予約であれば、どのポートでもリッスンできる
    # しかし、Heroku では、特定の​ポートをリッスンする必要がある
    # この特定のポートは、PORT​ 環境変数で指定される
    # Heroku で Web サーバーが起動したら、PORT​ で指定されているポート番号でリッスンしていることを確認する
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
