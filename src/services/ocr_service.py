"""OCR service using lightweight open-source engines.

Supports multiple OCR engines:
- Tesseract: Most popular, supports 100+ languages  
- EasyOCR: Deep learning-based, high accuracy
- PaddleOCR: Lightweight, fast, good for mobile
"""

import os
import tempfile
from typing import Dict, List
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Check what's available at import time
TESSERACT_AVAILABLE = False
try:
    import pytesseract
    from PIL import Image
    import cv2
    import numpy as np
    TESSERACT_AVAILABLE = True
except ImportError:
    pass


class ImagePreprocessor:
    """Image preprocessing for better OCR accuracy."""
    
    @staticmethod
    def preprocess(image_path: str):
        """Preprocess image for OCR."""
        import cv2
        import numpy as np
        
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        thresh = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        return thresh


class TesseractOCR:
    """Tesseract OCR engine wrapper."""
    
    def __init__(self, lang: str = "eng"):
        self.lang = lang
    
    def extract_text(self, image_path: str, preprocess: bool = True) -> Dict:
        """Extract text using Tesseract."""
        import pytesseract
        from PIL import Image
        import cv2
        
        if preprocess:
            img = ImagePreprocessor.preprocess(image_path)
            temp_path = tempfile.mktemp(suffix='.png')
            cv2.imwrite(temp_path, img)
            image_path = temp_path
        
        img = Image.open(image_path)
        data = pytesseract.image_to_data(
            img, lang=self.lang, output_type=pytesseract.Output.DICT
        )
        text = pytesseract.image_to_string(img, lang=self.lang)
        
        confidences = [
            float(conf) for conf in data['conf']
            if conf != '-1' and str(conf).replace('.', '').isdigit()
        ]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        if preprocess and os.path.exists(temp_path):
            os.remove(temp_path)
        
        return {
            "text": text.strip(),
            "confidence": avg_confidence / 100.0,
            "word_count": len(text.split()),
            "language": self.lang,
            "engine": "tesseract",
        }


class EasyOCREngine:
    """EasyOCR engine wrapper - lazy loaded."""
    
    def __init__(self, languages: List[str] = None):
        self.languages = languages or ['en']
        self.reader = None
    
    def _ensure_reader(self):
        """Lazy load EasyOCR reader."""
        if self.reader is None:
            import easyocr
            self.reader = easyocr.Reader(self.languages, gpu=False)
    
    def extract_text(self, image_path: str, preprocess: bool = True) -> Dict:
        """Extract text using EasyOCR."""
        import cv2
        
        self._ensure_reader()
        
        if preprocess:
            img = ImagePreprocessor.preprocess(image_path)
            temp_path = tempfile.mktemp(suffix='.png')
            cv2.imwrite(temp_path, img)
            image_path = temp_path
        
        results = self.reader.readtext(image_path)
        text_parts = []
        confidences = []
        
        for (bbox, text, conf) in results:
            text_parts.append(text)
            confidences.append(conf)
        
        full_text = ' '.join(text_parts)
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        if preprocess and os.path.exists(temp_path):
            os.remove(temp_path)
        
        return {
            "text": full_text.strip(),
            "confidence": avg_confidence,
            "word_count": len(full_text.split()),
            "language": ','.join(self.languages),
            "engine": "easyocr",
        }


class PaddleOCREngine:
    """PaddleOCR engine wrapper - lazy loaded."""
    
    def __init__(self, lang: str = "en"):
        self.lang = lang
        self.ocr = None
    
    def _ensure_ocr(self):
        """Lazy load PaddleOCR."""
        if self.ocr is None:
            from paddleocr import PaddleOCR
            self.ocr = PaddleOCR(
                use_angle_cls=True,
                lang=self.lang,
                use_gpu=False,
                show_log=False
            )
    
    def extract_text(self, image_path: str, preprocess: bool = True) -> Dict:
        """Extract text using PaddleOCR."""
        import cv2
        
        self._ensure_ocr()
        
        if preprocess:
            img = ImagePreprocessor.preprocess(image_path)
            temp_path = tempfile.mktemp(suffix='.png')
            cv2.imwrite(temp_path, img)
            image_path = temp_path
        
        result = self.ocr.ocr(image_path, cls=True)
        text_parts = []
        confidences = []
        
        if result and result[0]:
            for line in result[0]:
                if len(line) >= 2:
                    text = line[1][0]
                    conf = line[1][1]
                    text_parts.append(text)
                    confidences.append(conf)
        
        full_text = ' '.join(text_parts)
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        if preprocess and os.path.exists(temp_path):
            os.remove(temp_path)
        
        return {
            "text": full_text.strip(),
            "confidence": avg_confidence,
            "word_count": len(full_text.split()),
            "language": self.lang,
            "engine": "paddleocr",
        }


class OCRService:
    """Unified OCR service supporting multiple engines."""
    
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=3)
        self._engines = {}
        self._initialize_engines()
    
    def _initialize_engines(self):
        """Initialize available OCR engines."""
        if TESSERACT_AVAILABLE:
            self._engines['tesseract'] = TesseractOCR
        
        # Check for easyocr
        try:
            import easyocr
            self._engines['easyocr'] = EasyOCREngine
        except ImportError:
            pass
        
        # Check for paddleocr
        try:
            from paddleocr import PaddleOCR
            self._engines['paddleocr'] = PaddleOCREngine
        except ImportError:
            pass
    
    def available_engines(self) -> List[str]:
        """Get list of available OCR engines."""
        return list(self._engines.keys())
    
    async def extract_text(
        self,
        image_path: str,
        engine: str = "auto",
        language: str = "en",
        preprocess: bool = True
    ) -> Dict:
        """Extract text from image using specified OCR engine."""
        start_time = datetime.utcnow()
        
        if engine == "auto":
            if "tesseract" in self._engines:
                engine = "tesseract"
            elif "easyocr" in self._engines:
                engine = "easyocr"
            elif "paddleocr" in self._engines:
                engine = "paddleocr"
            else:
                raise RuntimeError("No OCR engine available")
        
        if engine not in self._engines:
            raise ValueError(f"OCR engine '{engine}' not available")
        
        engine_class = self._engines[engine]
        
        if engine == "tesseract":
            ocr_engine = engine_class(lang=language)
        elif engine == "easyocr":
            ocr_engine = engine_class(languages=[language])
        else:
            ocr_engine = engine_class(lang=language)
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            self.executor,
            ocr_engine.extract_text,
            image_path,
            preprocess
        )
        
        end_time = datetime.utcnow()
        processing_time = (end_time - start_time).total_seconds()
        
        result["processing_time_seconds"] = processing_time
        result["timestamp"] = end_time.isoformat()
        
        return result
    
    async def extract_with_multiple_engines(
        self,
        image_path: str,
        languages: List[str] = None
    ) -> Dict[str, Dict]:
        """Extract text using all available engines."""
        languages = languages or ["en"]
        results = {}
        
        tasks = []
        for engine in self.available_engines():
            task = self.extract_text(
                image_path,
                engine=engine,
                language=languages[0]
            )
            tasks.append((engine, task))
        
        for engine, task in tasks:
            try:
                result = await task
                results[engine] = result
            except Exception as e:
                results[engine] = {
                    "error": str(e),
                    "engine": engine
                }
        
        return results


# Global OCR service instance
_ocr_service = None


def get_ocr_service() -> OCRService:
    """Get or create OCR service singleton."""
    global _ocr_service
    if _ocr_service is None:
        _ocr_service = OCRService()
    return _ocr_service
