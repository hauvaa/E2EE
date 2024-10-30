Mô hình E2EE
1. Chức năng của Sản phẩm
  Tạo phòng chat: Cho phép người dùng khởi tạo một phòng chat như một server để nhận và gửi tin nhắn được mã hóa.
  Tham gia phòng chat: Cho phép người dùng kết nối tới server (phòng chat) bằng địa chỉ IP của server đã tạo trước đó.
  Mã hóa và Giải mã: Sử dụng mã hóa đối xứng AES (Advanced Encryption Standard) và chữ ký số ECC (Elliptic Curve Cryptography) để đảm bảo tính bảo mật và toàn vẹn của các tin nhắn.
  Chữ ký số và xác thực: Tạo chữ ký số ECC cho mỗi tin nhắn để xác thực nguồn gốc tin nhắn giữa người gửi và người nhận.
  Giao diện người dùng: Hiển thị các tin nhắn được gửi và nhận trên giao diện đồ họa (GUI) với tính năng nhập và gửi tin nhắn dễ dàng.
2. Yêu cầu Phần cứng và Phần mềm
  Phần cứng
    CPU: Tối thiểu Intel i3 hoặc tương đương
    RAM: 4GB trở lên
    Mạng: Kết nối internet hoặc mạng cục bộ (LAN) cho các máy khách và máy chủ kết nối
  Phần mềm
    Python: Phiên bản 3.8 hoặc mới hơn
  Thư viện bổ sung:
    pycryptodome hoặc cryptography: Để xử lý mã hóa và giải mã AES và ECC
    tkinter: Để xây dựng giao diện người dùng
3. Cách sử dụng
  Tạo phòng chat:
    Mở ứng dụng và chọn Khởi tạo phòng chat.
    Địa chỉ IP của server sẽ được hiển thị để chia sẻ với các máy khách muốn tham gia.
  Tham gia phòng chat:
    Nhập địa chỉ IP của server để kết nối và chọn Tham gia phòng chat.
  Gửi và nhận tin nhắn:
    Sử dụng khung nhập liệu để nhập tin nhắn và nhấn nút Gửi.
    Các tin nhắn sẽ được mã hóa, ký, và gửi đi, đảm bảo rằng chúng được bảo mật khi truyền qua mạng.
4. Các Thông tin Khác
   Ứng dụng sử dụng ECC và AES để bảo vệ các tin nhắn khỏi các tấn công bên thứ ba, đảm bảo tính toàn vẹn và bảo mật.
