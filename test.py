import cv2
import face_recognition
import sqlite3
import numpy as np
from tkinter import Tk, Label, Button

# Tạo bảng người dùng bằng SQLite với các cột mã hóa tên người dùng và khuôn mặt
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS users") #xóa bảng cũ nếu tồn tại tránh lỗi
c.execute('''CREATE TABLE users (username text, encoding blob, UNIQUE(username))''')
conn.commit()

def register():
    username = input("Enter username: ")
    
    # ghi lại khuôn mặt người đăng ký
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        frame_new = cv2.resize(frame, (0, 0), None, fx=1, fy=1)
        frame_new = cv2.cvtColor(frame_new, cv2.COLOR_BGR2RGB)
        
        # xác định vị trí khuôn mặt trên khung hình
        face_frame = face_recognition.face_locations(frame_new)
        if len(face_frame) == 1:
            # mã hóa khuôn mặt
            face_encode = face_recognition.face_encodings(frame_new, face_frame)
            encoding_blob = sqlite3.Binary(np.array(face_encode[0]).tostring())
            # lưu người dùng mới vào cơ sở dữ liệu người dùng
            c.execute("INSERT INTO users VALUES (?, ?)", (username, encoding_blob))
            conn.commit()
            break
        cv2.imshow('Register', frame_new)
        if cv2.waitKey(1) == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

def login():
    # Chụp khuôn mặt của người dùng bằng webcam
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        frame_new = cv2.resize(frame, (0, 0), None, fx=1, fy=1)
        frame_new = cv2.cvtColor(frame_new, cv2.COLOR_BGR2RGB)
        
        # Phát hiện khuôn mặt của người dùng trong khung hình đã chụp
        face_frame = face_recognition.face_locations(frame_new)
        if len(face_frame) == 1:
            # Mã hóa khuôn mặt của người dùng
            face_encode = face_recognition.face_encodings(frame_new, face_frame)
            encoding_blob = np.array(face_encode[0]).tostring()

            # Kiểm tra  mã hóa khuôn mặt  khớp với dữ liệu người dùng trong cơ sở dữ liệu người dùng không
            c.execute("SELECT * FROM users")
            rows = c.fetchall()
            for row in rows:
                username = row[0]
                encoding = np.frombuffer(row[1], dtype=np.float64)
                if face_recognition.compare_faces([encoding], face_encode[0])[0]:
                    print(f"Login successful! Welcome, {username}.")
                    return True
            break
        cv2.imshow('Login', frame_new)
        if cv2.waitKey(1) == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

def on_register_click():
    register()

def on_login_click():
    login()

# Tạo cửa sổ GUI
window = Tk()
window.title("Face Recognition")
window.geometry("300x200")

# Tạo và nút
label = Label(window, text="Press a button to continue")
label.pack()

register_button = Button(window, text="Register", command=on_register_click)
register_button.pack()

login_button = Button(window, text="Login", command=on_login_click)
login_button.pack()

# Bắt đầu vòng lặp sự kiện GUI
window.mainloop()

conn.close()
cap.release()
cv2.destroyAllWindows()
