import pyotp

def generate_current_totp(secret: str) -> str:

    if not secret or secret == "-":
        return "-"
    try:
        totp = pyotp.TOTP(secret)
        return totp.now()
    except Exception:
        return "Error"