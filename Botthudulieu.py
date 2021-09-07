import pandas as pd
from datetime import datetime
from csv import writer, QUOTE_ALL
from pytz import timezone


# Bot don gian thu ve gia last price cua ma VN30F2203 theo tung giay
# thoi gian chay: khoang 1.05 giay cho moi 1 lan thu data va viet vao day last_price
# neu no ko thoat thi a huy cai chuong trinh nay de no dung lai
while True:
    trading_time = int(datetime.now(timezone('Asia/Ho_Chi_Minh')).time().hour)
    if trading_time >= 9 or trading_time < 3:
        print('---> Thi truong vua mo cua va bat dau thu thap du lieu')
        last_price = []
        url = 'https://bgapidatafeed.vps.com.vn/getpsalldatalsnapshot/VN30F2109,VN30F2110,VN30F2112,VN30F2203'
        while True:
            closing_time = datetime.now(timezone('Asia/Ho_Chi_Minh')).time()
            if 3 <= int(closing_time.hour) <= 8:
                print('---> Thi truong da dong cua')
                break
            df = pd.read_json(url)
            last_price.append(df.to_numpy()[3, 6])

        string_file_name = 'Giahomnay_' + str(datetime.today()) + '.csv'
        with open(string_file_name, 'w', encoding='utf-8', newline='') as myfile:
            wr = writer(myfile, quoting=QUOTE_ALL)
            wr.writerow(last_price)
        print('---> Thoat chuong trinh thanh cong va luu vao file csv')
