import cv2
import face_recognition # yeu cau du lieu anh dau vao bieu dien duoi dang khong gian mau RGB
import os # thu vien load anh
import numpy # thu vien tinh toan ma tran
import pyttsx3

path = "Img_check"
images = []
classname = []
mylists = os.listdir(path)
 
for img in mylists:
    img_num = cv2.imread(f"{path}/{img}") # chuyen anh -> ma tran
    images.append(img_num)
    classname.append(os.path.splitext(img)[0]) # tach ten file va .jpg

def encoding(images):
    encodeLists = []
    for img_endcode in images:
        img_endcode = cv2.cvtColor(img_endcode, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img_endcode)[0] # ma hoa khuon mat
        encodeLists.append(encode)
    return encodeLists

encodeListsKnow = encoding(images) 
print("Loading :.............. 100%")  

cap = cv2.VideoCapture(0)

count = 0
while True:
    ret,frame = cap.read()
    frame_new = cv2.resize(frame,(0,0),None,fx=1,fy=1)
    frame_new = cv2.cvtColor(frame_new, cv2.COLOR_BGR2RGB)
    
    face_frame = face_recognition.face_locations(frame_new) # xac dinh vi tri khuon mat tren frame
    face_encode = face_recognition.face_encodings(frame_new) # ma hoa khuon mat tren frame

    for encodeFace, FaceLocation in zip(face_encode,face_frame):
        FaceDis = face_recognition.face_distance(encodeListsKnow, encodeFace) 
        matchindex = numpy.argmin(FaceDis)

        if  FaceDis[matchindex] < 0.5:
            name = classname[matchindex].upper()
        else:
            name = "UNKNOW"
        
        y1, x2, y2, x1 = FaceLocation
        cv2.rectangle(frame,(x1,y1), (x2,y2),(255,215,0),2)
        cv2.putText(frame,name,(x2,y2),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,215,0),2)   
        
        if name != "UNKNOW" and count == 0:
            engine = pyttsx3.init()
            engine.say(f"hello, {name}")
            engine.runAndWait()
        
             
    count = 1
      
    cv2.imshow('FaceID',frame)
    if cv2.waitKey(1) == ord("q"):
         break



cap.release()
cv2.destroyAllWindows()
        
    

