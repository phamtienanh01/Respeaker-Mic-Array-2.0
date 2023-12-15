from tuning import Tuning
import usb.core
import usb.util
import pymongo
#from datetime import datetime
import time


def run_microphone_tuning():
    # Kết nối tới MongoDB Atlas
    client = pymongo.MongoClient("mongodb+srv://Phamtienanh0:Phamtienanh0@cluster0.o3w7mgf.mongodb.net/?retryWrites=true&w=majority")

    # Database và Collection muốn lưu dữ liệu
    db = client['mydatabase']
    collection = db['mycollection']

    dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
    if dev: # Tìm thấy Respeaker Mic Array  
        Mic_tuning = Tuning(dev)
        Mic_tuning.set_vad_threshold(5)  # Thiết lập ngưỡng VAD là n dB

        direction = 360 - Mic_tuning.direction # thay đổi hướng Respeaker 
        print("Giá trị góc hiện tại", direction)
        
        old_direction = None  # biến lưu giá trị góc cũ
        is_changed = False  # biến đánh dấu sự thay đổi
        sampling_interval = 0.2  # Đặt khoảng thời gian lấy mẫu lại (ví dụ: 0.1 giây)
           
        while True: # Vòng lặp vô hạn
            try:
                if Mic_tuning.is_voice() == 1:  # Khi phát hiện giọng nói
                    direction = 360 - Mic_tuning.direction  # Lấy giá trị góc(hướng) đến của âm thanh hiện tại
                    if direction != old_direction:  # Kiểm tra sự thay đổi góc
                        #timestamp = datetime.now()
                        #data = {"number": direction, "timestamp": timestamp}
                        data = {"angle": direction}

                        collection.insert_one(data)
                        print("Đã lưu trữ góc thành công trên MongoDB.")
                        is_changed = True  # Đánh dấu sự thay đổi
                    
                    if is_changed:
                        print("Giá trị góc mới nhất là:", direction)
                        is_changed = False  # Đặt lại biến để chờ sự thay đổi tiếp theo
                    
                    old_direction = direction  # Cập nhật giá trị góc cũ = góc mới để kiểm tra ở vòng lặp tiếp theo
                time.sleep(sampling_interval)  # Đợi khoảng thời gian lấy mẫu lại
            except KeyboardInterrupt:
                print("******Thoát******")
                break

    # Đóng kết nối với MongoDB khi kết thúc chương trình
    client.close()


# Chương trình chính
def main():
    run_microphone_tuning()
    pass

# Gọi hàm main() để chạy chương trình chính
if __name__ == '__main__':
    main()
