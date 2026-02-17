# Deep Structural Paper Analysis Prompt

## Name
深度研究版论文结构分析 Prompt

Deep Structural Paper Analysis Prompt

## Description
面向复现、扩展或方法学批评，对论文进行精确、技术性的反向工程与风险评估，找出可攻击点与研究机会。

Reverse-engineering oriented prompt for reproduction, critique, and extension. Produces precise, technical breakdown of assumptions, components, failure modes, and research opportunities.

## Prompt

中文：

You are conducting deep structural analysis of a research paper for potential reproduction, extension, or methodological critique.

The attached PDF is the full paper.

Your task is NOT to summarize.
Your task is to reverse-engineer the paper.

Be precise, analytical, and technical.
Avoid background explanation.
Avoid abstract rewriting.
Avoid generic commentary.

Follow the structure exactly.

==================================================
[1] FORMAL PROBLEM FORMULATION

• Explicit mathematical/objective formulation (if provided)
• What exactly is being optimized or solved?
• What variables are controllable vs fixed?
• Is the problem well-posed? Why or why not?
• What assumptions are necessary for the formulation to hold?

==================================================
[2] EXPLICIT & IMPLICIT ASSUMPTIONS

Separate into:

A. Explicit assumptions (clearly stated)
B. Implicit assumptions (required but not discussed)

For each assumption:
• Why it is required
• What happens if it is violated

==================================================
[3] METHOD DECOMPOSITION

Decompose the method into minimal functional components.

For each component:
• Its purpose
• What would break if removed?
• Is it essential or auxiliary?
• Could a simpler substitute exist?

Then answer:
• Which part likely contributes most to performance?
• Which part is most fragile?

==================================================
[4] REPRODUCIBILITY RISK ANALYSIS

• Missing implementation details
• Sensitivity to hyperparameters
• Dependence on dataset characteristics
• Compute dependency (scale, hardware)
• Risk factors in reproducing reported results

Estimate reproducibility difficulty (1–5).

==================================================
[5] FAILURE MODE ANALYSIS

• Theoretical failure conditions
• Empirical failure scenarios
• Distribution shift vulnerability
• Overfitting risks
• Hidden instability sources

Does the paper meaningfully address these failures?

==================================================
[6] EVALUATION STRESS TEST

• Are baselines fairly implemented?
• Are ablations sufficient?
• Are comparisons apples-to-apples?
• Metric robustness (does metric align with problem?)
• What experiment is missing but critical?

If you had to design one additional experiment to challenge the paper, what would it be?

==================================================
[7] IMPROVEMENT PATHWAYS

Identify:

• Parameter-level improvement
• Architectural-level improvement
• Objective-level reformulation
• Problem-redefinition opportunity
• Scalability extension
• Robustness extension

Rank improvement feasibility (short-term / medium-term / long-term research).

==================================================
[8] THEORETICAL & CONCEPTUAL LIMIT

• What theoretical gap remains?
• Does the method generalize conceptually?
• Is it solving a proxy problem?
• Is the gain fundamental or dataset-specific?

==================================================
[9] RESEARCH OPPORTUNITY EXTRACTION

Based on structural weaknesses:

Generate:
• 3 research questions that extend this work
• 2 research questions that challenge this work
• 1 research question that reframes the problem entirely

==================================================

Strict Output Rules:
- Maximum 4 bullet points per subsection.
- No summarizing.
- No repetition.
- High signal density.
- Analytical tone only.

## Use Cases

场景：
- 复现准备：重点查看 `REPRODUCIBILITY RISK ANALYSIS` 与 `METHOD DECOMPOSITION`。
- 改进/扩展：优先 `IMPROVEMENT PATHWAYS` 与 `RESEARCH OPPORTUNITY EXTRACTION`。
- 写 rebuttal：关注 `EVALUATION STRESS TEST` 与 `FAILURE MODE ANALYSIS`。

Use cases:
- Reproduction preparation
- Method improvement / extension
- Rebuttal and critique
