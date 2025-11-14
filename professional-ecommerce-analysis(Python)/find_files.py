# find_files.py - Run this to see where everything is

import os

def find_all_files():
    current_dir = os.getcwd()
    print(f"🔍 Searching in: {current_dir}")
    print("\n📁 ALL FILES AND FOLDERS:")
    
    for root, dirs, files in os.walk(current_dir):
        # Get relative path
        level = root.replace(current_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}📁 {os.path.basename(root)}/')
        
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            if file.endswith('.py'):
                print(f'{subindent}📄 {file}')

if __name__ == "__main__":
    find_all_files()