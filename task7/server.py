import socket

HOST = '127.0.0.1'  
PORT = 65432       


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server is listening on {HOST}:{PORT}")
        conn, addr = s.accept()
        with conn:
            print('Connected to', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print("Received from client:", data.decode())
                response = input("Reply to client: ")
                conn.sendall(response.encode())


if __name__ == "__main__":
    main()
