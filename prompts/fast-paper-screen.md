# Fast Paper Screening Prompt Template

## 名称
高效率论文自动分析 Prompt 模板

## 描述
在 10–15 分钟内完成论文的“研究定位 + 价值判断”，输出结构化、高密度信息，避免无效摘要与冗余背景。

## Prompt 内容
```
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
# Fast Paper Screening Prompt

## Name
高效率论文自动分析 Prompt 模板

Fast / High-Density Paper Structural Analysis Prompt

## Description
在 10–15 分钟内完成论文的“研究定位 + 价值判断”，输出结构化、高密度信息，避免无效摘要与冗余背景。

10–15 minute structural analysis to decide paper positioning and research value. Produces dense, decision-oriented output and avoids generic summaries.

## Prompt

中文：

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

## Use Cases

场景：
- 场景 1（一天扫 5–10 篇）：只看 `Problem Structure`、`Innovation Density`、`Strategic Value`。
- 场景 2（准备精读）：重点看 `Method Architecture`、`Evaluation Robustness`、`Critical Questions`。
- 场景 3（related work）：重点看 `Transferability` 与 `What makes it different from prior work`。

Use cases:
- Quick triage of many papers
- Directional exploration
- Initial related-work collection
