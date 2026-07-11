# TokenShield
A lightweight, secure terminal based Password Manager and 2FA TOTP Authenticator written in Python.

## Features
1. Secure Encryption: Protects your data using AES (Fernet) and PBKDF2HMAC key derivation with 480,000 iterations and a secure salt.

2. Integrated 2FA (TOTP): Generates current 2FA live codes directly in your terminal (pyotp). -> You dont need to grab your phone and scan the QR Code in order to authenticate yourself. All on the PC

3. QR-Code Scanner: Automatically extracts 2FA secrets from QR-code images using OpenCV.

4. Password Generator: Built-in generator for secure random passwords.

## Requirements & Installation
### 1. Prerequisites

Make sure you have Python 3.8+ installed on your system.
If dou dont, go to https://www.python.org/downloads/ or follow the instruction:
#### Windows:

```bash
winget install -e --id Python.Python.3
```

#### Linux:

```
sudo apt update && sudo apt install -y python3 python3-pip
```

#### macOS: Through the python website linked above is the best option 


### 2. Install Dependencies

```
pip install cryptography platformdirs rich pyotp opencv-python
```

### 3. File Structure

To ensure the script runs correctly, make sure all three project files are in the same folder. Example:
<br>
<br>
```text
TokenShield/
│
├── main.py                            # Main Function
├── totp_handler.py                    # Generates current TOTP code
└── qr_handler.py                      # Reads the QR Code
```

## How to run
Navigate to your project directory and doubble click the script Password.py <br> <br>
**Note:** If this doesnt work, in the explorer go to the folder with the files. Right click on an empty spot and click "Open in Terminal". Then execute:
```text
python Passwords.py
```

## First Start
When you run the program for the first time, it will ask you to set a Master Password. This password is used to encrypt your vault file (vault.json).

⚠️ Important: If you lose your Master Password, there is no way to recover your data!

## Main Menu Options

1. **See every Entry:** Displays a table of all saved data / accounts, including live 2FA codes (Passwords remain hidden as •••••••• for security).

2. **Search Entry:** Search for a specific website or app name to reveal the actual password.

3. **Add Entry:** Add a new account. You can auto generate a password and add a QR code image to automatically link 2FA.

4. **Delete Entry:** Removes an entry from your vault.

5. **Change Master Password:** Change the Master Password.

6. **Password Generator:** Quickly generate a secure random password of any length.

7. **Close:** Closes the application.

## Security Specifications
1. KDF: PBKDF2HMAC (SHA256)

2. Cycles: 480,000

3. Encryption standard: Fernet (AES-128 in CBC mode with HMAC-SHA256 authentication)

4. Storage Location: Handled by platformdirs: 


**Windows:** ` C:\Users\<user>\AppData\Local\TokenShield `

**Linux:** ` /home/<user>/.local/share/TokenShield `

**macOS:** `/Users/<user>/Library/Application Support/TokenShield`

## License
AGPL-3.0 License
