from socket import *
from tkinter import *
from threading import *
import datetime


class ChatClient:
    client_socket = None

    def __init__(self, ip, port):
        self.initialize_socket(ip, port)
        self.initialize_gui()
        self.listen_thread()

    def initialize_socket(self, ip, port):
        '''
        TCP socket을 생성하고 server에게 연결
        '''
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        remote_ip = ip
        remote_port = port
        self.client_socket.connect((remote_ip, remote_port))

    def send_chat(self):
        '''
        message를 전송하는 콜백 함수
        '''
        now = datetime.datetime.now()  # + datetime.timedelta(seconds=20)
        nowTime = now.strftime('%H:%M')
        senders_name = self.name_widget.get().strip()
        data = self.enter_text_widget.get(1.0, 'end').strip()
        message = ("[" + senders_name + "]" + ": " + data).encode('utf-8')
        self.chat_transcript_area.insert('end', message.decode('utf-8') + '\n')
        self.chat_transcript_area.yview(END)
        self.chat_time_area.insert('end', nowTime + '\n')
        self.chat_time_area.yview(END)
        self.client_socket.send("채팅".encode())
        self.client_socket.send(message)
        self.enter_text_widget.delete(1.0, 'end')
        return 'break'

    def send_notice(self):
        '''
        notice를 전송하는 콜백 함수
        '''
        now = datetime.datetime.now()  # + datetime.timedelta(seconds=20)
        nowTime = now.strftime('%H:%M')
        senders_name = self.name_widget.get().strip()
        data = self.enter_text_widget.get(1.0, 'end').strip()
        message = ("[" + senders_name + "]" + ": " + data).encode('utf-8')
        self.text.set(message.decode('utf-8'))
        self.chat_transcript_area.insert('end', message.decode('utf-8') + '\n')
        self.chat_transcript_area.yview(END)
        self.chat_time_area.insert('end', nowTime + '\n')
        self.chat_time_area.yview(END)
        self.client_socket.send("공지".encode())
        self.client_socket.send(message)
        self.enter_text_widget.delete(1.0, 'end')
        return 'break'

    def initialize_gui(self):
        '''
        위젯을 배치하고 초기화한다.
        '''
        self.root = Tk()
        fr = []
        for i in range(0, 6):
            fr.append(Frame(self.root))
            fr[i].pack(fill=BOTH)

        self.root.title('멀티 채팅 프로그램')
        self.notice_label = Label(fr[0], text='공지:')
        self.text = StringVar()
        self.text.set("")
        self.notice_transcript_area = Label(fr[0], textvariable=self.text)
        self.recv_label = Label(fr[1], text='수신 메시지:')
        self.send_label = Label(fr[4], text='송신 메시지:')
        self.name_label = Label(fr[3], text='사용자 이름:')
        self.send_btn = Button(fr[4], text='전송', command=self.send_chat)
        self.send_notice_btn = Button(fr[4], text='공지', command=self.send_notice)
        self.chat_transcript_area = Text(fr[2], height=20, width=54)
        self.chat_time_area = Text(fr[2], height=20, width=6)
        self.enter_text_widget = Text(fr[5], height=5, width=60)
        self.name_widget = Entry(fr[3], width=15)

        self.notice_label.pack(side=LEFT)
        self.notice_transcript_area.pack(side=LEFT)
        self.name_label.pack(side=LEFT)
        self.name_widget.pack(side=LEFT)
        self.recv_label.pack(side=LEFT)
        self.send_btn.pack(side=RIGHT, padx=20)
        self.send_notice_btn.pack(side=RIGHT, padx=20)
        self.chat_transcript_area.pack(side=LEFT, pady=2)
        self.chat_time_area.pack(side=LEFT, pady=2)
        self.send_label.pack(side=LEFT)
        self.enter_text_widget.pack(side=LEFT, padx=2, pady=2)

    def listen_thread(self):
        '''
        데이터 수신 Thread를 생성하고 시작한다.
        '''
        t = Thread(target=self.receive_message, args=(self.client_socket,))
        t.start()

    def receive_message(self, so):
        '''
        Server로부터 message를 수신하고 문서창에 표시한다.
        '''
        while True:
            buf = so.recv(256)
            # 연결이 종료됨
            if not buf:
                break
            if(buf.decode('utf-8') == "채팅"):
                buf = so.recv(256)
                now = datetime.datetime.now()  # + datetime.timedelta(seconds=20)
                nowTime = now.strftime('%H:%M')
                self.chat_transcript_area.insert('end', buf.decode('utf-8') + '\n')
                self.chat_transcript_area.yview(END)
                self.chat_time_area.insert('end', nowTime + '\n')
                self.chat_time_area.yview(END)

            if(buf.decode('utf-8') == "공지"):
                buf = so.recv(256)
                now = datetime.datetime.now()  # + datetime.timedelta(seconds=20)
                nowTime = now.strftime('%H:%M')
                self.text.set(buf.decode('utf-8'))
                self.chat_transcript_area.insert('end', buf.decode('utf-8') + '\n')
                self.chat_transcript_area.yview(END)
                self.chat_time_area.insert('end', nowTime + '\n')
                self.chat_time_area.yview(END)

        so.close()

if __name__ == "__main__":
    ip = input("server IP addr: ")
    if ip == '':
        ip = '127.0.0.1'
    port = 2500
    ChatClient(ip, port)
    mainloop()