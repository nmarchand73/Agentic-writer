"""
Replace w:fldSimple PAGE field (invalid in w:r) with proper
three-run OOXML complex field sequence in all footer XML files.
"""
import sys, os, re

unpacked_dir = sys.argv[1]
word_dir = os.path.join(unpacked_dir, 'word')

PAGE_FIELD_RUNS = '''\
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Palatino Linotype" w:cs="Palatino Linotype" w:hAnsi="Palatino Linotype"/>
        <w:color w:val="AAAAAA"/>
        <w:sz w:val="36"/>
        <w:szCs w:val="36"/>
      </w:rPr>
      <w:fldChar w:fldCharType="begin"/>
    </w:r>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Palatino Linotype" w:cs="Palatino Linotype" w:hAnsi="Palatino Linotype"/>
        <w:color w:val="AAAAAA"/>
        <w:sz w:val="36"/>
        <w:szCs w:val="36"/>
      </w:rPr>
      <w:instrText xml:space="preserve"> PAGE </w:instrText>
    </w:r>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Palatino Linotype" w:cs="Palatino Linotype" w:hAnsi="Palatino Linotype"/>
        <w:color w:val="AAAAAA"/>
        <w:sz w:val="36"/>
        <w:szCs w:val="36"/>
      </w:rPr>
      <w:fldChar w:fldCharType="end"/>
    </w:r>'''

patched = 0
for fname in sorted(os.listdir(word_dir)):
    if not fname.startswith('footer'):
        continue
    fpath = os.path.join(word_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Match the entire <w:r>...<w:fldSimple w:instr="PAGE".../>...</w:r> block
    new_content = re.sub(
        r'<w:r>\s*<w:rPr>.*?</w:rPr>\s*<w:fldSimple[^/]*/>\s*</w:r>',
        PAGE_FIELD_RUNS,
        content,
        flags=re.DOTALL
    )
    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        patched += 1
        print(f"Patched: {fname}")

print(f"Total patched: {patched} footer(s)")
