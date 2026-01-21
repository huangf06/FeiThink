
import re

with open('/mnt/e/FeiThink/Demons.S01E04.en.srt', 'r', encoding='utf-8') as f:
    content = f.read()

blocks = re.split(r'\n\s*\n', content.strip())
print(f"Total blocks: {len(blocks)}")
print("Last block sample:")
print(blocks[-1])
