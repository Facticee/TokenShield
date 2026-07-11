import cv2
import pyotp
from rich.console import Console

console = Console()

def extract_totp_secret_from_qr(image_path: str) -> str:
    try:

        img = cv2.imread(image_path)
        if img is None:
            console.print("[red]❌ Image couldnt be loaded. Right Path?[/red]")
            return None

        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(img)

        if not data:
            console.print("[red]❌ No QR Code found.[/red]")
            return None

        totp_obj = pyotp.parse_uri(data)
        return totp_obj.secret

    except Exception as e:
        console.print(f"[red]❌ Error while processing QR Code: {e}[/red]")
        return None