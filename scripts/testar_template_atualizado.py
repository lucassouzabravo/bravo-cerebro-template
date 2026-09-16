#!/usr/bin/env python3
"""Recusa um template que perdeu as skills e regras universais da atualização de 16/09/2026."""
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    "skills/comunicacao/comm-coach/SKILL.md": "comm-coach",
    "skills/design/process-visualizer/SKILL.md": "process-visualizer",
    "skills/design/bravo-dark-html/SKILL.md": "bravo-dark-html",
    "skills/comunicacao/bravo-documents/SKILL.md": "bravo-documents",
    "skills/design/fluxo-n8n-miro/SKILL.md": "fluxo-n8n-miro",
    "skills/desenvolvimento/skill-creator/SKILL.md": "skill-creator",
}
ROOT_MARKERS = {
    "AGENTS.md": ["### Prova em todo projeto", "### Delegação e segunda checagem"],
    "SOUL.md": ["Concreto acima de rótulo"],
    "MEMORY.md": ["prova executável"],
    "MAPA.md": ["Prova executável de um projeto"],
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    checks = 0
    for relative, name in SKILLS.items():
        skill = ROOT / relative
        text = skill.read_text(encoding="utf-8")
        require(text.startswith("---\n"), f"frontmatter ausente: {relative}")
        require(f"name: {name}" in text.split("---", 2)[1], f"nome incorreto: {relative}")
        adapter = ROOT / ".claude" / "skills" / name / "SKILL.md"
        require(adapter.is_file(), f"adaptador ausente: {adapter.relative_to(ROOT)}")
        require(f"@../../../{relative.replace(chr(92), '/') }" in adapter.read_text(encoding="utf-8"),
                f"adaptador não aponta para a skill canônica: {name}")
        checks += 3

    for relative, markers in ROOT_MARKERS.items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        for marker in markers:
            require(marker in text, f"regra ausente em {relative}: {marker}")
            checks += 1

    print(f"OK {checks}/0 — skills, adaptadores e regras universais presentes.")


if __name__ == "__main__":
    main()
