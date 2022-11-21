from socket import *
serverPort = 12003  # 서버가 사용할 포트는 12000
repository = {}
send_message = ''
# 1. client와 연결을 위한 소켓 생성
# 2. 생성한 소켓을 사용하려는 포트와 바인딩 (사용하려는 포트를 고정시킴)
# 3. client측에 connection요청
# 4. listen(), accept()메서드를 순서대로 호출하고 client로 부터를 기다림 (blocking function으로 client의 response 받기 전까지 대기)
# 5. client로부터 connection response를 받았으면 client와 연결생성
# 6. client와 통신을 위한 소켓 생성
# 7. client와 통신
# 8. client로 부터 close() request를 받으면 연결 종료

server_sock = socket(AF_INET, SOCK_STREAM)    # IPv4를 이용하는 TCP소켓(SOCK_STREAM 파라미터 사용) 생성
server_sock.bind(('', serverPort)) # addr에 빈 문자열을 넣음으로써 모든 인터페이스와 연결 허용, 소켓에 고정된 포트 할당
server_sock.listen(1)              # client의 connect 요청을 받음
connection_sock, addr = server_sock.accept() # accept() 함수는 통신을 위한 소켓과 클라이언트 소켓에 바인드 된 주소를 리턴함
                                             # 요청이 올 때 까지 대기(blocking func)
print('연결 성공')
param_list = ['cmd', 'key', 'value']         # client로부터 받은 데이터 저장할 변수 이름

while True:
    recv_message = ""
    try :                                    # client가 close()요청시 recv()함수 예외 처리를 위한 try-except문
        recv_message = connection_sock.recv(1024).decode('utf-8') # client가 보낸 메시지 디코딩
        print('From Client : ',recv_message)           # 수신한 message 출력


        msg_list = recv_message.split(',')                     # 메시지 split
        cmd, key, value = "", "", ""
        for param, val in zip(param_list,msg_list):  # client로부터 받은 데이터 cmd, key, value변수 에 저장
            globals()[param] = val
        cmd = cmd.upper()                           # PUT,GET,DELETE,LIST 명령어는 대문자 처리

        if cmd == 'PUT':                            # cmd == PUT
            if key not in repository.keys():
                repository[key] = value             # 딕셔너리에 해당 key없으면 key-value쌍 생성
                send_message = 'SUCCESS'
            else :
                repository.update({key : value})    # 딕셔너리에 해당 key 존재하면 value갱신
                send_message = 'VALUE CHANGE SUCCESS'

        elif cmd == 'GET':                          # 딕셔너리에 해당 key 없는 경우
            if key not in repository.keys() :
                send_message = 'NOT EXIST!'
            else :                                  # send_message에 key에 대응하는 value값 대입
                send_message = '\n' + 'VALUE : ' + repository[key]

        elif cmd == 'DELETE':
            if key not in repository.keys():        # 딕셔너리에 해당 key 없을 때
                send_message = 'NOT EXIST!'
            else :
                del repository[key]                 # 딕셔너리에 해당 key 존재하면 key-value쌍 제거
                send_message = 'SUCCESS!'

        elif cmd== 'LIST':
            if len(repository) == 0:                # 딕셔너리 비어있을 때
                send_message = "NOT EXIST!"
            else :                                  # 딕셔너리에 item들어있으면 모든 key-value쌍 send_message에 대입
                send_message = ""
                for k,v in repository.items():      # key-value쌍 전부 send_message에 담기
                    send_message = send_message + f"\n{k},{v}"

    except ConnectionResetError :           # client와 연결 종료되면 프로그램 종료
        print('연결종료')
        connection_sock.close()
        break

    connection_sock.send(send_message.encode('utf-8'))   # send_message utf-8로 인코딩
    print('Response : ', send_message, '\n')  # 답장 출력


