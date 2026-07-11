import cv2
import pyotp
from rich.console import Console

console = Console()

def extract_totp_secret_from_qr(image_path: str) -> str:

    try:

        img = cv2.imread(image_path)
        if img is None:
            console.print("[red]❌ Bild konnte nicht geladen werden. Pfad korrekt?[/red]")
            return None

        # weißer rand damit opencv erkennt
        white = [255, 255, 255]
        img_with_border = cv2.copyMakeBorder(
            img, 20, 20, 20, 20,
            borderType=cv2.BORDER_CONSTANT,
            value=white
        )


        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(img_with_border)

        if not data:
            console.print("[red]❌ Kein QR-Code im Bild gefunden (trotz Optimierung).[/red]")
            return None

        totp_obj = pyotp.parse_uri(data)
        return totp_obj.secret

    except Exception as e:
        console.print(f"[red]❌ Fehler beim Verarbeiten des QR-Codes: {e}[/red]")
        return None