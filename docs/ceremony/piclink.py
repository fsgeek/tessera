from pathlib import Path

for cosa in Path("../../tmp/ceremony/").iterdir():
    print(f"\n![{cosa.name}]({cosa})")
