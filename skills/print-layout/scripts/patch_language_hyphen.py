"""
1. Set French language on all text runs in document.xml (enables FR hyphenation dict)
2. Write a correct settings.xml with autoHyphenation in proper OOXML element order
"""
import sys, os, re

unpacked_dir = sys.argv[1]
word_dir = os.path.join(unpacked_dir, 'word')

LANG_TAG = '<w:lang w:val="fr-FR" w:eastAsia="fr-FR" w:bidi="ar-SA"/>'

def add_lang(match):
    rpr = match.group(0)
    if 'w:lang' in rpr:
        return rpr
    return rpr.replace('</w:rPr>', f'  {LANG_TAG}\n    </w:rPr>')

# ── 1. Patch document.xml only ────────────────────────────────────────────
doc_path = os.path.join(word_dir, 'document.xml')
with open(doc_path, 'r', encoding='utf-8') as f:
    content = f.read()
new_content = re.sub(r'<w:rPr>.*?</w:rPr>', add_lang, content, flags=re.DOTALL)
changed = new_content.count(LANG_TAG)
with open(doc_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print(f"Added lang to {changed} run properties in document.xml")

# ── 2. Write correct settings.xml with autoHyphenation ───────────────────
# Preserve existing namespaces from the original, inject hyphenation in correct order
settings_path = os.path.join(word_dir, 'settings.xml')
with open(settings_path, 'r', encoding='utf-8') as f:
    s = f.read()

if 'autoHyphenation' in s:
    print("autoHyphenation already present in settings.xml")
else:
    # Insert before <w:evenAndOddHeaders (correct OOXML order: after displayBackgroundShape)
    # or if not found, before </w:settings>
    inject = '  <w:autoHyphenation w:val="1"/>\n  <w:consecutiveHyphenLimit w:val="2"/>\n  <w:hyphenationZone w:val="360"/>\n'
    if '<w:evenAndOddHeaders' in s:
        new_s = s.replace('<w:evenAndOddHeaders', inject + '  <w:evenAndOddHeaders', 1)
    elif '<w:compat>' in s:
        new_s = s.replace('<w:compat>', inject + '  <w:compat>', 1)
    else:
        new_s = s.replace('</w:settings>', inject + '</w:settings>')
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(new_s)
    print("Enabled autoHyphenation in settings.xml")
