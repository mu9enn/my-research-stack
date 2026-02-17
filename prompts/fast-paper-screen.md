# Fast Paper Screening Prompt Template

## Name
高效率论文自动分析 Prompt 模板

High-Density Paper Structural Analysis Prompt

## Description
在 10–15 分钟内完成论文的“研究定位 + 价值判断”，输出结构化、高密度信息，避免无效摘要与冗余背景。

10–15 minute structural analysis to decide paper positioning and research value. Produces dense, decision-oriented output and avoids generic summaries.

## Prompt

```text
你现在将执行一篇论文的高密度结构化分析。

附带的 PDF 是整篇论文。

你的任务不是总结论文。
你的任务是提取对研究决策有用的结构性信息。

避免：
- 复述摘要
- 通用性总结
- 夸张或评价性语言
- 重复显而易见的背景
- 冗长解释

简洁、密集、分析性强。

输出必须严格遵循下面的结构。

--------------------------------------------------
[1] PROBLEM STRUCTURE

• 一句概述性的问题领域
• 核心研究问题（精确）
• 问题类型（方法学类别，而非应用领域）
• 该问题结构性存在的原因
• 假设强度（strong / medium / weak，并简述原因）

--------------------------------------------------
[2] METHOD ARCHITECTURE

• 方法范式（optimization / generative / theoretical / benchmark / framework / hybrid）
• 核心机制（抽象层面，不要实现细节）
• 与先前工作的结构性差异
• 依赖约束（数据 / 环境 / 监督 / 规模 / 计算）
• 若缩减规模，方法是否仍然成立？

--------------------------------------------------
[3] INNOVATION DENSITY

• 是增量创新还是结构性创新？
• 新颖性是概念性还是工程驱动？
• 它是在重新定义问题还是仅仅提升性能？
• 创新强度（1–5）

--------------------------------------------------
[4] EVALUATION ROBUSTNESS

• 实验是否足以验证主张？
• 可能的评估盲点
• 指标幻觉风险
• 是否包含失败案例分析？
• 在真实世界中可能在哪些地方失效？

--------------------------------------------------
[5] TRANSFERABILITY

• 可迁移的思想（抽象原则）
• 可迁移的机制（技术手段）
• 不可迁移的部分
• 该思想可能泛化到的领域

--------------------------------------------------
[6] STRATEGIC VALUE

• 长期研究价值（1–5）
• 有用方向：
  - 问题启发
  - 方法启发
  - 评估启发
  - 仅需了解文献
  - 低优先级
• 是否值得深入研读？（yes / selective / no）
• 若为选择性研读，哪些部分值得读？

--------------------------------------------------
[7] CRITICAL QUESTIONS

列出 3–5 个严肃研究者在读完该论文后应提出的关键问题。

--------------------------------------------------

严格输出规则：
- 每个子部分最多 4 个要点。
- 不要复述摘要。
- 不要冗余解释。
- 不要填充句子。
- 高信号输出。
```

```text
You are performing high-density research paper structural analysis.

The PDF attached is a full research paper.

Your task is NOT to summarize the paper.
Your task is to extract only structurally useful information for research decision-making.

Avoid:
- rewriting the abstract
- generic summaries
- praising language
- repeating obvious background
- long explanations

Be concise, dense, analytical.

Output must follow the exact structure below.

--------------------------------------------------
[1] PROBLEM STRUCTURE

• One-sentence Problem Domain
• Core Research Question (precise)
• Problem Type (methodological category, not application area)
• Why this problem structurally exists
• Level of assumptions (strong / medium / weak + short reason)

--------------------------------------------------
[2] METHOD ARCHITECTURE

• Method Paradigm (optimization / generative / theoretical / benchmark / framework / hybrid)
• Core Mechanism (abstract level, not implementation detail)
• What makes it different from prior work (structural difference)
• Dependency constraints (data / environment / supervision / scale / compute)
• If scale is reduced, does the method still stand?

--------------------------------------------------
[3] INNOVATION DENSITY

• Is this incremental or structural innovation?
• Is the novelty conceptual or engineering-driven?
• Does it redefine the problem or only improve performance?
• Innovation strength (1–5)

--------------------------------------------------
[4] EVALUATION ROBUSTNESS

• Are experiments sufficient to validate claims?
• Possible evaluation blind spots
• Risk of metric illusion
• Does it include failure case analysis?
• Where might it break in real-world settings?

--------------------------------------------------
[5] TRANSFERABILITY

• Transferable idea (abstract principle)
• Transferable mechanism (technical)
• Non-transferable parts
• Fields where the idea could generalize

--------------------------------------------------
[6] STRATEGIC VALUE

• Long-term research value (1–5)
• Useful for:
  - problem inspiration
  - method inspiration
  - evaluation inspiration
  - literature awareness only
  - low priority
• Should this be deeply read? (yes / selective / no)
• If selective, which section is worth reading?

--------------------------------------------------
[7] CRITICAL QUESTIONS

List 3–5 critical questions a serious researcher should ask after reading this paper.

--------------------------------------------------

Strict output rules:
- Maximum 4 bullet points per subsection.
- No abstract rewriting.
- No redundant explanations.
- No filler sentences.
- High signal only.
```

## Use Cases

快速筛论文（大量论文的初筛）

Quick triage of many papers
