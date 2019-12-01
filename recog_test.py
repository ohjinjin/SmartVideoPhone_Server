import cv2
import numpy as np
import os
import socket
import time
import threading

# 클라이언트 별 스레드
class ClientThread(threading.Thread):

    def __init__(self,ip,port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        print ("[+] New thread started for "+ip+":"+str(port))


    def run(self):    
        print ("Connection from : "+ip+":"+str(port))
        while True:
            tmp = clientSock.recv(1024).decode()
            #print(tmp+",client said.")
            if (tmp != "") and (tmp == "recognize"):
                # 인식하라고 메시지가 오면 mjpgstreamer에서 스냅샷을 가지고 face recognition을 진행
                # recognition 결과를 반환받아 tcp/ip 송신하도록 바꾸기
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                recognizer.read('trainer.yml')
                cascadePath = "haarcascades/haarcascade_frontalface_default.xml"
                faceCascade = cv2.CascadeClassifier(cascadePath);
                font = cv2.FONT_HERSHEY_SIMPLEX

                #iniciate id counter
                id = 0

                # names related to ids: example ==> loze: id=1,  etc
                # 이런식으로 사용자의 이름을 사용자 수만큼 추가해준다.
                names = ['None', 'ohjinjin']

                # Initialize and start realtime video capture
                #cam = cv2.VideoCapture(0)
                cap = cv2.VideoCapture("http://192.168.219.104:8090/?action=stream")
                    
                cap.set(3, 640) # set video widht
                cap.set(4, 480) # set video height

                # Define min window size to be recognized as a face
                minW = 0.1*cap.get(3)
                minH = 0.1*cap.get(4)

                boool = False
                path = 0
                while True:
                    #ret, img =cam.read()
                    ret, img = cap.read()
                    
                    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    
                    faces = faceCascade.detectMultiScale( 
                        gray,
                        scaleFactor = 1.2,
                        minNeighbors = 5,
                        minSize = (int(minW), int(minH)),
                       )

                    for(x,y,w,h) in faces:
                        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
                        # Check if confidence is less them 100 ==> "0" is perfect match
                        if (confidence < 100):
                            boool = True
                            id = names[id]
                            confidence = "  {0}%".format(round(100 - confidence))
                            clientSock.sendall("True\n".encode())
                            print("cheche")
                        else:
                            id = "unknown"
                            confidence = "  {0}%".format(round(100 - confidence))
                        
                        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
                        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
                    
                    cv2.imshow('camera',img) 
                    #k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
                    if boool or path>100:
                        if not boool:
                            clientSock.sendall("False\n".encode())
                            #break
                        boool = False
                        break
                    
                    path += 1
                # Do a bit of cleanup
                print("\n [INFO] Exiting Program and cleanup stuff")
                cap.release()
                cv2.destroyAllWindows()
            time.sleep(5)

        
        
## tcp/ip 소켓 생성
# 접속할 서버 주소
HOST ='192.168.219.106' # or loopback addr

# 클라이언트 접속을 대기하는 포트 번호
PORT = 8080

# 주소 체계로 IPv4, 소켓 타입으로 TCP 사용
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 포트 사용중이라 연결할 수 없다는 winError 10048 에러 해결을 위해 필요
serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 네트워크 인터페이스와 포트 번호에 소켓을 바인딩
serverSock.bind((HOST, PORT))

# 안드로이드 스레드들 관리
threads = []

while True:
    # 서버가 클라이언트의 접속을 허용하도록_최대 4명까지
    serverSock.listen(4)

    # accept 함수에서 대기하다가 클라이언트가 접속하면 새로운 소켓을 리턴
    (clientSock, (ip, port)) = serverSock.accept()
    newthread = ClientThread(ip, port)
    newthread.start()
    threads.append(newthread)
    print("\n클라이언트 수: "+str(len(threads)))

