from socket import *
from threading import *


class ChatServer:
    clients = []  # 접속된 클라이언트 소켓 목록
    final_received_message = ""  # 최종 수신 메시지

    # 소켓을 생성하고 연결되면 accept_client() 호출
    def __init__(self):
        self.s_sock = socket(AF_INET, SOCK_STREAM)
        self.ip = ''
        self.port = 2500
        self.s_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s_sock.bind((self.ip, self.port))
        print("클라이언트 대기 중...")
        self.s_sock.listen(100)
        self.accept_client()

    # 연결 클라이언트 소켓을 목록에 추가하고 스레드를 생성하여 데이터를 수신한다.
    def accept_client(self):
        while True:
            client = c_socket, (ip, port) = self.s_sock.accept()
            if client not in self.clients:
                # 접속된 소켓을 목록에 추가
                self.clients.append(client)
            print(ip, ':', str(port), ' 가 연결되었습니다.')
            # 수신 스레드
            cth = Thread(target=self.receive_messages, args=(c_socket,))
            # 스레드 시작
            cth.start()

    # 데이터를 수신하여 모든 클라이언트에게 전송한다.
    def receive_messages(self, c_socket):
        while True:
            try:
                incoming_message = c_socket.recv(256)
                # 연결이 종료됨
                if not incoming_message:
                    break
            except:
                continue
            else:
                self.final_received_message = incoming_message.decode('utf-8')
                print(self.final_received_message)
                self.send_all_clients(c_socket)
        c_socket.close()

    # 송신 클라이언트를 제외한 모든 클라이언트에게 메시지 전송
    def send_all_clients(self, senders_socket):
        # 목록에 있는 모든 소켓에 대해
        for client in self.clients:
            socket, (ip, port) = client
            # 송신 클라이언트는 제외
            if socket is not senders_socket:
                try:
                    socket.sendall(self.final_received_message.encode())
                # 연결 종료
                except:
                    # 소켓 제거
                    self.clients.remove(client)
                    print("{}, {} 연결이 종료되었습니다.".format(ip, port))


if __name__ == "__main__":
    ChatServer()
