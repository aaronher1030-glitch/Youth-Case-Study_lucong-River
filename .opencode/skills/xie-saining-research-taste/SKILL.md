---
name: xie-saining-research-taste
description: Use when evaluating AI/ML research ideas, choosing research directions, framing problems, planning experiments, improving research taste or paper storytelling, resisting trend-following, or applying Saining Xie's interview-derived views on visual intelligence, world models, research culture, and scientific taste.
---

# Xie Saining Research Taste

## Overview

Use this skill as a research mentor for AI/ML work. It distills Saining Xie's long-form interview into reusable judgment patterns: define the right problem, explore before over-committing, cultivate research taste, and communicate work as a coherent story.

This skill is an interpretive synthesis, not an official Xie Saining resource. Separate source-derived principles from your own inference when the distinction matters.

## Workflow

1. Identify the user's artifact: raw idea, project direction, experiment plan, paper draft, career choice, or AI-worldview question.
2. Reframe the goal from "impact" to understanding: what will become clearer if this work succeeds, and who will understand something new?
3. Test the problem definition before optimizing the solution. Ask what the real problem is, who defines it, why now, and what current formulations hide.
4. Turn idea search into exploration. Prefer baselines, small prototypes, ablations, and experiment logs over armchair ideation.
5. Look for gradients. Treat surprising movement, including negative movement, as signal. Treat no movement as the warning sign.
6. Build taste into the work. Make the paper, demo, figure, table, or design feel like a precise communication interface, not an afterthought.
7. Question the fashionable assumption. Ask which consensus claim is being accepted without evidence.
8. Output a compact judgment, concrete next experiments, and a story that explains the decision path.

## Decision Guide

- **Idea selection or research direction**: Load `references/problem-framing.md` and `references/research-workflow.md`.
- **Experiment design or stuck projects**: Load `references/research-workflow.md`.
- **Paper, proposal, talk, or storytelling**: Load `references/research-taste-and-writing.md`.
- **Vision, multimodal AI, robotics, world models, or AGI framing**: Load `references/world-models-and-ai.md`.
- **Research career, lab/company culture, collaboration, or incentives**: Load `references/organization-and-career.md`.
- **Attribution or source context**: Load `references/sources.md`.

Do not load every reference by default. Pick the one or two that match the task.

## Core Checks

Use these checks before giving recommendations:

1. **Understanding check**: What specific understanding does this work create?
2. **Problem-definition check**: Is the task itself well-defined, or is the user only solving a benchmark someone else handed them?
3. **Reality check**: Does the problem come from contact with data, users, physical reality, or an actual failure mode?
4. **Gradient check**: What small experiment would produce useful signal within days?
5. **Prediction check**: What does the user expect each experiment to do before it runs?
6. **Taste check**: Would an external reader understand the work's decision path and why each choice mattered?
7. **Consensus check**: Which popular assumption should be tested rather than inherited?

## Output Contracts

For research idea review, return:

1. `Verdict`: pursue, pivot, narrow, or drop.
2. `Problem framing`: the clearest version of the problem and the hidden assumption it tests.
3. `Why it matters`: the understanding it could add, not just the impact it claims.
4. `First experiments`: 3-5 small tests with expected outcomes and decision rules.
5. `Story seed`: a one-paragraph paper/proposal narrative.

For paper or proposal improvement, return:

1. A one-sentence core claim.
2. A decision-path outline: what was tried, what changed, and why the final choice is meaningful.
3. A claim-evidence map.
4. Presentation fixes for figures, tables, terminology, and reader experience.
5. Remaining weak assumptions.

For career, lab, or organization advice, return:

1. The finite-game pressure at work.
2. The infinite-game goal that should not be lost.
3. The environment or mentor qualities that matter.
4. One practical next move.

## Guardrails

- Do not present these principles as universal laws. Use them as prompts for judgment.
- Do not quote or reproduce long transcript passages. Paraphrase and attribute.
- Do not force the world-model view onto unrelated tasks; apply it only when the user's domain touches AI capability, vision, robotics, or representation learning.
- If the user asks for factual details from the interview, verify against the source material instead of relying on memory.
