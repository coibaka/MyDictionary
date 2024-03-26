# Xây dựng một mô hình ngôn ngữ Tiếng Việt và lưu trữ dữ liệu vào cơ sở dữ liệu SQLite3:

import sqlite3
from transformers import AutoModel, AutoTokenizer
import torch

# import sqlite3

# Định nghĩa một context manager để quản lý kết nối cơ sở dữ liệu
class DatabaseConnection:
    def __init__(self, db):
        self.db = db
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type or exc_val or exc_tb:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()

""" # Sử dụng context manager với câu lệnh 'with'
with DatabaseConnection('vietnamese_nlp.db') as conn:
    cursor = conn.cursor()
    # Thực hiện các truy vấn ở đây
    cursor.execute('YOUR SQL QUERY HERE')
    # Không cần phải gọi conn.close() vì nó sẽ tự động được gọi """

# Khởi tạo mô hình và tokenizer
model_name = "vinai/phobert-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)


# Sử dụng context manager với câu lệnh 'with'
with DatabaseConnection('vietnamese_nlp.db') as conn:
    
    # Kết nối đến cơ sở dữ liệu SQLite
    conn = sqlite3.connect('vietnamese_nlp.db')
    c = conn.cursor()

    # Tạo bảng để lưu trữ dữ liệu
    c.execute('''CREATE TABLE IF NOT EXISTS sentences (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, embedding BLOB)''')

# Hàm để thêm câu và embedding vào cơ sở dữ liệu
def add_sentence_to_db(sentence, cursor, connection):
    # Mã hóa câu để lấy embedding
    input_ids = tokenizer.encode(sentence, return_tensors='pt')
    with torch.no_grad():
        embedding = model(input_ids)[0].numpy()  # Lấy tensor đầu tiên và chuyển thành numpy array

    # Thêm câu và embedding vào cơ sở dữ liệu
    cursor.execute("INSERT INTO sentences (text, embedding) VALUES (?, ?)", (sentence, embedding.tobytes()))
    connection.commit()

# Ví dụ thêm một câu vào cơ sở dữ liệu
add_sentence_to_db("Chào mừng bạn đến với thế giới của NLP.", c, conn)

# Đóng kết nối cơ sở dữ liệu
#conn.close()


