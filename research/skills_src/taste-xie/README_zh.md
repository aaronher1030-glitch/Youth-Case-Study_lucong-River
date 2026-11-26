<div align="center">

# 谢赛宁研究品味 Skill

**把一次长访谈，整理成 AI/ML 研究者可以反复调用的判断框架。**

[English](README.md) · [Skill 文件](xie-saining-research-taste/SKILL.md) · [来源说明](xie-saining-research-taste/references/sources.md)

![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827?style=for-the-badge)
![Research Taste](https://img.shields.io/badge/Research-Taste%20%26%20Judgment-2563eb?style=for-the-badge)
![MIT License](https://img.shields.io/badge/License-MIT-16a34a?style=for-the-badge)

</div>

---

这不是一份访谈摘要，而是一个可以安装到 Codex、Claude Code、Gemini 等 agent 系统里的 **research taste skill**。

它试图回答一个更实际的问题：

> 如果让 AI agent 学会一点“谢赛宁式”的研究判断，它应该在你拿出一个 idea、实验计划、论文草稿或方向选择时问什么？

## 为什么值得 Star

很多 AI 研究建议听起来都对，但落到行动时很空：

- 多做 ablation
- 把 story 写清楚
- 找一个 stronger contribution
- 追一下最新 trend

这个 skill 把这些模糊建议压成一套可执行检查：

| 常见焦虑 | Skill 会追问 |
| --- | --- |
| 这个方向够不够 hot？ | 它到底带来了什么新的理解？ |
| 能不能刷过 benchmark？ | 这个问题定义本身是对的吗？ |
| 下一步做什么实验？ | 哪个小实验能在几天内产生信号？ |
| 论文怎么写得更强？ | 读者能否复原你的决策路径？ |
| 要不要跟主流趋势？ | 哪个流行假设值得被测试，而不是继承？ |

## 它能帮你做什么

- 判断一个 AI/ML research idea 值不值得做
- 把模糊方向改写成更好的问题定义
- 设计能快速产生信号的小实验
- 改善 paper、proposal、talk 的故事线和研究品味
- 从视觉智能、世界模型、机器人视角反思 LLM-centric 项目
- 分析导师、合作者、研究组织、credit assignment 与职业选择

## 快速安装

克隆仓库：

```bash
git clone https://github.com/ky-ji/xie-saining-research-taste-skills.git
cd xie-saining-research-taste-skills
```

安装到 Codex：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R xie-saining-research-taste "${CODEX_HOME:-$HOME/.codex}/skills/"
```

安装到 Claude Code：

```bash
mkdir -p "$HOME/.claude/skills"
cp -R xie-saining-research-taste "$HOME/.claude/skills/"
```

安装到 Gemini：

```bash
mkdir -p "$HOME/.gemini/skills"
cp -R xie-saining-research-taste "$HOME/.gemini/skills/"
```

## 直接复制这些 Prompt

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

中文也可以这样问：

```text
请使用 $xie-saining-research-taste 帮我判断这个 research idea 是否值得做，并给出第一个两周实验计划。
```

## 核心 7 问

这个 skill 会把研究判断压缩成 7 个问题：

1. **理解**：这个工作会让人们多理解什么？
2. **问题定义**：你在解决真正的问题，还是只是在继承别人的 benchmark？
3. **现实接触**：这个 idea 是否接触了数据、用户、物理世界或真实 failure mode？
4. **梯度**：哪个小实验能在几天内给出有用信号？
5. **预测**：实验前，你预期会看到什么？
6. **品味**：外部读者能否看懂你的决策路径？
7. **共识检验**：哪个流行假设应该被测试，而不是被默认接受？

## 仓库结构

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

每个 reference 对应一个使用场景：

| 文件 | 适合处理 |
| --- | --- |
| `problem-framing.md` | 选题、问题定义、长期主义研究视角 |
| `research-workflow.md` | 实验设计、探索、负信号、pivot |
| `research-taste-and-writing.md` | 论文故事线、图表、命名、表达品味 |
| `world-models-and-ai.md` | 视觉智能、机器人、世界模型、AGI 谦逊 |
| `organization-and-career.md` | 导师、组织文化、credit assignment、研究激励 |
| `sources.md` | 来源、引用、非官方说明 |

## 输出长什么样

当你让它 review 一个 research idea，它会要求 agent 返回：

```text
Verdict: pursue / narrow / pivot / drop
Problem framing: 最清晰的问题定义
Why it matters: 它可能增加什么理解
First experiments: 3-5 个小实验，包含预测和决策规则
Story seed: 一段 paper / proposal 的核心叙事
```

这个输出格式很重要。它会逼 agent 做判断、给实验、讲清楚故事，而不是只给一串温和但没法执行的建议。

## 观点来源

这是一个非官方、转述式整理，不代表谢赛宁、张小珺、AMI Labs、NYU 或任何平台的官方观点。

主要来源：

- 原访谈：<https://www.youtube.com/watch?v=rIwgZWzUKm8>
- Podwise 摘要与时间线：<https://podwise.ai/dashboard/episodes/7527167>
- Podecho AI 翻译逐字稿：<https://echo.liujiacai.net/2026-03-16-saining-xie-world-models-ami-labs-yann-lecun-fei-fei-li-and-42/transcript>
- NoStandUpTalk 八主题笔记：<https://nostanduptalk.github.io/notes-xie-saining-research-taste-ai/>
- 结构参考仓库：<https://github.com/Master-cai/Research-Paper-Writing-Skills>

本仓库的贡献是资料筛选、结构化整理，以及封装为可复用 AI-agent skill。

## License

MIT License，详见 [LICENSE](LICENSE)。
