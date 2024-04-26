# Ransomwarehehe

1. Attacker sẽ gen pairs key bằng cách run `gen_pairs_key_attacker.py` 
2. Những file bên ngoài là những file trên máy attacker, Folder `Victim` tượng trưng cho những thứ xảy ra ở phía Victim, Folder `/Victim/Test` tượng trưng cho những file sẽ được mã hóa và giải
3. Nhúng `attacker_public_key.pem` vào `Ransomwarehehe.py`
4. Run Encryptor rồi xem các file trong folder test đã được mã hóa ![alt text](/Image/image.png)
5. Copy `victim_private_key_encrypted` ra folder ngoài, tượng trưng cho việc gửi file cho attacker sau khi trả tiền chuộc ![alt text](/Image/image-1.png)
6. Attacker run file `recover_victim_private_key.py` sau khi có file `victim_private_key.pem` copy vào folder `Victim/` tượng trưng cho việc attacker gửi file victim_private_key lại cho Victim ![alt text](/Image/image-2.png)
7. Victim run Decryptor và giải mã thành công các file trong folder `/Victim/Test` ![alt text](/Image/image-3.png)