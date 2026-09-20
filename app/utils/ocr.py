from PIL import Image
import pytesseract


def image_to_text(image: Image.Image) -> str:
    """
    Convert an image into text using Tesseract OCR.
    """
    text = pytesseract.image_to_string(image)

    return text.strip()