import psycopg2
from werkzeug.security import generate_password_hash,check_password_hash


connection = None
cursor = None

DB_USER = "admin"
DB_PASSWORD = "pass"
DB_HOST = "127.0.0.1"
DB_PORT = 5432
DB_NAME = "memberdb"

# DB_USER = "admin"
# DB_PASSWORD = "uuPaLpJodCbahwbi6QbUk1n3VRYZCqHU"
# DB_HOST = "dpg-ch9meid269v0obb7h8q0-a"
# DB_PORT = 5432
# DB_NAME = "memberdb_t8wb"



ACCOUNT_TABLE = "account_table"
PROFILE_TABLE = "prof_table"

ADMIN_USER_NAME = "admin"
ADMIN_PASSWORD = "admin00"

MAX_USERNAME_ACCOUNT = 20
MAX_PASSWORD_ACCOUNT = 128

MALE_BIT = B'1'
FEMALE_BIT = B'0'



#===========================================================================================
#                                   データベ－スへの接続
#===========================================================================================
def connect_to_database():
    global connection
    global cursor
    try:
        connection = psycopg2.connect(user=DB_USER,password=DB_PASSWORD,host=DB_HOST,port=DB_PORT,database=DB_NAME)
        print("データベ－ス:{}への接続に成功".format(DB_NAME))
    except:
        print("データベ－ス:{}への接続に失敗".format(DB_NAME))
        return False

    try:
        cursor = connection.cursor()
        print("Cursor オブジェクトの作成に成功")
    except:
        print("Cursor オブジェクトの作成に失敗")        
        return False
    
    return True

#===========================================================================================
#                                   SQLの実行
#===========================================================================================
def execute_sql(sql,commit_flag):
    print("SQL : {}".format(sql))
    try:
        cursor.execute(sql)
        if commit_flag == True:
            connection.commit()
        print("実行成功")
        return True
    except:
        print("実行失敗")
        return False

#===========================================================================================
#                                   テーブル名の取得
#===========================================================================================
def get_table_name():
    tables = None
    str_sql = """SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"""     
    if execute_sql(str_sql,False) == False:
        return False,tables
    
    tables = cursor.fetchall()
    if len(tables) == 0:
        return True,tables
    
    return True,tables

#===========================================================================================
#                                   アカウントテーブルの作成
#===========================================================================================
def create_account_table():
    str_sql = "CREATE TABLE {} (".format(ACCOUNT_TABLE)
    str_sql = "{}   id integer NOT NULL,".format(str_sql)
    str_sql = "{}   user_name varchar(20) NOT NULL UNIQUE,".format(str_sql)
    str_sql = "{}   password varchar(128) NOT NULL,".format(str_sql)
    str_sql = "{}   PRIMARY KEY ( id )".format(str_sql)
    str_sql = "{});".format(str_sql)							
    if execute_sql(str_sql,True) == False:
        return False
    
    return True

#===========================================================================================
#                                   アカウントテーブルの取得
#===========================================================================================
def get_account_table():
    tables = None
    str_sql = "SELECT * FROM {};".format(ACCOUNT_TABLE)     
    if execute_sql(str_sql,False) == False:
        return tables
    
    tables = cursor.fetchall()
    if len(tables) == 0:
        return None
    
    return tables

#===========================================================================================
#                            アカウントテーブルから特定のメンバを取得
#===========================================================================================
def get_account_member(member):
    account = None
    str_sql = "SELECT id,user_name,password FROM {} WHERE user_name='{}';".format(ACCOUNT_TABLE,member)
    if execute_sql(str_sql,False) == False:
        return account    
    
    accounts = cursor.fetchall()
    if len(accounts) == 0:
        return account
    
    account = accounts[0]
    return account


#===========================================================================================
#                               アカウントテーブルへの追加
#===========================================================================================
def add_account(user_name,password):

    if user_name == "" or len(user_name) > MAX_USERNAME_ACCOUNT:
        return False

    if password == "" or len(password) > MAX_PASSWORD_ACCOUNT:
        return False

    tables = get_account_table()    
       
    if tables == None:
        id = 1
    else:
        ids = []
        for table in tables:
            print(table[0],table[1],table[2])
            ids.append(table[0])
        id = max(ids) + 1

    print(id,user_name,password)

    str_sql = "INSERT INTO {} (id,user_name,password)".format(ACCOUNT_TABLE)
    str_sql = "{}   VALUES ({},'{}','{}');".format(str_sql,id,user_name,password)
    result = execute_sql(str_sql,True)
    
    return result
        


