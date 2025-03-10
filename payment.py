import sqlite3

db_name = "payment.db"

def create_user_pay_table():
    SQL = """
        CREATE TABLE IF NOT EXISTS pay (
            id INTEGER PRIMARY KEY,
            quanity INT,
            nomer INT,
            date TEXT,
            code INT
        )
    """
    con = sqlite3.connect(db_name)
    con.execute(SQL)
    con.commit() 

class Pay_user:
    def __init__(self, id, quanity, nomer, date, code):
        self.id = id
        self.quanity = quanity
        self.nomer = nomer
        self.date = date
        self.code = code
    
    @staticmethod
    def get_user_pay_by_id(id):
        SQL = """
            SELECT * FROM pay WHERE id = ?
        """
        con = sqlite3.connect(db_name)
        q = con.execute(SQL, (id))
        data = q.fetchall()
        if not data:
            return None
        return data

    @staticmethod
    def create_pay(quanity, nomer, date, code):
        SQL = """
            INSERT INTO pay(quanity, nomer, date, code)
            VALUES (?, ?, ?, ?)
        """
        con = sqlite3.connect(db_name)
        con.execute(SQL, (quanity, nomer, date, code))
        con.commit()  

