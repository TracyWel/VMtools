from cryptography.fernet import Fernet
from os.path import join


def is_encrypted(text):
    """
    Uses the assumption that encrypted text should have an even distribution
    of letters to determine if it's encrypted.
    :param text: the text to be tested
    :return: True if encrypted
    """
    import collections
    from math import sqrt

    scores = collections.defaultdict(lambda: 0)
    for letter in text: scores[letter] += 1
    largest = max(scores.values())
    average = len(text) / 256.0
    return largest < average + 5 * sqrt(average)


print("This tool reads an existing encryption key file, "
      "queries for a username and password and writes "
      "the encrypted results to another file.")
path = input("Enter path to files: ")
user_name = input("UserName: ")
pass_word = input("Password: ")

if is_encrypted(user_name):
    print(f'UserName {user_name} appears to already be encrypted. Exiting')
    exit(-1)
if is_encrypted(pass_word):
    print(f'Password {pass_word} appears to already be encrypted. Exiting')
    exit(-1)

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
