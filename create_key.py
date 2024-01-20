from cryptography.fernet import Fernet
from os.path import join


print("This tool creates an encryption key and writes it to a file"
      "in the specified directory")
path = input("Enter path to create key file in: ")
key = Fernet.generate_key()
file_path = join(path, 'testkey.key')
with open(file_path, 'wb') as testkey:
    testkey.write(key)
print(f'key file written to {path}')