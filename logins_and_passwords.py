import os

filename = "logins_and_passwords.txt"

if not os.path.exists(filename):
    with open(filename, "w") as file:
        pass  # Ничего не делаем, просто создаем пустой файл
    print(f"Файл {filename} успешно создан.")
else:
    print(f"Файл {filename} уже существует.")

def get_accounts_data():
    if not os.path.exists(filename):
        print(f"Файл {filename} не существует.")
        return []

    with open(filename, "r") as file:
        lines = file.readlines()

    lines = [line.strip().split() for line in lines]  # Удаляем символы новой строки

    return lines
