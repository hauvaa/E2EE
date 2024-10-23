from Crypto.Util.Padding import pad, unpad
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import socket
import threading

# Biến toàn cục để kiểm soát trạng thái dừng
running = True

# Tạo khóa ECC
def generate_keys():
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    return private_key, public_key

# Mã hóa thông điệp bằng AES
def encrypt_AES(shared_key, message):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(shared_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_message = pad(message, algorithms.AES.block_size)
    cipher_text = encryptor.update(padded_message) + encryptor.finalize()
    return iv + cipher_text

# Giải mã thông điệp bằng AES
def decrypt_AES(shared_key, cipher_text):
    iv = cipher_text[:16]
    cipher_text = cipher_text[16:]
    cipher = Cipher(algorithms.AES(shared_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_message = decryptor.update(cipher_text) + decryptor.finalize()
    return unpad(padded_message, algorithms.AES.block_size)

# Chữ ký ECC
def sign_ECC(private_key, message):
    return private_key.sign(message, ec.ECDSA(hashes.SHA256()))

# Xác thực chữ ký
def verify_ECC(public_key, signature, message):
    try:
        public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
        return True
    except Exception:
        return False

# Hàm gửi tin nhắn tới client
def send_message_to_client(client, server_private_key, shared_key):
    while running:
        message = input("Enter message to send to client: ")
        if message.lower() == 'exit':
            break
        message_bytes = message.encode('utf-8')
        cipher_text = encrypt_AES(shared_key, message_bytes)
        signature = sign_ECC(server_private_key, message_bytes)

        client.sendall(len(cipher_text).to_bytes(4, 'big'))  # Gửi độ dài phản hồi
        client.sendall(cipher_text)  # Gửi phản hồi
        client.sendall(len(signature).to_bytes(4, 'big'))
        client.sendall(signature)

# Hàm nhận tin nhắn từ client
def receive_message_from_client(client, client_public_key, shared_key, addr):
    while running:
        try:
            length_data = client.recv(4)
            if not length_data:
                print(f"Client {addr} has closed the connection.")
                break
            cipher_text_length = int.from_bytes(length_data, 'big')

            cipher_text = b""
            while len(cipher_text) < cipher_text_length:
                part = client.recv(cipher_text_length - len(cipher_text))
                if not part:
                    print(f"Client {addr} has closed the connection.")
                    break
                cipher_text += part

            # Nhận chữ ký
            signature_length_data = client.recv(4)
            signature_length = int.from_bytes(signature_length_data, 'big')
            signature = client.recv(signature_length)

            if not cipher_text or not signature:
                print("Cipher text or signature is missing.")
                break

            # Giải mã và xác thực
            decrypted_message = decrypt_AES(shared_key, cipher_text)

            if verify_ECC(client_public_key, signature, decrypted_message):
                print(f"Received from {addr}: {decrypted_message.decode('utf-8')}")
            else:
                print(f"Invalid signature from {addr}!")
        except Exception as e:
            print(f"Error receiving message from {addr}: {e}")
            break

    client.close()
    print(f"Connection from {addr} closed.")

# Hàm gửi tin nhắn đến server
def send_message_to_server(client, shared_key, client_private_key):
    global running
    while running:
        message = input("Enter message to send (or 'exit' to quit): ")
        if message.lower() == 'exit':
            running = False
            break
        message_bytes = message.encode('utf-8')
        cipher_text = encrypt_AES(shared_key, message_bytes)

        signature = sign_ECC(client_private_key, message_bytes)

        # Gửi cả ciphertext và chữ ký
        client.sendall(len(cipher_text).to_bytes(4, 'big'))  # Gửi độ dài ciphertext (4 byte)
        client.sendall(cipher_text)  # Gửi ciphertext
        client.sendall(len(signature).to_bytes(4, 'big'))  # Gửi độ dài chữ ký
        client.sendall(signature)  # Gửi chữ ký

# Hàm nhận phản hồi từ server
def receive_message_from_server(client, server_public_key, shared_key):
    global running
    while running:
        try:
            # Nhận độ dài ciphertext từ server (4 byte)
            response_length_data = client.recv(4)
            if not response_length_data:
                break
            response_ciphertext_length = int.from_bytes(response_length_data, 'big')

            # Nhận ciphertext từ server
            response_cipher = b""
            while len(response_cipher) < response_ciphertext_length:
                part = client.recv(response_ciphertext_length - len(response_cipher))
                if not part:
                    break
                response_cipher += part

            # Nhận độ dài chữ ký từ server (4 byte)
            signature_length_data = client.recv(4)
            signature_length = int.from_bytes(signature_length_data, 'big')
            signature = client.recv(signature_length)

            if not response_cipher or not signature:
                print("Missing cipher or signature")
                break

            # Giải mã ciphertext
            decrypted_response = decrypt_AES(shared_key, response_cipher)

            # Xác thực chữ ký bằng public key của server
            if verify_ECC(server_public_key, signature, decrypted_response):
                print("Server response:", decrypted_response.decode('utf-8'))
            else:
                print("Invalid server signature!")

        except Exception as e:
            print(f"Error receiving message: {e}")
            break

    client.close()
    print("Client closed.")

# Khởi động client và bắt đầu các luồng
def start_client():
    global running
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.1.12', 8080))  # Thay 'server_ip_address' bằng địa chỉ IP của máy A

    # Tạo cặp khóa cho client
    client_private_key, client_public_key = generate_keys()

    # Gửi public key của client đến server
    client_public_key_pem = client_public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )
    client.sendall(client_public_key_pem)

    # Nhận public key từ server
    server_public_key_pem = client.recv(1024)
    server_public_key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), server_public_key_pem)

    # Tạo khóa chia sẻ
    shared_key = client_private_key.exchange(ec.ECDH(), server_public_key)

    # Tạo luồng để gửi và nhận tin nhắn
    send_thread = threading.Thread(target=send_message_to_server, args=(client, shared_key, client_private_key))
    receive_thread = threading.Thread(target=receive_message_from_server, args=(client, server_public_key, shared_key))

    # Chạy luồng gửi và nhận
    send_thread.start()
    receive_thread.start()

    # Đợi các luồng hoàn thành
    send_thread.join()
    receive_thread.join()

def start_server():
    global running
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen()
    print("Server started...")

    while running:
        client, addr = server.accept()
        print(f"Connection from {addr} has been established!")

        # Tạo khóa mới cho server
        server_private_key, server_public_key = generate_keys()

        # Gửi public key của server đến client
        server_public_key_pem = server_public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint
        )
        client.sendall(server_public_key_pem)

        # Nhận public key từ client
        client_public_key_pem = client.recv(1024)
        client_public_key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), client_public_key_pem)

        # Tạo khóa chia sẻ
        shared_key = server_private_key.exchange(ec.ECDH(), client_public_key)

        # Tạo luồng để gửi và nhận tin nhắn từ client
        receive_thread = threading.Thread(target=receive_message_from_client, args=(client, client_public_key, shared_key, addr))
        receive_thread.start()

        send_thread = threading.Thread(target=send_message_to_client, args=(client, server_private_key, shared_key))
        send_thread.start()

        # Kết thúc khi gửi xong tin nhắn
        send_thread.join()
        receive_thread.join()

    server.close()
    print("Server closed.")


if __name__ == "__main__":
    start_server()
