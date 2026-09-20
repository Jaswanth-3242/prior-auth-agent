from pathlib import Path

import pymupdf  # PyMuPDF
from PIL import Image

from app.utils.ocr import image_to_text


class DocumentAgent:
    """
    Responsible for converting supported documents into text.
    """

    SUPPORTED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".txt"}

    def process(self, file_path: str) -> dict:
        """
        Process a document and return extracted text.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {path.suffix}"
            )

        extension = path.suffix.lower()

        if extension == ".pdf":
            text = self._process_pdf(path)

        elif extension in {".png", ".jpg", ".jpeg"}:
            text = self._process_image(path)

        elif extension == ".txt":
            text = self._process_text(path)

        else:
            raise ValueError("Unsupported document type")

        return {
            "filename": path.name,
            "file_type": extension,
            "text": text,
        }

    def _process_pdf(self, path: Path) -> str:
        """
        Extract text from a PDF.

        First attempts normal PDF text extraction.
        If no useful text is found, OCR will be used.
        """

        document = pymupdf.open(path)

        extracted_text = []

        for page in document:
            text = page.get_text()

            if text.strip():
                extracted_text.append(text)

        text = "\n".join(extracted_text).strip()

        document.close()

        if text:
            return text

        # No selectable text → probably scanned PDF.
        # Render pages and run OCR.
        document = fitz.open(path)

        ocr_text = []

        for page in document:
            pixmap = page.get_pixmap()

            image = Image.frombytes(
                "RGB",
                [pixmap.width, pixmap.height],
                pixmap.samples,
            )

            ocr_text.append(image_to_text(image))

        document.close()

        return "\n".join(ocr_text).strip()

    def _process_image(self, path: Path) -> str:
        """
        Extract text from an image using OCR.
        """

        image = Image.open(path)

        return image_to_text(image)

    def _process_text(self, path: Path) -> str:
        """
        Read a plain text file.
        """

        return path.read_text(encoding="utf-8").strip()