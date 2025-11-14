# src/analysis/font_utils.py
"""
Utility functions for Persian/Arabic text support in matplotlib
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from bidi.algorithm import get_display
import arabic_reshaper
import os

def setup_persian_font():
    """Setup Persian/Arabic font support for matplotlib using bidi and arabic_reshaper"""
    try:
        # For newer versions of arabic_reshaper, we don't need config
        # It automatically detects Farsi/Persian
        
        # Try to find a font that supports Persian characters
        persian_fonts = [
            'B Nazanin', 
            'Iranian Sans', 
            'Tahoma', 
            'Arial',
            'DejaVu Sans',
            'Vazir',
            'Segoe UI'
        ]
        
        available_fonts = [f.name for f in fm.fontManager.ttflist]
        selected_font = 'DejaVu Sans'  # Default fallback
        
        for font in persian_fonts:
            if any(font.lower() in f_name.lower() for f_name in available_fonts):
                selected_font = font
                break
        
        plt.rcParams['font.family'] = selected_font
        plt.rcParams['axes.unicode_minus'] = False
        print(f"✅ Using font: {selected_font}")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Font setup warning: {e}")
        return False

def persian_text(text):
    """Convert text to properly displayed Persian text using bidi and reshaper"""
    try:
        if text is None:
            return ""
            
        text_str = str(text)
        
        # Check if text contains Persian/Arabic characters
        if any('\u0600' <= char <= '\u06FF' for char in text_str):
            # This is Persian/Arabic text - reshape and apply bidi
            reshaped_text = arabic_reshaper.reshape(text_str)
            bidi_text = get_display(reshaped_text)
            return bidi_text
        else:
            # This is English or other text
            return text_str
    except Exception as e:
        print(f"⚠️  Text conversion error for '{text}': {e}")
        return str(text)