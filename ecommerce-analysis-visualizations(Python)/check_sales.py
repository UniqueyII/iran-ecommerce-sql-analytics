# check_sales.py
import os

analysis_folder = 'src/analysis'
if os.path.exists(analysis_folder):
    files = os.listdir(analysis_folder)
    print(f"📁 Files in {analysis_folder}: {files}")
else:
    print(f"❌ Folder {analysis_folder} not found")