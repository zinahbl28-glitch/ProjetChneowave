#!/usr/bin/env python3
"""
Script d'audit exhaustif interface CHNeoWave
Usage: python audit_ui_complete.py
"""

import os
import re
import json
from pathlib import Path


def audit_complete_ui():
    """Audit exhaustif de tous fichiers UI"""

    # Always resolve from repository root (script directory)
    repo_root = Path(__file__).resolve().parent
    ui_path = repo_root / "src" / "ui"
    results = {
        "files_audited": [],
        "total_emojis_found": 0,
        "total_dimensions_found": 0,
        "issues_by_priority": {"critical": [], "high": [], "medium": []},
    }

    # 1. Découverte de tous fichiers UI
    ui_files = list(ui_path.rglob("*.py"))

    # 2. Patterns de recherche
    emoji_pattern = r"[\U0001F300-\U0001FAD6\U0001F680-\U0001F6FF\u2600-\u27BF\u2190-\u2BFF\uFE0F]"
    dimension_patterns = [
        r"resize\(\s*(\d+)\s*,\s*(\d+)\s*\)",
        r"setFixedWidth\(\s*(\d+)\s*\)",
        r"setFixedHeight\(\s*(\d+)\s*\)",
        r"setMinimumSize\(\s*(\d+)\s*,\s*(\d+)\s*\)",
        r"setMinimumWidth\(\s*(\d+)\s*\)",
        r"setMinimumHeight\(\s*(\d+)\s*\)",
        r"setContentsMargins\(\s*(\d+)",
        r"setSpacing\(\s*(\d+)\s*\)",
        r"font\s*\(.*?(\d+)\)",
        r"QFont\(.*?,\s*(\d+)",
        r"font-size:\s*(\d+)px",
        r"padding:\s*(\d+)px",
    ]

    # 3. Audit fichier par fichier
    for file_path in ui_files:
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            # Fallback encoding
            content = file_path.read_text(errors="ignore")

        lines = content.splitlines()

        file_audit = {
            "file": str(file_path).replace("\\", "/"),
            "emojis": [],
            "dimensions": [],
            "css_issues": [],
        }

        # Recherche emojis
        for i, line in enumerate(lines, 1):
            emojis = re.findall(emoji_pattern, line)
            for emoji in emojis:
                file_audit["emojis"].append({
                    "line": i,
                    "emoji": emoji,
                    "context": line.strip()[:200],
                })

        # Recherche dimensions
        for i, line in enumerate(lines, 1):
            for pattern in dimension_patterns:
                matches = re.findall(pattern, line)
                if matches:
                    file_audit["dimensions"].append({
                        "line": i,
                        "pattern": pattern,
                        "values": matches,
                        "context": line.strip()[:200],
                    })

        if file_audit["emojis"] or file_audit["dimensions"]:
            results["files_audited"].append(file_audit)
            results["total_emojis_found"] += len(file_audit["emojis"]) 
            results["total_dimensions_found"] += len(file_audit["dimensions"]) 

    return results


if __name__ == "__main__":
    audit_results = audit_complete_ui()

    print("AUDIT UI EXHAUSTIF TERMINE")
    print(f"Fichiers analyses: {len(audit_results['files_audited'])}")
    print(f"Emojis trouves: {audit_results['total_emojis_found']}")
    print(f"Dimensions trouvees: {audit_results['total_dimensions_found']}")

    # Sauvegarde rapport JSON
    out_path = Path("audit_ui_exhaustif.json")
    out_path.write_text(json.dumps(audit_results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Rapport sauvegarde: {out_path}")


