import Comb
from VAD import run_microphone_tuning
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Thái Duy - 417H0174")
root.resizable(False, False) # không cho phép mở rộng hoặc thu nhỏ cửa sổ
root.configure(bg="#110000")
root.attributes('-topmost', True)  # Keep the window on top
current_function = 1
def show_message(event=None):
    global current_function
    if current_function == 1:
        try:
            num1 = int(entry.get())
            if num1 >= 0 and num1 <=360:
                Comb.numinput(num1)
                messagebox.showinfo("Thông báo", "Bạn đã nhập thành công số: " + str(num1))
                entry.delete(0, tk.END)
            else:
                messagebox.showerror("Lỗi", "Dữ liệu nhập vào không phù hợp")
                entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Lỗi", "Dữ liệu nhập vào không phải là số")
            entry.delete(0, tk.END)
    elif current_function == 2:
        pass
    elif current_function == 3:
        pass
    elif current_function == 4:
        pass

def switch_function_1(): #Chức năng nhập giá trị góc từ bàn phím
    global current_function
    current_function = 1
    label.config(text="Bạn đang sử dụng chức năng nhập dữ liệu từ bàn phím",font=("Arial Bold", 15))

def switch_function_2(): #Chức năng lấy giá trị góc từ giọng nói
    label.config(text="Bạn đang sử dụng chức năng nhận diện giọng nói",font=("Arial Bold", 15))
    global current_function
    current_function = 2
    root.update() # cập nhật giao diện để hiển thị label mới 
    messagebox.showinfo("Thông báo", "Nhấn Ok để bắt đầu nói...")
    angle = Comb.speechrecog() # Lấy giá trị góc từ giọng nói
    if angle is not None:
        messagebox.showinfo("Thông báo", "Đã nhận giá trị: " + str(angle))
    else:
        messagebox.showerror("Lỗi", "Không nhận được giá trị từ giọng nói")

def switch_function_3():
    global current_function, running, tuning_thread
    current_function = 3
    label.config(text="Bạn đang sử dụng chức năng DOA từ Respeaker Mic Array",font=("Arial Bold", 15))
    run_microphone_tuning()
    

def switch_function_4():
    global current_function, running, tuning_thread
    current_function = 4
    messagebox.showinfo("Thông báo","Cảm ơn bạn đã sử dụng chương trình")
    root.quit()

def on_enter_pressed(event):
    show_message()

label = tk.Label(root, text="Bạn đang sử dụng chức năng nhập dữ liệu từ bàn phím",font=("Arial Bold", 15), bg="black", fg="white")
label.pack(padx=10, pady=10)

entry = tk.Entry(root,width=50,font=("Arial", 15))
entry.pack(padx=10, pady=10)

button = tk.Button(root, text="Gửi dữ liệu", command=show_message, font=("Arial Bold", 13),width=10, bg="black", fg="white")
button.pack(padx=10, pady=10)

entry.bind('<Return>', on_enter_pressed)

switch_button_1 = tk.Button(root, text="Nhập dữ liệu", command=switch_function_1,font=("Arial Bold", 14), width=18, bg="#33CCFF")
switch_button_1.pack(side="left",padx=10, pady=10)

switch_button_2 = tk.Button(root, text="Giọng nói", command=switch_function_2,font=("Arial Bold", 14), width=18,bg="#FF6666")
switch_button_2.pack(side="left",padx=10, pady=10)

switch_button_3 = tk.Button(root, text="Respeaker Mic Array", command=switch_function_3,font=("Arial Bold", 14), width=18,bg="#CC99FF")
switch_button_3.pack(side="left",padx=10, pady=10)

quit_button = tk.Button(root, text="Thoát", command=switch_function_4,font=("Arial Bold", 14), width=18,bg="#00EE00")
quit_button.pack(side="left",padx=10, pady=10)


root.mainloop()
