from tuning import Tuning
import usb.core
import usb.util
import time
import pymongo
from datetime import datetime
import json

# Kết nối tới MongoDB Atlas
client = pymongo.MongoClient("mongodb+srv://duyth799:ko7f0APk2MX6lUso@cluster0.zvhpbft.mongodb.net/?retryWrites=true&w=majority")

# Database và Collection muốn lưu dữ liệu
db = client['mydatabase']
collection = db['mycollection']

dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)

if dev: # Tìm thấy Respeaker Mic Array  
    Mic_tuning = Tuning(dev)
    print("Giá trị góc hiện tại", Mic_tuning.direction)
    
    voice_signal_found = False  # biến mặc định tìm giọng nói là False
    old_direction = None  # biến lưu giá trị góc cũ
    is_changed = False  # biến đánh dấu sự thay đổi
    
    while True: # Vòng lặp vô hạn
        try:
            if Mic_tuning.is_voice() == 1:  # Khi phát hiện giọng nói
                direction = Mic_tuning.direction  # Lấy giá trị góc(hướng) đến của âm thanh hiện tại
                if direction != old_direction:  # Kiểm tra sự thay đổi góc
                    timestamp = datetime.now()
                    timestamp_str = timestamp.strftime("%d-%m-%Y %H:%M:%S")
                    data = {"number": direction, "timestamp": timestamp}
                    collection.insert_one(data)
                    print("Đã lưu trữ góc (số nguyên) và timestamp thành công trong MongoDB.")
                    voice_signal_found = True  # biến mặc định tìm giọng nói là False
                    is_changed = True  # Đánh dấu sự thay đổi
                
                if is_changed:
                    print("Giá trị góc mới nhất là:", direction)
                    is_changed = False  # Đặt lại biến để chờ sự thay đổi tiếp theo
                
                old_direction = direction  # Cập nhật giá trị góc cũ = góc mới để kiểm tra ở vòng lặp tiếp theo
            else:
                if voice_signal_found: # Nếu Voice Signal = True thì thực hiện đoạn code dưới
                    voice_signal_found = False # Đổi lại thành False để điều kiện trên ko đúng để cho ctr in duy nhất 1 dòng ko tìm thấy giọng nói
                    print("                         ")
                    print("Không tìm thấy âm thanh/Chưa có sự thay đổi góc âm thanh")
                    print("                         ")
        except KeyboardInterrupt:
            break
