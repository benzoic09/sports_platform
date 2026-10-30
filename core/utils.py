import io
import base64
import qrcode


def make_qr(text):
    """Return a QR code image of `text` as a base64 string."""
    image = qrcode.make(text)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()