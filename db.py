import sqlite3, bcrypt, os
from user import User, Student, Tutor

con = sqlite3.connect("data.db", check_same_thread=False)
cur = con.cursor()


def email_taken(email: str) -> bool:
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    return cur.fetchone() is not None


def create_user(
    type: str, first_name: str, last_name: str, email: str, password: str
) -> User:
    password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    cur.execute(
        "INSERT INTO users (type, first_name, last_name, email, password) VALUES (?, ?, ?, ?, ?)",
        (type, first_name, last_name, email, password),
    )
    con.commit()
    # Get the id of the user that was just created
    id = cur.lastrowid
    return User(id, type, first_name, last_name, email, password)


def get_user(email: str) -> User:
    cur.execute(f"SELECT * FROM Users WHERE email='{email}'")
    user = cur.fetchone()
    if user is None:
        return None
    return User(*user)


def check_password(user: User, password: str):
    return bcrypt.checkpw(password.encode(), user.password.encode())


# TESTING

if __name__ == "__main__":
    try:
        user = create_user("student", "John", "Doe", "john.d@email.com", "testPW")
    except sqlite3.Error as e:
        print(e)
    else:
        print(user.id)
