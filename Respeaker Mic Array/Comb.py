import speech_recognition as sr
import pymongo
from datetime import datetime
import json
import re
import time
import os

# Kết nối tới MongoDB Atlas
client = pymongo.MongoClient("mongodb+srv://duyth799:ko7f0APk2MX6lUso@cluster0.zvhpbft.mongodb.net/?retryWrites=true&w=majority")

# Chọn database và collection để lưu trữ số nguyên và timestamp
db = client['mydatabase']
collection = db['mycollection']


def numinput(num):
    try:
        #num = int(input("Nhập góc điều khiển (Nhấn Ctr + C để quay lại menu trước): "))
        if num is not None and num >= 0 and num <= 360:
            # Tạo giá trị timestamp hiện tại
            timestamp = datetime.now()
            # Chuyển giá trị thời gian thành chuỗi để lưu vào file JSON
            timestamp_str = timestamp.strftime("%d-%m-%Y %H:%M:%S")
            # Dữ liệu JSON đưa lên mongoDB
            data = {"number": num, "timestamp": timestamp}
            # Thêm dữ liệu vào Database
            collection.insert_one(data)
            print("Đã lưu trữ góc",num, "và timestamp thành công trong MongoDB.")
            print(" ")
        else:  # Nếu nhập sai góc ngoài 0 - 360
            print("Bạn nhập chưa giá góc chưa hợp lệ / Vui lòng nhập lại giá trị góc từ 0 - 360 độ")
            print(" ")
            time.sleep(1) 
    except ValueError:
        print("Bạn nhập sai kiểu dữ liệu / Vui lòng nhập lại")
        time.sleep(2)
    return None, None 




def creatjsonfile(num,timestamp_str):
    # Tạo một đối tượng JSON mới chứa các giá trị đã được chuyển đổi
    data_json = {"number": num, "timestamp": timestamp_str}
    with open("a.json", 'w') as f:
        # Lưu đối tượng JSON vào tệp
        json.dump(data_json, f)
        f.write('\n')
    print("Đã lưu file JSON")
    print(" ")
    # Truy vấn và in ra 3 giá trị JSON mới nhất
    cursor = collection.find().sort("timestamp", pymongo.DESCENDING).limit(3)
    print("Giá trị JSON gần nhất là:")
    for doc in cursor:
            print(doc)
            print(" ")
    time.sleep(3)          

# Sử dụng thư viện SpeechRecognition để chuyển giọng nói thành văn bản
def mic():
    print("Bắt đầu nói")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='vi-VN')
            return text
        except sr.UnknownValueError:
            print("Không nhận dạng được giọng nói. Vui lòng nói lại.")
            return None

def speechrecog():
    text = mic()
    if text is not None:
        match = re.findall(r'\d+', text)
        if match:
            if int(match[-1]) <= 360 and int(match[-1]) >= 0:
                angle = int(match[-1])
                timestamp = datetime.now()
                # Dữ liệu JSON đưa lên mongoDB
                data = {"number": angle, "timestamp": timestamp}
                # Thêm dữ liệu vào Database
                collection.insert_one(data)
                print(f"Đã cập nhật giá trị góc quay thành công. Giá trị mới: {angle}")
                return angle
            else:
                print("Giá trị góc không hợp lệ")
        else:
            print("Lỗi", "Không tìm thấy giá trị góc trong khi nhận dạng")
    else:
        print("Lỗi", "Không nhận được giá trị từ giọng nói")
    return None



if __name__ == '__main__':
    while True:
        os.system('cls' if os.name=='nt' else 'clear')
        print("Nhập phím 1 + Enter để điều khiển góc bằng giọng nói")
        print("Nhập phím 2 + Enter để nhập góc điều khiển từ bàn phím ")
        print("Nhập phím 3 + Enter để lấy giá trị góc từ module Respeaker Mic Array 2.0")
        print("Nhập phím 4 + Enter để thoát chương trình")
        n =int(input("Nhập ở đây:"))

        if  n == 1:
            while True:
                try:
                    speechrecog()
                except KeyboardInterrupt:
                    os.system('cls' if os.name=='nt' else 'clear')
                    print("Quay lại nhập lựa chọn")
                    time.sleep(1)
                    break
        elif n == 2:
            while True:
                os.system('cls' if os.name=='nt' else 'clear')
                try:    
                    num, timestamp_str = numinput()
                    creatjsonfile(num, timestamp_str)
                except ValueError:
                    print("Bạn nhập sai kiểu dữ liệu / Vui lòng nhập lại")
                    time.sleep(2)
                except KeyboardInterrupt:
                    print("Quay lại nhập lựa chọn")
                    time.sleep(1)
                    break
        elif n == 3:
            os.system('cls' if os.name=='nt' else 'clear')
            print("Chức Năng Chưa Được Phát Triển")
        elif n == 4:
            os.system('cls' if os.name=='nt' else 'clear')
            print("Thoát Chương Trình")
            exit()
        else:
            os.system('cls' if os.name=='nt' else 'clear')
            print("Vui Lòng Nhập Lại Lựa Chọn")
            
    