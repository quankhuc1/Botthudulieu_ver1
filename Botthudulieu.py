from datetime import datetime
from csv import writer, QUOTE_ALL
from pytz import timezone
import requests


# Bot don gian thu ve gia last price cua ma VN30F2203 theo tung giay
# thoi gian chay: khoang 1.05 giay cho moi 1 lan thu data va viet vao day last_price
# neu no ko thoat thi a huy cai chuong trinh nay de no dung lai
while True:
    trading_time = int(datetime.now(timezone('Asia/Ho_Chi_Minh')).time().hour)
    if 9 <= trading_time < 15:
        print('---> Thi truong vua mo cua va bat dau thu thap du lieu')
        last_price = []
        url = 'https://bgapidatafeed.vps.com.vn/getpsalldatalsnapshot/VN30F2109,VN30F2110,VN30F2112,VN30F2203'
        while True:
            closing_time = int(datetime.now(timezone('Asia/Ho_Chi_Minh')).time().hour)
            if closing_time < 9 or closing_time >= 15:
                print('---> Thi truong da dong cua')
                break
            try:
                # timeout cua request nay la 10s. Neu connection mat hon 10 giay, no se raise exception phia duoi
                data = requests.get('https://bgapidatafeed.vps.com.vn/getpsalldatalsnapshot/VN30F2109,'
                                    'VN30F2110,VN30F2112,VN30F2203', timeout=10).json()
                last_price.append(data[3]['lastPrice'])
            except requests.exceptions.RequestException as exception:
                if str(type(exception).__name__) == 'TimeoutError':
                    print('Chuong trinh doi may chu tra ve trong 10 giay nhung may chu ko tra thong tin ve')
                    pass
                elif str(type(exception).__name__) == 'ConnectionError':
                    print('Mat ket noi voi server')
                    pass
                else:
                    print('request.get() bi loi va se phai xem them thong tin cua exception')
                    print('---> Ten cua exception:', str(type(exception).__name__))
                    print('---> Chuong trinh se bi thoat do co exception va du lieu se duoc luu')
                    break
        # neu day last_price co it hon 2 gia, chuong trinh se ko in ra file csv de tranh in ra file csv co moi 1 gia
        if len(last_price) >= 2:
            date_time = str(datetime.today()).replace('-', '_')[:10]
            string_file_name = 'Giahomnay_' + date_time + '.csv'
            with open(string_file_name, 'w', encoding='utf-8', newline='') as myfile:
                wr = writer(myfile, quoting=QUOTE_ALL)
                wr.writerow(last_price)
            print('---> Thoat chuong trinh thanh cong va luu vao file csv')
    else:
        print('Thi truong dang dong cua, hay mo chuong trinh vao thoi gian luc thi truong mo cua')
        break
