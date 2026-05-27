#!/bin/bash
# Pipeline : generate → unpack → patch → repack → validate → PDF
# Usage (depuis Agentic-writer) :
#   bash skills/print-layout/scripts/build_story.sh <story_base_name> <generator_script.js>
# Usage (depuis le dossier de la skill) :
#   bash scripts/build_story.sh <story_base_name> <generator_script.js>
#
# Variables optionnelles :
#   STORY_WORK_DIR     — répertoire de travail (défaut : <racine NewBooks>/output)
#   DOCX_OFFICE_SCRIPTS — dossier office/ (unpack.py, pack.py, validate.py, soffice.py)
set -e

STORY=$1
SCRIPT=$2

if [[ -z "$STORY" || -z "$SCRIPT" ]]; then
  echo "Usage: bash build_story.sh <story_base_name> <generator_script.js>"
  exit 1
fi

SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPTS_DIR")"
PROJECT_ROOT="$(cd "$SCRIPTS_DIR/../../../.." && pwd)"
WORK_DIR="${STORY_WORK_DIR:-$PROJECT_ROOT/output}"
mkdir -p "$WORK_DIR"

DOCX="$WORK_DIR/${STORY}.docx"
UNPACKED="$WORK_DIR/${STORY}_unpacked"
PDF="$WORK_DIR/${STORY}.pdf"

DOCX_OFFICE="${DOCX_OFFICE_SCRIPTS:-/mnt/skills/public/docx/scripts/office}"
if [[ ! -f "$DOCX_OFFICE/unpack.py" ]]; then
  DOCX_OFFICE="$(cd "$SCRIPTS_DIR/../../_shared/story-build/office" && pwd)"
fi
if [[ ! -f "$DOCX_OFFICE/unpack.py" ]]; then
  echo "Erreur : scripts office introuvables."
  echo "Définir DOCX_OFFICE_SCRIPTS vers le dossier contenant unpack.py, pack.py, validate.py, soffice.py."
  exit 1
fi

export STORY_WORK_DIR="$WORK_DIR"
export STORY_BASE_NAME="$STORY"
if [[ -z "${STORY_MD:-}" && -f "$PROJECT_ROOT/${STORY}.md" ]]; then
  export STORY_MD="$PROJECT_ROOT/${STORY}.md"
fi

echo "── Projet : $PROJECT_ROOT"
echo "── Travail : $WORK_DIR"
echo "── Step 1: Generate docx"
node "$SCRIPT"

echo "── Step 2: Unpack"
rm -rf "$UNPACKED"
python3 "$DOCX_OFFICE/unpack.py" "$DOCX" "$UNPACKED/"

echo "── Step 3a: Language + autoHyphenation"
python3 "$SCRIPTS_DIR/patch_language_hyphen.py" "$UNPACKED/"

echo "── Step 3b: Footer page numbers (LAST)"
python3 "$SCRIPTS_DIR/patch_footers.py" "$UNPACKED/"

echo "── Step 4: Repack"
python3 "$DOCX_OFFICE/pack.py" \
  "$UNPACKED/" "$DOCX" --original "$DOCX"

echo "── Step 5: Validate"
python3 "$DOCX_OFFICE/validate.py" "$DOCX"

echo "── Step 6: Convert to PDF"
python3 "$DOCX_OFFICE/soffice.py" \
  --headless --convert-to pdf "$DOCX" --outdir "$WORK_DIR"

if [[ -d /mnt/user-data/outputs ]]; then
  echo "── Copy to Cursor outputs"
  cp "$DOCX" /mnt/user-data/outputs/
  cp "$PDF"  /mnt/user-data/outputs/
fi

echo "── Cleanup temp files"
rm -rf "$UNPACKED"
rm -f "$WORK_DIR/${STORY}_print.html"

echo "Done → $DOCX + $PDF"
