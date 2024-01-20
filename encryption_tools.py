from cryptography.fernet import Fernet
from os.path import join

print("This tool reads an existing encryption key file, "
      "queries for a username and password and writes "
      "the encrypted results to another file.")
path = input("Enter path to files: ")
user_name = input("UserName: ")
pass_word = input("Password: ")
file_path = join(path, 'testkey.key')

with open(file_path, 'rb') as testkey:
    key = testkey.read()

ekey = Fernet(key)
encryptU = ekey.encrypt(user_name.encode('utf-8'))
encryptP = ekey.encrypt(pass_word.encode('utf-8'))
file_path = join(path, 'encryption.txt')

with open(file_path, 'wb') as file:
    file.write(encryptU + b'\n')
    file.write(encryptP)

with open(file_path, 'rb') as file:
    encrypted = file.readlines()
    username = ekey.decrypt(encrypted[0]).decode("utf8")
    password = ekey.decrypt(encrypted[1]).decode("utf8")

print(username, password)
