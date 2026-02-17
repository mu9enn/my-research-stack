# Deep Paper Screening Prompt Template

## Name
深度研究版论文结构分析 Prompt

Deep Structural Paper Analysis Prompt

## Description
面向复现、扩展或方法学批评，对论文进行精确、技术性的反向工程与风险评估，找出可攻击点与研究机会。

Reverse-engineering oriented prompt for reproduction, critique, and extension. Produces precise, technical breakdown of assumptions, components, failure modes, and research opportunities.

## Prompt

```text
你正在对一篇论文进行深度结构化分析，目标是复现、扩展或进行方法论批评。

附带的 PDF 是整篇论文。

你的任务不是总结。
你的任务是对论文进行反向工程式解析。

保持精确、分析性和技术性。
避免背景性解释、复述摘要或泛泛评论。

严格按照以下结构输出。

==================================================
[1] FORMAL PROBLEM FORMULATION

• 若有，给出明确的数学/目标函数表述
• 精确说明优化或求解的对象
• 可控变量与固定变量分别有哪些
• 问题是否良定？为什么或为什么不？
• 该表述成立需要哪些假设？

==================================================
[2] EXPLICIT & IMPLICIT ASSUMPTIONS

将假设分为：

A. 明确给出的假设
B. 隐含但未讨论的假设

对每个假设说明：
• 为何需要
• 违反时会发生什么

==================================================
[3] METHOD DECOMPOSITION

将方法拆解为最小功能组件。

对于每个组件：
• 功能是什么
• 移除后会破坏什么
• 是必需还是辅助
• 是否存在更简单的替代

然后回答：
• 哪部分最可能贡献性能提升？
• 哪部分最脆弱？

==================================================
[4] REPRODUCIBILITY RISK ANALYSIS

• 缺失的实现细节
• 对超参的敏感度
• 对数据集特性的依赖
• 计算依赖（规模、硬件）
• 复现结果的风险因素

评估复现难度（1–5）。

==================================================
[5] FAILURE MODE ANALYSIS

• 理论上的失效条件
• 经验上的失效场景
• 分布转移脆弱性
• 过拟合风险
• 隐藏的不稳定来源

论文是否有意义地讨论这些失败？

==================================================
[6] EVALUATION STRESS TEST

• 基线实现是否公平？
• 消融实验是否充分？
• 比较是否 apples-to-apples？
• 指标是否与问题对齐？
• 缺失但关键的实验是什么？

如果需要设计一个额外实验来挑战论文，你会设计什么？

==================================================
[7] IMPROVEMENT PATHWAYS

识别：

• 参数层面的改进
• 架构层面的改进
• 目标函数层面的重构
• 问题重定义的机会
• 可扩展性扩展
• 鲁棒性扩展

按可行性对改进排序（短期 / 中期 / 长期）。

==================================================
[8] THEORETICAL & CONCEPTUAL LIMIT

• 剩余的理论性空白是什么？
• 方法是否在概念上可泛化？
• 是否在解决代理问题？
• 收益是基础性的还是数据集专属？

==================================================
[9] RESEARCH OPPORTUNITY EXTRACTION

基于结构性弱点：

生成：
• 3 个可扩展该工作的研究问题
• 2 个挑战该工作的研究问题
• 1 个完全重构问题定义的研究问题

==================================================

严格输出规则：
- 每个子部分最多 4 个要点。
- 不要总结。
- 不要重复。
- 高信号密度。
- 仅使用分析性语气。
```

```text
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
```

## Use Cases

复现准备：重点查看 `REPRODUCIBILITY RISK ANALYSIS` 与 `METHOD DECOMPOSITION`。

Reproduction / extension / rebuttal preparation: focus on `REPRODUCIBILITY RISK ANALYSIS` and `METHOD DECOMPOSITION`.
