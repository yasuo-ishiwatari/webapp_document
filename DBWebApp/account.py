import chardet


from database import get_account_member

MAX_USER_NAME_LEN = (20 - 1)
MIN_PASSWORD_LEN = 8
MAX_PASSWORD_LEN = 16



def check_new_account(user_name,pass_word,pass_word_conf):

    if user_name == "" or pass_word == "" or pass_word_conf == "":
        return False

    print(user_name,pass_word,pass_word_conf)

    # ID妥当性チェック
    if user_name.isidentifier() == False:
        return False

    # ASCIIコ－ドチェック
    if pass_word.isascii() == False:
        return False

    # ASCIIコ－ドチェック
    if pass_word_conf.isascii() == False:
        return False

    # ユ－ザ存在チェック
    accounts = get_account_member(user_name)
    if accounts != None:
        print(accounts)
        return False
    
    # ユ－ザ名長チェック
    if len(user_name) > MAX_USER_NAME_LEN:
        return False

    print("User Name is OK")

    #パスワード長チェック
    if len(pass_word) < MIN_PASSWORD_LEN or len(pass_word) > MAX_PASSWORD_LEN:
        return 

    #パスワード文字　英数字チェック
    for c in pass_word:
        if c.isalpha() == False and c.isdigit() == False:
            return False
    
    print("PassWord is OK")

    #パスワード確認チェック
    if pass_word != pass_word_conf:
        return False

    print("PassWord confirm is OK")

    return True
