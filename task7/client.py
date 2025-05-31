import socket

HOST = '127.0.0.1'  
PORT = 65432        


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connected to server {HOST}:{PORT}")
        while True:
            msg = input("Message to server: ")
            s.sendall(msg.encode())
            data = s.recv(1024)
            print("Reply from server:", data.decode())


if __name__ == "__main__":
    main()
