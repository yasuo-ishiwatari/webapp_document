import datetime

prefect_list = ["北海道","青森県","岩手県","宮城県","秋田県","山形県","福島県",
"茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県",
"新潟県","富山県","石川県","福井県","山梨県","長野県","岐阜県",
"静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県",
"奈良県","和歌山県","鳥取県","島根県","岡山県","広島県","山口県",
"徳島県","香川県","愛媛県","高知県","福岡県","佐賀県","長崎県",
"熊本県","大分県","宮崎県","鹿児島県","沖縄県"]

Min_Year = 1940
now = datetime.datetime.now()
Max_Year = now.year

YearList = []
yy = Min_Year
while True:
    if yy > Max_Year:
        break
    YearList.append(yy)
    yy += 1

MonthList = ["1","2","3","4","5","6","7","8","9","10","11","12"]

DayList = []
for idx in range(31):
    dd = "{}".format(idx+1)
    DayList.append(dd)


def Get_Prefect():
    return prefect_list

def Get_Year():
    return YearList

def Get_Month():
    return MonthList

def Get_Day():
    return DayList