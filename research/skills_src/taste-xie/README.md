<div align="center">

# Xie Saining Research Taste

**An AI-agent skill for sharper research taste, better problem framing, and more thoughtful AI/ML work.**

[中文说明](README_zh.md) · [Skill](xie-saining-research-taste/SKILL.md) · [Sources](xie-saining-research-taste/references/sources.md)

![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827?style=for-the-badge)
![AI Research](https://img.shields.io/badge/AI%20Research-Taste%20%26%20Judgment-2563eb?style=for-the-badge)
![MIT License](https://img.shields.io/badge/License-MIT-16a34a?style=for-the-badge)

</div>

---

> Research is not only about doing more experiments. It is about defining the right problem, noticing the right signal, and making the work understandable to others.

This repository packages ideas from Saining Xie's long-form interview with Zhang Xiaojun into a reusable skill for Codex, Claude Code, Gemini, and other agent systems. It is designed for researchers, builders, and students who want an AI assistant that can critique research directions with taste instead of only producing generic suggestions.

## Why Star This

Most AI research advice sounds like this:

- "run more ablations"
- "improve the story"
- "find a stronger contribution"
- "follow the latest trend"

This skill turns those vague instructions into a concrete review workflow:

| Research pressure | What the skill asks instead |
| --- | --- |
| Is this idea hot enough? | What understanding does it create? |
| Can we beat the benchmark? | Is this the right problem definition? |
| Which experiment next? | What small test will produce real signal? |
| How do we write the paper? | Can readers reconstruct the decision path? |
| Should we follow the trend? | Which fashionable assumption should be tested? |

## What It Helps With

- Evaluate whether an AI/ML research idea is worth pursuing
- Reframe a vague direction into a sharper research problem
- Design fast experiments that produce useful signal
- Improve paper, proposal, and talk narratives
- Think through visual intelligence, world models, robotics, and LLM-centric assumptions
- Reflect on research culture, mentors, collaboration, and credit assignment

## Quick Start

Clone the repo:

```bash
git clone https://github.com/ky-ji/xie-saining-research-taste-skills.git
cd xie-saining-research-taste-skills
```

Install for Codex:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R xie-saining-research-taste "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Install for Claude Code:

```bash
mkdir -p "$HOME/.claude/skills"
cp -R xie-saining-research-taste "$HOME/.claude/skills/"
```

Install for Gemini:

```bash
mkdir -p "$HOME/.gemini/skills"
cp -R xie-saining-research-taste "$HOME/.gemini/skills/"
```

## Try These Prompts

```text
Use $xie-saining-research-taste to evaluate this research idea and tell me whether to pursue, narrow, pivot, or drop it.
```

```text
Use $xie-saining-research-taste to turn this vague AI direction into a concrete problem definition and a 2-week experiment plan.
```

```text
Use $xie-saining-research-taste to review my paper introduction for research taste, story, and claim-evidence alignment.
```

```text
Use $xie-saining-research-taste to critique this LLM-centric project from a visual intelligence and world-model perspective.
```

## The 7 Checks

The skill centers research review around seven questions:

1. **Understanding**: What specific understanding does this work create?
2. **Problem definition**: Is the task itself right, or just inherited?
3. **Reality contact**: Does the idea touch data, users, physics, or real failure modes?
4. **Gradient**: What small experiment gives useful signal within days?
5. **Prediction**: What do we expect before running the experiment?
6. **Taste**: Can an external reader follow the decision path?
7. **Consensus**: Which popular assumption should be tested rather than inherited?

## What's Inside

```text
xie-saining-research-taste/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── problem-framing.md
    ├── research-workflow.md
    ├── research-taste-and-writing.md
    ├── world-models-and-ai.md
    ├── organization-and-career.md
    └── sources.md
```

Reference guide:

| File | Use it for |
| --- | --- |
| `problem-framing.md` | idea selection, problem definition, infinite-game lens |
| `research-workflow.md` | experiments, probes, negative signal, pivots |
| `research-taste-and-writing.md` | paper story, figures, naming, communication polish |
| `world-models-and-ai.md` | visual intelligence, robotics, world models, AGI humility |
| `organization-and-career.md` | mentors, culture, credit assignment, research incentives |
| `sources.md` | attribution and source context |

## Example Output Shape

When reviewing a research idea, the skill asks the agent to return:

```text
Verdict: pursue / narrow / pivot / drop
Problem framing: the clearest version of the problem
Why it matters: the understanding it could add
First experiments: 3-5 small tests with predictions and decision rules
Story seed: a one-paragraph paper or proposal narrative
```

That output contract is the point: the skill pushes the agent to make a judgment, propose experiments, and explain the story rather than leaving you with a soft list of suggestions.

## Inspiration And Attribution

This is an unofficial, paraphrased synthesis of public materials around Saining Xie's 2026 long-form interview with Zhang Xiaojun. It is not endorsed by Saining Xie, Zhang Xiaojun, AMI Labs, NYU, YouTube, Podwise, Podecho, or NoStandUpTalk.

Main sources:

- Original interview: <https://www.youtube.com/watch?v=rIwgZWzUKm8>
- Podwise episode summary and outline: <https://podwise.ai/dashboard/episodes/7527167>
- Podecho AI-translated transcript: <https://echo.liujiacai.net/2026-03-16-saining-xie-world-models-ami-labs-yann-lecun-fei-fei-li-and-42/transcript>
- NoStandUpTalk eight-theme note: <https://nostanduptalk.github.io/notes-xie-saining-research-taste-ai/>
- Packaging reference: <https://github.com/Master-cai/Research-Paper-Writing-Skills>

The maintainer's contribution is selection, structuring, and adaptation into a reusable AI-agent skill.

## License

MIT License. See [LICENSE](LICENSE).
