import tkinter as tk
from tkinter import messagebox


class KeyInfoWindow:
    def __init__(self, root, private_key, public_key, shared_key, peer_public_key, source):
        # Cửa sổ mới hiển thị thông tin khóa
        self.window = tk.Toplevel(root)
        self.window.title(f"{source}")
        self.window.geometry("600x600")  # Giới hạn kích thước cửa sổ là 600x600

        # Hiển thị khóa riêng (Private Key)
        tk.Label(self.window, text="Khóa riêng của máy (Private Key):").grid(row=0, column=0, sticky="w")
        tk.Label(self.window, text=str(private_key), wraplength=580, anchor="w").grid(row=0, column=1, sticky="w")

        # Hiển thị khóa công khai (Public Key)
        tk.Label(self.window, text="Khóa công khai của máy (Public Key):").grid(row=1, column=0, sticky="w")
        tk.Label(self.window, text=str(public_key), wraplength=580, anchor="w").grid(row=1, column=1, sticky="w")

        # Hiển thị khóa chia sẻ (Shared Key)
        tk.Label(self.window, text="Khóa chia sẻ (Shared Key):").grid(row=2, column=0, sticky="w")
        tk.Label(self.window, text=str(shared_key), wraplength=580, anchor="w").grid(row=2, column=1, sticky="w")

        # Hiển thị khóa công khai từ đối phương (Peer Public Key)
        tk.Label(self.window, text="Khóa công khai từ đối phương (Peer Public Key):").grid(row=3, column=0, sticky="w")
        tk.Label(self.window, text=str(peer_public_key), wraplength=580, anchor="w").grid(row=3, column=1, sticky="w")

        # Thêm label để hiển thị chữ ký
        self.signature_label = tk.Label(self.window, text="Chữ ký (Signature):")
        self.signature_label.grid(row=4, column=0, sticky="w")
        self.signature_value = tk.Label(self.window, text="Chưa có chữ ký", wraplength=580, anchor="w")
        self.signature_value.grid(row=4, column=1, sticky="w")

        # Nút đóng cửa sổ
        tk.Button(self.window, text="Đóng", command=self.window.destroy).grid(row=5, column=0, columnspan=2)

    def update_signature_display(self, signature, action_type):
        # Cập nhật chữ ký mới trong cửa sổ
        self.signature_value.config(text=f"{action_type} - {signature.hex()}")


def display_key_info(private_key, public_key, shared_key, peer_public_key, source):
    # Tạo cửa sổ Tkinter chính
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ gốc

    # Tạo cửa sổ hiển thị thông tin khóa
    KeyInfoWindow(root, private_key, public_key, shared_key, peer_public_key, source)
    root.mainloop()
