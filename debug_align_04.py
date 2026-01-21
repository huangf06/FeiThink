
import re
from check_translations_count import TRANSLATIONS

def main():
    with open('/mnt/e/FeiThink/Demons.S01E04.en.srt', 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = re.split(r'\n\s*\n', content.strip())
    
    limit = min(len(blocks), len(TRANSLATIONS))
    
    for i in range(475, 490):
        if i < limit:
            original_text = '\n'.join(blocks[i].split('\n')[2:])
            print(f"--- Block {i+1} --- (Index {i})")
            print(f"EN: {original_text}")
            print(f"ZH: {TRANSLATIONS[i]}")
            print("")

if __name__ == "__main__":
    main()
