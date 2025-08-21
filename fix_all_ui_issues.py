#!/usr/bin/env python3
"""
fix_all_ui_issues.py

Correction systématique post-audit pour l'UI CHNeoWave.

Fonctions:
- Charge le fichier d'audit JSON généré (src/ui/audit_ui_exhaustif.json)
- Remplace tous les emojis par des libellés professionnels
- Standardise les dimensions (resize, setFixedWidth, margins, spacing, QFont, CSS font-size/padding)
- Crée un backup .backup de chaque fichier modifié
- Génère un rapport corrections_applied.json à la racine

Usage:
    python fix_all_ui_issues.py --execute
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path
from typing import Callable, Dict, List, Tuple


REPO_ROOT = Path(__file__).resolve().parent


def load_audit() -> dict:
    """Charge l'audit depuis l'un des emplacements connus."""
    candidates = [
        REPO_ROOT / "src/ui/audit_ui_exhaustif.json",
        REPO_ROOT / "audit_ui_exhaustif.json",
    ]
    for p in candidates:
        if p.exists():
            with p.open("r", encoding="utf-8") as f:
                return json.load(f)
    raise FileNotFoundError("audit_ui_exhaustif.json introuvable (essayé src/ui/ et racine)")


def build_emoji_mapping() -> Dict[str, str]:
    """Mapping professionnel pour les principaux emojis rencontrés.

    Note: On privilégie des libellés neutres/professionnels.
    """
    mapping = {
        # Navigation / Modules
        "🧭": "Navigation",
        "📋": "",
        "⚙️": "Options",
        "⚙": "Options",
        "📊": "Acquisition",
        "📈": "Statistique",
        "🔬": "Analyses",
        "📤": "Export",
        # Status / Indicateurs
        "🔴": "●",
        "✅": "✓",
        "🔶": "◆",
        "🟢": "✓",
        "🟡": "●",
        "🔵": "●",
        # Actions
        "🚀": "Démarrer",
        "⏹️": "Arrêter",
        "⏹": "Arrêter",
        "⏸️": "Pause",
        "⏸": "Pause",
        "🔄": "Actualiser",
        "💾": "Sauvegarder",
        "🗑️": "Supprimer",
        "🗑": "Supprimer",
        # Interface / Informations
        "🌊": "CHNeoWave",
        "🎯": "Objectif",
        "📁": "Projet",
        "📂": "Projet",
        "🕐": "Heure",
        "👨‍💼": "Ingénieur",
        "👤": "Profil",
        "🔖": "Code",
        "ℹ️": "Informations",
        "ℹ": "Informations",
        "🧪": "Tests",
        "🏗️": "Architecture",
        "🏗": "Architecture",
        "🎉": "",
        "✨": "",
        "⚡": "",
        "💡": "Système",
        "❌": "Erreur",
        "❓": "Aide",
        "📥": "Importer",
        "📖": "Documentation",
        "📚": "Documentation",
        "🚪": "Quitter",
        "🔗": "Lien",
        "🏷️": "Étiquette",
        "🏷": "Étiquette",
        "🔧": "Options",
        "👤": "Profil",
        "📝": "Activité",
        # Variations selector seul (souvent capté dans l'audit)
        "️": "",
    }
    return mapping


def apply_emoji_mapping(content: str, mapping: Dict[str, str]) -> Tuple[str, int]:
    replaced = 0
    for emoji, replacement in mapping.items():
        if emoji in content:
            count = content.count(emoji)
            content = content.replace(emoji, replacement)
            replaced += count
    return content, replaced


def clamp(val: int, max_val: int) -> int:
    return val if val <= max_val else max_val


def replace_resize(match: re.Match) -> str:
    w = int(match.group(1))
    h = int(match.group(2))
    # Standard: clamp à 1280x800
    return f"resize({clamp(w, 1280)}, {clamp(h, 800)})"


def replace_set_fixed_width(match: re.Match) -> str:
    w = int(match.group(1))
    # Standard: si > 300 → 240
    if w > 300:
        return "setFixedWidth(240)"
    return match.group(0)


def replace_set_min_height(match: re.Match) -> str:
    h = int(match.group(1))
    # Standard boutons : >50→36, >40→30
    if h > 50:
        return "setMinimumHeight(36)"
    if h > 40:
        return "setMinimumHeight(30)"
    return match.group(0)


def replace_set_fixed_height(match: re.Match) -> str:
    h = int(match.group(1))
    if h > 50:
        return "setFixedHeight(36)"
    if h > 40:
        return "setFixedHeight(30)"
    return match.group(0)


def replace_set_margins(match: re.Match) -> str:
    a = int(match.group(1))
    b = int(match.group(2))
    c = int(match.group(3))
    d = int(match.group(4))
    # Standard: si l'un > 20 → (8,8,8,8)
    if any(x > 20 for x in (a, b, c, d)):
        return "setContentsMargins(8, 8, 8, 8)"
    return match.group(0)


def replace_set_spacing(match: re.Match) -> str:
    s = int(match.group(1))
    # Standard: >25→12, sinon >15→6
    if s > 25:
        return "setSpacing(12)"
    if s > 15:
        return "setSpacing(6)"
    return match.group(0)


def replace_qfont(match: re.Match) -> str:
    # QFont("Segoe UI", 24, ...)
    size = int(match.group(1))
    new_size = size
    if size > 24:
        new_size = 18
    elif size > 16:
        new_size = 15
    elif size > 14:
        new_size = 14
    return match.group(0).replace(str(size), str(new_size), 1)


def replace_css_font_size(match: re.Match) -> str:
    size = int(match.group(1))
    new_size = size
    if size > 16:
        new_size = 14
    elif size > 14:
        new_size = 13
    return f"font-size: {new_size}px;"


def replace_css_padding_single(match: re.Match) -> str:
    pad = int(match.group(1))
    # Si padding unique trop grand, réduire à 8
    if pad > 16:
        return "padding: 8px;"
    return match.group(0)


def replace_css_padding_dual(match: re.Match) -> str:
    a = int(match.group(1))
    b = int(match.group(2))
    if a > 12 or b > 24:
        return "padding: 8px 16px;"
    return match.group(0)


def standardize_dimensions(content: str) -> Tuple[str, int]:
    patterns: List[Tuple[re.Pattern[str], Callable[[re.Match], str]]] = [
        (re.compile(r"resize\(\s*(\d+)\s*,\s*(\d+)\s*\)"), replace_resize),
        (re.compile(r"setFixedWidth\(\s*(\d+)\s*\)"), replace_set_fixed_width),
        (re.compile(r"setMinimumHeight\(\s*(\d+)\s*\)"), replace_set_min_height),
        (re.compile(r"setFixedHeight\(\s*(\d+)\s*\)"), replace_set_fixed_height),
        (re.compile(r"setContentsMargins\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)"), replace_set_margins),
        (re.compile(r"setSpacing\(\s*(\d+)\s*\)"), replace_set_spacing),
        (re.compile(r"QFont\(\s*[^,]+,\s*(\d+)"), replace_qfont),
        (re.compile(r"font-size:\s*(\d+)px;"), replace_css_font_size),
        (re.compile(r"padding:\s*(\d+)px;"), replace_css_padding_single),
        (re.compile(r"padding:\s*(\d+)px\s+(\d+)px;"), replace_css_padding_dual),
    ]

    changes = 0
    for pattern, func in patterns:
        # Compter avant remplacement
        before = len(list(pattern.finditer(content)))
        if before:
            content = pattern.sub(func, content)
            after = len(list(pattern.finditer(content)))
            changes += max(before - after, 0) or before  # approx nombre d'occurrences touchées
    return content, changes


def process_file(path: Path, emoji_mapping: Dict[str, str]) -> Tuple[int, int, bool]:
    """Traite un fichier et retourne (emojis_replaced, dims_fixed, modified)."""
    text = path.read_text(encoding="utf-8")
    original = text

    # Emojis
    text, ecount = apply_emoji_mapping(text, emoji_mapping)

    # Dimensions
    text, dcount = standardize_dimensions(text)

    modified = text != original
    if modified:
        backup = path.with_suffix(path.suffix + ".backup")
        shutil.copy2(path, backup)
        path.write_text(text, encoding="utf-8")
    return ecount, dcount, modified


def main() -> int:
    audit = load_audit()
    emoji_mapping = build_emoji_mapping()

    results: List[Dict[str, object]] = []
    files = [Path(entry["file"]) for entry in audit.get("files_audited", [])]

    processed = 0
    total_emojis = 0
    total_dims = 0

    for fpath in files:
        if not fpath.exists():
            # Essayer de relocaliser dans l'arbre si le chemin absolu diffère
            try_rel = REPO_ROOT / Path("src/ui") / fpath.name
            if try_rel.exists():
                fpath = try_rel
            else:
                continue

        ecount, dcount, modified = process_file(fpath, emoji_mapping)
        processed += 1 if modified else 0
        total_emojis += ecount
        total_dims += dcount
        if modified:
            results.append({
                "file": str(fpath),
                "emojis_replaced": ecount,
                "dimensions_fixed": dcount,
            })

    report_path = REPO_ROOT / "corrections_applied.json"
    report_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Corrections terminées")
    print(f"Fichiers modifiés: {len(results)}")
    print(f"Emojis remplacés (approx): {total_emojis}")
    print(f"Dimensions standardisées (approx): {total_dims}")

    return 0


if __name__ == "__main__":
    if "--execute" in sys.argv:
        raise SystemExit(main())
    print("Usage: python fix_all_ui_issues.py --execute")