#===========================================================================================
#                            アカウントテーブルから特定のメンバを削除
#===========================================================================================
def delete_account_member(user_name):

    str_sql = "DELETE FROM {} WHERE user_name='{}';".format(ACCOUNT_TABLE,user_name)
    result = execute_sql(str_sql,True)
    return result


#===========================================================================================
#                                   プロファイルテーブルの作成
#===========================================================================================
def create_prof_table():
    str_sql = "CREATE TABLE {} (".format(PROFILE_TABLE)
    str_sql = "{}   id integer NOT NULL,".format(str_sql)
    str_sql = "{}   user_name varchar(20) NOT NULL UNIQUE,".format(str_sql)
    str_sql = "{}   registerd_day date NOT NULL,".format(str_sql)
    str_sql = "{}   family_name varchar(10) NOT NULL,".format(str_sql)
    str_sql = "{}   given_name varchar(10) NOT NULL,".format(str_sql)
    str_sql = "{}   birthday date NOT NULL,".format(str_sql)
    str_sql = "{}   gender bit NOT NULL,".format(str_sql)
    str_sql = "{}   address varchar(10) NOT NULL,".format(str_sql)
    str_sql = "{}   PRIMARY KEY ( id )".format(str_sql)
    str_sql = "{});".format(str_sql)							
    if execute_sql(str_sql,True) == False:
        return False
    
    return True


#===========================================================================================
#                         プロファイルテーブルから全メンバを取得
#===========================================================================================
def get_profile():
    profile_info = None
    str_sql = "SELECT * FROM {};".format(PROFILE_TABLE)
    if execute_sql(str_sql,False) == False:
        return profile_info    
    
    profile_info = cursor.fetchall()
    if len(profile_info) == 0:
        return None

    print(profile_info)
    
    return profile_info


#===========================================================================================
#                         プロファイルテーブルから特定のメンバを取得
#===========================================================================================
def get_profile_member(member):
    profile_info = None
    str_sql = "SELECT * FROM {} WHERE user_name='{}';".format(PROFILE_TABLE,member)
    if execute_sql(str_sql,False) == False:
        return profile_info    
    
    profile_info = cursor.fetchall()
    if len(profile_info) == 0:
        return None

    print(profile_info)
    
    return profile_info


#===========================================================================================
#                                   プロファイルテーブルへの追加
#===========================================================================================
def add_member_profile(prof_data):

    user_name = prof_data['username']
    registerday = prof_data['registerday']
    fname = prof_data['fname']
    gname = prof_data['gname'] 
    birthday = prof_data['birthday']
    gender = prof_data['gender']
    address = prof_data['address']

    tables = get_profile_member(user_name)    
    if tables != None:
        return False

    tables = get_profile()
    if tables == None:
        id = 1
    else:
        ids = []
        for table in tables:
            print(table[0])
            ids.append(table[0])
        id = max(ids) + 1

    if gender == True:
        gender_bit = MALE_BIT
    else:
        gender_bit = FEMALE_BIT
    
    str_sql = "INSERT INTO {} (id,user_name,registerd_day,family_name,given_name,birthday,gender,address)".format(PROFILE_TABLE)
    str_sql = "{}   VALUES ({}".format(str_sql,id)
    str_sql = "{},'{}'".format(str_sql,user_name)
    str_sql = "{},TO_DATE('{}', 'YYYYMMDD')".format(str_sql,registerday)
    str_sql = "{},'{}','{}'".format(str_sql,fname,gname)
    str_sql = "{},TO_DATE('{}', 'YYYYMMDD')".format(str_sql,birthday)
    str_sql = "{},{},'{}');".format(str_sql,gender_bit,address)   
    result = execute_sql(str_sql,True)
    print(str_sql)

    return result
        

#===========================================================================================
#                                 プロファイルテーブルの更新
#===========================================================================================
def update_member_profile(prof_data):
    user_name = prof_data['username']
    registerday = prof_data['registerday']
    fname = prof_data['fname']
    gname = prof_data['gname'] 
    birthday = prof_data['birthday']
    gender = prof_data['gender']
    address = prof_data['address']

    tables = get_profile_member(user_name)    
    if tables == None:
        return False
 
    if gender == True:
        gender_bit = MALE_BIT
    else:
        gender_bit = FEMALE_BIT
    
    str_sql = "UPDATE {} SET family_name='{}',given_name='{}'".format(PROFILE_TABLE,fname,gname)
    str_sql = "{},birthday=TO_DATE('{}', 'YYYYMMDD')".format(str_sql,birthday)
    str_sql = "{},gender={},address='{}'".format(str_sql,gender_bit,address)
    str_sql = "{} WHERE user_name='{}';".format(str_sql,user_name)
    
    print(str_sql)
    result = execute_sql(str_sql,True)


    return result


