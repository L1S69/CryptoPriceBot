import sqlite3  # Library for interacting with database


def get_data(chat_id, variable: str, default: str):
    with sqlite3.connect("preferences.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT {variable} FROM user_preferences WHERE chat_id = ?",
                       (chat_id,))  # Get data by user's chat_id
        result = cursor.fetchone()  # Get the first row of the result
        data = result[0] if result and result[0] != None else default  # Get the value if the result is not empty, otherwise set it to default
        return data


def set_data(chat_id, variable: str, value):
    with sqlite3.connect("preferences.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE user_preferences SET {variable} = ? WHERE chat_id = ?", (value, chat_id))
        conn.commit()
