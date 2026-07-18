# Educational File Locker (Ransomware Demo)

A minimal educational project that demonstrates how symmetric encryption can lock and unlock local files. It is **not** production malware and must only be run in a controlled environment you own (for example, this repository folder with the included sample `.txt` files).

---

## Warning / Disclaimer

- **Educational use only.** Do not run this against real documents, production systems, or machines you do not control.
- **Irreversible without the key.** When you run `ramsonware.py`, it prints a Fernet key to the terminal. **You must copy and save that key immediately.** Later you pass it as an argument to `decryptor.py`. If you close the terminal, lose the key, or overwrite it without saving it, **the encrypted files cannot be recovered** and the original content is gone.
- The encryptor **deletes the original `.txt` files** after writing the encrypted `.locked` copies. There is no backup step.
- Both scripts walk the **current working directory** (and subdirectories) via `os.walk("")`. Run them only from a safe test folder.
- Silent failures: file I/O / decrypt errors are swallowed with a bare `except: pass`, so a wrong key or a bad file may look like “success” while some files remain locked.
- You are solely responsible for any damage caused by misuse of this code.

---

## Project composition

| Path | Role |
|------|------|
| `ramsonware.py` | Encrypts target files, deletes originals, prints the decryption key |
| `decryptor.py` | Decrypts `.locked` files using a key passed on the command line |
| `a.txt`, `b.txt`, `c.txt`, `d.txt` | Sample plaintext files for safe local testing |
| `.gitignore` | Ignores a local `venv/` directory |
| `README.md` | This documentation |

**External dependency:** [`cryptography`](https://pypi.org/project/cryptography/) (Fernet authenticated encryption).

There is no `requirements.txt` in the repo; install the library manually (see below).

---

## How it works

### Encryption (`ramsonware.py`)

1. Generates a random Fernet key with `Fernet.generate_key()`.
2. Builds a `Fernet` cipher from that key.
3. Recursively walks the current directory.
4. For every file whose name ends with `.txt`:
   - Reads the file as bytes.
   - Encrypts the bytes with Fernet.
   - Writes the ciphertext to `<original_path>.locked` (e.g. `a.txt` → `a.txt.locked`).
   - Deletes the original `.txt` file.
5. Prints a success message and the key as a UTF-8 string, for example:

   ```text
   [!] All files have been encrypted successfully!

   [!] key: <base64-url-safe-fernet-key>
   ```

**Save that key.** It is the only way to decrypt later.

By default only `.txt` files are encrypted. The extension filter is hardcoded in the script and can be changed for experiments (e.g. `.ps1`, `.sh`), but that increases risk.

### Decryption (`decryptor.py`)

1. Reads the Fernet key from `sys.argv[1]` and encodes it to bytes.
2. Builds a `Fernet` cipher with that key (must be the **same** key printed by `ramsonware.py`).
3. Recursively walks the current directory.
4. For every file ending with `.locked`:
   - Reads and decrypts the contents.
   - Writes the plaintext back to the path with `.locked` removed (e.g. `a.txt.locked` → `a.txt`).
   - Deletes the `.locked` file.
5. Prints a success message.

If the key is wrong, decryption fails per file (errors are ignored), and originals are not restored.

---

## Requirements

- Python 3.x
- `cryptography` package

```bash
pip install cryptography
```

Optional: use a virtual environment (ignored by `.gitignore` if named `venv/`):

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
pip install cryptography
```

---

## Usage

Run everything from the project directory so only the intended test files are affected.

### 1. Encrypt (and save the key)

```bash
python ramsonware.py
```

Example output:

```text
[!] All files have been encrypted successfully!

[!] key: gAAAAABl...your-key-here...
```

**Copy the key now** and store it somewhere safe (clipboard, note, password manager). Without it, decryption is impossible.

After a successful run, sample files look like:

- `a.txt.locked`
- `b.txt.locked`
- `c.txt.locked`
- `d.txt.locked`

The original `.txt` files are removed.

### 2. Decrypt (pass the saved key)

```bash
python decryptor.py "YOUR_SAVED_KEY_HERE"
```

Replace `YOUR_SAVED_KEY_HERE` with the exact string printed after encryption (quotes help if the shell would otherwise mangle the value).

After a successful run with the correct key, `.locked` files are removed and the `.txt` files are restored.

---

## Critical workflow note

```text
ramsonware.py  →  prints KEY  →  YOU MUST SAVE THE KEY
                         ↓
decryptor.py KEY  →  restores .txt files from .locked
```

| Step | Action |
|------|--------|
| 1 | Run `python ramsonware.py` |
| 2 | **Immediately copy the printed `key:` value** |
| 3 | Keep that key until you finish testing |
| 4 | Run `python decryptor.py "<key>"` to unlock |

If you skip step 2, the encrypted data is effectively lost: Fernet uses a random key each run, and the project does not write the key to disk.

---

## ⚠️ Customization notes

- **Target directory:** both scripts use `os.walk("")` (current directory). Change that path only if you understand the blast radius.
- **Encrypt filter:** in `ramsonware.py`, `file.endswith((".txt"))`.
- **Decrypt filter:** in `decryptor.py`, `file.endswith((".locked"))`.
- Encrypted output naming: original path + `.locked` suffix.

---

## ⚠️ What this project does *not* do

- No network C2, ransom note UI, persistence, or privilege escalation.
- No key escrow, key file on disk, or recovery mechanism.
- No confirmation prompt before encrypting/deleting files.
- No logging of which files failed.

---

## ⚠️ Safe testing checklist

1. Work only inside this repository (or a disposable copy of it).
2. Confirm you only care about the sample `.txt` files (or recreate them).
3. Run `python ramsonware.py`.
4. **Save the printed key before closing the terminal.**
5. Verify `.txt` files became `.locked`.
6. Run `python decryptor.py "<saved-key>"`.
7. Verify `.txt` files are restored and readable.

---

## License / ethics

Use this code only to learn about cryptography and file I/O on systems and data you own. Deploying or distributing ransomware against others is illegal and unethical.
