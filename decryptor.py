import os
import sys
from cryptography.fernet import Fernet

# Use same key as the one used for encryption
key = sys.argv[1].encode() # get the key from the command line
cipher = Fernet(key)

# Walk through the directory and encrypt the files | "" means the current directory
for root, _, files in os.walk(""):
    for file in files:
        # U can change the extension to decrypt other files, example .txt, .ps1, .sh, ... for this example we will decrypt .locked files
        if file.endswith((".locked")):
            file_path = os.path.join(root, file)
            
            try:
                with open(file_path, "rb") as f:
                    data = f.read()
                decrypted = cipher.decrypt(data)

                original = file_path.replace(".locked", "")

                with open(original, "wb") as f:
                    f.write(decrypted)

                os.remove(file_path)
            except:
                pass

print(f"\n[!] All files have been decrypted successfully!\n")