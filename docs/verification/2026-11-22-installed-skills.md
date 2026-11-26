# Installed skills — where they came from

Third-party agent skills, downloaded 22 November 2026 and installed under `.opencode/skills/` so OpenCode can load them by ID. None of them are part of the competition entry; they are writing tools.

| Installed ID | Upstream repository | Commit | Licence | What it is for |
|---|---|---|---|---|
| `research-paper-writing` | Master-cai/Research-Paper-Writing-Skills | `77e7c2c` | MIT | Section-by-section rewrite guidance: abstract, introduction, method, experiments, related work, conclusion, plus `paper-review.md` and `does-my-writing-flow-source.md` |
| `evidence-driven-writing` | Norman-bury/research-writing-skill (sub-skill) | `6f79595` | MIT | Forces every background or introduction claim to trace to a citation |
| `peer-review` | Same, sub-skill | `6f79595` | MIT | Pre-submission evaluation checklist, bias detection, self-review template |
| `verification` | Same, sub-skill | `6f79595` | MIT | Prohibits claiming work is finished until a command confirms it |
| `research-taste-distillation` | Jingqi-Xu/research-taste-distillation | `e43d204` | MIT | Builds a research-philosophy profile and uses it to critique an idea |
| `xie-saining-research-taste` | ky-ji/xie-saining-research-taste-skills | `d168cc2` | MIT | Problem framing, "why not simpler", paper storytelling, from an ML researcher's interview |

Full clones are kept in `research/skills_src/` for provenance; the installed copies are the subset listed above. Upstream `LICENSE` files are copied into each installed directory.

## Caveats recorded at install

- These are written for machine-learning papers. Their default output shape is IMRaD, not the kit's eight sections. Use the checklists, not the structures.
- Two are Chinese-first in places; English sections were checked before installing.
- `research-taste-*` skills are about choosing a research problem. This project has already chosen one; the useful part is the critique stance, not the idea-selection workflow.
- To stop a skill being advertised to the model, add `metadata: { opencode/autoinvoke: false }` to its frontmatter, or delete its directory.

## Uninstall

Delete the directory under `.opencode/skills/` and, if you want the disk space back, `research/skills_src/`.
