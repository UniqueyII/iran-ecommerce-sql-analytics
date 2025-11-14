# Add this to your requirements or install:
# pip install python-bidi arabic-reshaper

from bidi.algorithm import get_display
import arabic_reshaper

def _persian_text(self, text):
    """Properly render Persian text"""
    try:
        reshaped_text = arabic_reshaper.reshape(text)
        return get_display(reshaped_text)
    except:
        return text

# Then use it in your labels:
province_name = self._persian_text(row['province'])