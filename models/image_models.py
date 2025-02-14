from typing import Dict, Optional
from datetime import datetime
from docling.document import Document
from pydantic import BaseModel, Field

class ImageQuality(BaseModel):
    """Quality metrics for processed images"""
    clarity: float = Field(description="Image clarity score between 0 and 1")
    contrast: float = Field(description="Image contrast level between 0 and 1")
    resolution: float = Field(description="Effective resolution score between 0 and 1")
    noise_level: Optional[float] = Field(None, description="Image noise level if detectable")

class OCRMetrics(BaseModel):
    """Metrics for OCR text extraction"""
    word_count: int = Field(description="Total number of words in extracted text")
    line_count: int = Field(description="Number of text lines detected")
    paragraph_count: int = Field(description="Number of paragraphs identified")
    char_count: int = Field(description="Total character count")
    confidence_score: float = Field(
        description="OCR confidence score",
        ge=0,
        le=1
    )

class ImageAnalysisResult(Document):
    """Complete result of image analysis including OCR and quality metrics"""
    enhanced_text: str = Field(
        description="Enhanced and formatted text from image",
        examples=["This is a sample of enhanced text with proper formatting"]
    )
    original_ocr: str = Field(description="Raw OCR output before enhancement")
    metrics: OCRMetrics
    image_quality: ImageQuality
    analysis_timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        schema_extra = {
            "example": {
                "enhanced_text": "Sample enhanced text",
                "original_ocr": "Raw OCR output",
                "metrics": {
                    "word_count": 100,
                    "line_count": 10,
                    "paragraph_count": 3,
                    "char_count": 500,
                    "confidence_score": 0.95
                },
                "image_quality": {
                    "clarity": 0.8,
                    "contrast": 0.7,
                    "resolution": 0.9,
                    "noise_level": 0.1
                }
            }
        }