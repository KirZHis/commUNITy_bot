import sqlite3

def www():
    conn = sqlite3.connect('Answers.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE Answers (
        ID INT PRIMARY KEY,
        Name VARCHAR(255),
        Age INT,
        City VARCHAR(255),
        About VARCHAR(255),
        Profession VARCHAR(255),
        State INT
    )''')

    conn.close()
