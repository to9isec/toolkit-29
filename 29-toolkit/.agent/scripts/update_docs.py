import os
import re
import glob

DOCS_PATHS = [
    "docs/*.md",
    "src/modules/gcc/docs/*.md",
    "src/modules/csm/docs/*.md"
]

NEW_DATE = "05/03/2026"
NEW_VERSION = "2.31.7"

def update_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        
        # Update Date
        content = re.sub(
            r'(\*\*Última Atualização:\*\*\s*)\d{2}/\d{2}/\d{4}', 
            rf'\g<1>{NEW_DATE}', 
            content
        )
        
        # Update Version
        content = re.sub(
            r'(\*\*Versão do Sistema:\*\*\s*)\d+\.\d+\.\d+', 
            rf'\g<1>{NEW_VERSION}', 
            content
        )
        content = re.sub(
            r'(\*\*Versão:\*\*\s*)\d+\.\d+\.\d+', 
            rf'\g<1>{NEW_VERSION}', 
            content
        )

        # Update Headers like FUSIONONE v2.x.x
        content = re.sub(
            r'(FUSIONONE v)\d+\.\d+\.\d+', 
            rf'\g<1>{NEW_VERSION}', 
            content
        )

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {filepath}")
            return True
        return False
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

updated_count = 0
for path_pattern in DOCS_PATHS:
    for filepath in glob.glob(path_pattern):
        if update_file(filepath):
            updated_count += 1

print(f"Script finished. Updated {updated_count} files.")
