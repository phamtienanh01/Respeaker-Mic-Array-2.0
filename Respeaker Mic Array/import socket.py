import socket
import usb.core
import usb.util
import time
from tuning import Tuning

# Thiết lập thông tin kết nối ESP32
ESP32_IP = "192.168.137.17"  # Địa chỉ IP của ESP32
ESP32_PORT = 1234  # Cổng kết nối

# Kết nối tới ESP32 qua TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ESP32_IP, ESP32_PORT))

# Tìm thiết bị Mic
dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)

if dev:
    Mic_tuning = Tuning(dev)
    print("Initial Mic direction:", Mic_tuning.direction)

    # Gửi giá trị Mic_tuning.direction liên tục
    old_direction = None  # Khởi tạo giá trị góc cũ
    
    while True:
        try:
            direction = 360-  Mic_tuning.direction  # Lấy giá trị góc từ Mic_tuning

            if direction != old_direction:
                data = str(direction)  # Chuyển đổi giá trị góc thành chuỗi
                
                # Gửi dữ liệu qua TCP/IP với ký tự phân tách là dấu cách
                data_with_separator = data + " "
                client_socket.sendall(data_with_separator.encode())
                
                # Đợi phản hồi từ ESP32
                response = client_socket.recv(1024)
                print("Response from ESP32:", response.decode())

                print("New direction:", direction)  # In giá trị góc mới
                
                old_direction = direction  # Cập nhật giá trị góc cũ
            
            #time.sleep(0.1)  # Đợi 0.1 giây trước khi gửi dữ liệu tiếp theo
        except KeyboardInterrupt:
            break

# Đóng kết nối
client_socket.close()
