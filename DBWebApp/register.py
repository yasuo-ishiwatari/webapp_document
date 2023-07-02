import datetime
from dateutil.relativedelta import relativedelta

MALE_BIT = True
FEMALE_BIT = False

profile_data = {}
profile_data['username'] = ""
profile_data['registerday'] = ""
profile_data['fname'] = ""
profile_data['gname'] = ""
profile_data['birthday'] = ""
profile_data['gender'] = ""
profile_data['address'] = ""

def check_register_info(register_info):

    errmsg = ""

    global profile_data
    profile_data = {}

    user_name = register_info['user']
    family_name = register_info['fname']
    given_name = register_info['gname']
    str_birth_year = register_info['year']
    str_birth_month = register_info['month']
    str_birth_day = register_info['day']
    gender = register_info['gender']
    address = register_info['address']

    # ユ－ザ名チェック 
    if user_name == "":
        errmsg = "ユ－ザ名が認識できません！！"
        return errmsg,profile_data

    # 氏名チェック
    if family_name == "" or given_name == "":
        errmsg = "氏名が空欄です！！"
        return errmsg,profile_data

    # 誕生日チェック
    birth_year = 0
    birth_month = 0
    birth_day = 0

    try:
        birth_year = int(str_birth_year)
        birth_month = int(str_birth_month) 
        birth_day = int(str_birth_day)
    except:
        errmsg = "日付が不適切です！！"
        errmsg,profile_data

    try:
        str_birth = "{}/{:0>2}/{:0>2}".format(birth_year,birth_month,birth_day)
        birth =  datetime.datetime.strptime(str_birth,"%Y/%m/%d")
    except:
        errmsg = "日付が不適切です！！"
        return errmsg,profile_data

    birthday = "{}{:0>2}{:0>2}".format(birth_year,birth_month,birth_day)

    # 性別チェック
    gender_bit = False
    if gender == "male":
        gender_bit = MALE_BIT
    elif gender == "female":
        gender_bit = FEMALE_BIT
    else:
        errmsg = "性別が不明です！！"
        return errmsg,profile_data

    # 住所チェック
    if address == "":
        errmsg = "住所が空欄です！！"
        return errmsg,profile_data
    
    # 登録日セット
    now = datetime.datetime.now()
    registerday = "{}{:0>2}{:0>2}".format(now.year,now.month,now.day)

    # 登録デ－タセット
    profile_data['username'] = user_name
    profile_data['registerday'] = registerday
    profile_data['fname'] = family_name
    profile_data['gname'] = given_name
    profile_data['birthday'] = birthday 
    profile_data['gender'] = gender_bit
    profile_data['address'] = address

    return errmsg,profile_data

def get_age_from_birthday(birthday):
    today = datetime.date.today()
    birth_day = datetime.date(birthday.year,birthday.month,birthday.day)
    age = relativedelta(today,birth_day).years

    return age

def check_record_condition_info(record_condition):
    
    # 登録日チェック
    if record_condition['registerd'] == "ON":
        try:
            year = int(record_condition['registerd_year_start'])
            month = int(record_condition['registerd_month_start'])
            day = int(record_condition['registerd_day_start'])
            str_registerd = "{}/{:0>2}/{:0>2}".format(year,month,day)
            registerdday_start =  datetime.datetime.strptime(str_registerd,"%Y/%m/%d")
            str_registerday_start = "{}/{:0>2}/{:0>2} 00:00:00".format(year,month,day)
            year = int(record_condition['registerd_year_end'])
            month = int(record_condition['registerd_month_end'])
            day = int(record_condition['registerd_day_end'])
            str_registerd = "{}/{:0>2}/{:0>2}".format(year,month,day)
            registerdday_end =  datetime.datetime.strptime(str_registerd,"%Y/%m/%d")
            str_registerday_end = "{}/{:0>2}/{:0>2} 00:00:00".format(year,month,day)

            if registerdday_start > registerdday_end:
                str_registerday_start = ""
                str_registerday_end = ""                

        except:
            str_registerday_start = ""
            str_registerday_end = ""
    else:
        str_registerday_start = ""
        str_registerday_end = ""        

    # 誕生日チェック
    if record_condition["birth"] == "ON":
        print(record_condition)
        try:
            year = int(record_condition['birth_year_start'])
            month = int(record_condition['birth_month_start'])
            day = int(record_condition['birth_day_start'])
            str_birth = "{}/{:0>2}/{:0>2}".format(year,month,day)
            birthday_start =  datetime.datetime.strptime(str_birth,"%Y/%m/%d")
            str_birthday_start = "{}/{:0>2}/{:0>2} 00:00:00".format(year,month,day)
            year = int(record_condition['birth_year_end'])
            month = int(record_condition['birth_month_end'])
            day = int(record_condition['birth_day_end'])
            str_birth = "{}/{:0>2}/{:0>2}".format(year,month,day)
            birthday_end =  datetime.datetime.strptime(str_birth,"%Y/%m/%d")
            str_birthday_end = "{}/{:0>2}/{:0>2} 00:00:00".format(year,month,day)

            if birthday_start > birthday_end:
                str_birthday_start = ""
                str_birthday_end = ""               

        except:
            str_birthday_start = ""
            str_birthday_end = ""
    else:
        str_birthday_start = "" 
        str_birthday_end = ""       

    record_condition_info = {}
    record_condition_info["registerd_start"] = str_registerday_start
    record_condition_info["registerd_end"] = str_registerday_end
    record_condition_info["birth_start"] = str_birthday_start
    record_condition_info["birth_end"] = str_birthday_end

    if record_condition['male'] == "OFF":
        record_condition_info["gender"] = "female"
    elif record_condition['female'] == "OFF":
        record_condition_info["gender"] = "male"
    else:
        record_condition_info["gender"] = ""

    record_condition_info["address"] = record_condition['address']


    return record_condition_info

