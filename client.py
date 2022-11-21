from sys import stdin
from socket import *
from _thread import *
hostname = gethostname()
IP_addr = gethostbyname(hostname)     # 클라이언트와 서버가 같은 IP를 사용하므로 호스트의 IP를 받아옴
serverPort = 12003                          # 서버가 지정한 포트번호

# 1. 통신을 위한 소켓 생성
# 2. 서버에 connect 요청 보냄
# 3. 명령어를 입력받아 서버로 전송
# 4. 서버로부터 받은 response 출력
# 4. 연결 종료를 원하면 서버에 'exit'을 입력하여 서버에 close() 요청

client_socket = socket(AF_INET, SOCK_STREAM) # TCP 소켓 생성
client_socket.connect((IP_addr,serverPort))  # 서버에 connect 시도


while True :
    message = stdin.readline().strip()               # 메시지 입력
    if message == 'exit' :                  # exit 입력 시 연결 종료
        client_socket.close()               # 소켓 close()호출
        print('연결 종료')

    else :
        client_socket.send(message.encode('utf-8'))  # 입력한 메시지를 utf-8로 인코딩
        returnMessage = client_socket.recv(1024)     # 서버로부터 1024 자리의 메시지를 수신
        print('From Server: ', returnMessage.decode('utf-8')) # 서버로부터 받은 메시지를 utf-8로 디코딩 후 출력