#===========================================================================================
#                            プロファイルテーブルから特定のメンバを削除
#===========================================================================================
def delete_profile_member(user_name):

    str_sql = "DELETE FROM {} WHERE user_name='{}';".format(PROFILE_TABLE,user_name)
    result = execute_sql(str_sql,True)
    return result


#===========================================================================================
#                                   デ－タベ－ス初期化
#===========================================================================================
def initDatabase():
    # デ－タベ－スへの接続
    if connect_to_database() == False:
        return False
      
    res,tables = get_table_name()
    if res == False:
        return False

    account_table_exist = False
    prof_table_exist = False
    for table in tables:
        if ACCOUNT_TABLE in table:
            account_table_exist = True
        if PROFILE_TABLE in table:
            prof_table_exist = True 


    # アカウント用テーブルの作成
    if account_table_exist == False:
        if create_account_table() == False:
            return False
        
    # 管理者メンバの存在確認
    account = get_account_member(ADMIN_USER_NAME)
    print(account)
    
    # 管理者メンバの登録
    if account == None:
        password = generate_password_hash(ADMIN_PASSWORD,method='sha256')
        # print(password)
        if add_account(ADMIN_USER_NAME,password) == False:
            return

    # プロファイル用テーブルの作成
    if prof_table_exist == False:
        if create_prof_table() == False:
            return False

    return True

#===========================================================================================
#                                  アカウントの追加 
#===========================================================================================
def add_member_account(username,password):
    password = generate_password_hash(password,method='sha256')
    # print(password)
    if add_account(username,password) == False:
        return   

#===========================================================================================
#                                   アカウント認証
#===========================================================================================
def check_account(user_name,str_password):
    accounts = get_account_member(user_name)
    if accounts == None:
        return False
    password = accounts[2]
    return check_password_hash(password,str_password) 


#===========================================================================================
#                                  アカウントの追加 
#===========================================================================================
def delete_member(user_name):
    member_profile = get_profile_member(user_name)
    if member_profile != None:
        result = delete_profile_member(user_name)
        if result ==  False:
            return False
        
        member_profile = get_profile_member(user_name)
        if member_profile != None:
            return False
        
    member_account = get_account_member(user_name)
    if member_account != None:
        result = delete_account_member(user_name)
        if result == False:
            return False
        member_account = get_account_member(user_name)
        if member_account != None:
            return False

    return True


#===========================================================================================
#                                  プロファイル選択取得 
#===========================================================================================
def get_profile_condition(condition):
    profile_info = None
    condition_add = False
    str_sql = "SELECT * FROM {}".format(PROFILE_TABLE)

    if condition["registerd_start"] != "" and condition["registerd_end"] != "":
        condition_add = True
        str_sql = "{} WHERE registerd_day BETWEEN '{}' AND '{}'".format(str_sql,condition["registerd_start"],condition["registerd_end"])


    if condition["birth_start"] != "" and condition["birth_end"] != "":
        if condition_add == True:
            str_sql = "{} AND birthday BETWEEN '{}' AND '{}'".format(str_sql,condition["birth_start"],condition["birth_end"])   
        else:
            condition_add = True
            str_sql = "{} WHERE birthday BETWEEN '{}' AND '{}'".format(str_sql,condition["birth_start"],condition["birth_end"])   

    if condition["gender"] == "male":
        if condition_add == True:
            str_sql = "{} AND gender = '1'".format(str_sql)   
        else:
            condition_add = True
            str_sql = "{} WHERE gender = '1'".format(str_sql)           


    if condition["gender"] == "female":
        if condition_add == True:
            str_sql = "{} AND gender = '0'".format(str_sql)   
        else:
            condition_add = True
            str_sql = "{} WHERE gender = '0'".format(str_sql)  


    if condition["address"] != "":
        if condition_add == True:
            str_sql = "{} AND address = '{}'".format(str_sql,condition["address"])   
        else:
            condition_add = True
            str_sql = "{} WHERE address = '{}'".format(str_sql,condition["address"])  

    str_sql = "{};".format(str_sql)

    if execute_sql(str_sql,False) == False:
        return profile_info    
    
    profile_info = cursor.fetchall()
    if len(profile_info) == 0:
        return None

    print(profile_info)
    
    return profile_info
