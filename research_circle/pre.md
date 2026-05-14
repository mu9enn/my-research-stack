下面先把你的需求重新描述清楚，然后给出我刚刚检索到的可用开源项目、官方资料和可借鉴信息。

---

# 1. 你的需求本质是什么

你想搭建的不是一个单纯的“论文写作 Skill”，而是一个更靠前、更科研导向的系统：

> **给定一个研究方向，系统能够自动上网搜索相关文献，阅读和整理已有工作，发现研究空白，提出可能冲 A 会的论文 idea，并进一步规划完整科研流程。**

它和截图里的 **“CS 顶会论文写作全流程 Skill”** 很像，但重点更前置。

截图里的 pipeline 更偏：

```text
Idea → Literature Review → Method → Experiment → Writing → Review → Rebuttal
```

而你的系统当前重点应该是：

```text
Research Direction
→ 自动检索相关文献
→ 构建领域知识图谱/论文地图
→ 找 gap / contradiction / underexplored setting
→ 生成多个 A 会 idea
→ 做 novelty check
→ 评估 feasibility / impact / risk
→ 输出可执行 research plan
```

也就是说，它不是“帮我写论文”，而是：

> **帮我从一个方向中系统性挖出值得做的论文项目。**

---

# 2. 这个系统应该具备的核心能力

我建议把需求拆成 8 个能力模块。

## 2.1 方向理解与任务澄清

输入可能是：

```text
AI agents for scientific discovery
MolBench-VS virtual screening agent
long-horizon tool-use trajectory synthesis
医学 AI foundation model adaptation
```

系统不能直接开始搜索，而要先判断：

```text
这是一个 broad direction？
这是一个具体 idea？
这是一个已有 paper 延展？
这是一个要冲 A 会的新项目？
用户是否已有实验资源、代码、数据集、导师方向约束？
```

这对应你前面提到的“第一性原理”：不要默认用户已经想清楚了。

---

## 2.2 自动文献搜索

系统需要能搜索：

```text
arXiv
Semantic Scholar
OpenAlex
CrossRef
ACL Anthology
Google Scholar 替代源
GitHub / Papers with Code
OpenReview
顶会 accepted papers
```

Claude Code 里可以通过 Skill + MCP + 外部脚本实现。Claude Code 官方文档里明确提到，Skills 适合把重复 checklist、多步骤流程、长程序化说明从 CLAUDE.md 里拆出来，而且 Skill body 只有使用时才加载，比把所有内容塞进 CLAUDE.md 更适合复杂工作流。([Claude API Docs][1])

---

## 2.3 论文阅读与结构化抽取

每篇论文需要抽取：

```text
problem
motivation
method
experiment
dataset
metric
claim
limitation
open question
code availability
possible extension
```

这一步不能只是 summary，要服务于 idea discovery。

---

## 2.4 研究空白发现

系统需要识别：

```text
已有方法没解决的问题
benchmark 缺口
evaluation 缺口
setting gap
methodological gap
domain adaptation gap
tool-use / agent pipeline gap
recent trend 中的未闭环问题
```

这部分可以借鉴 SciPIP、AI-Researcher、Paper Circle 这类项目。

SciPIP 的核心思路就是：用户给定 research background 后，先做 literature review，再生成潜在 paper idea，并结合语义、实体、citation co-occurrence 做多维检索。([GitHub][2])

---

## 2.5 Idea 生成

生成的 idea 不能只是“提出一个想法”，而应该有固定结构：

```text
Title
Core hypothesis
Why now
Related work
Novelty source
Method sketch
Experiment plan
Dataset / benchmark
Expected result
Risk
Fallback plan
A会定位
Potential reviewers' concerns
```

NoviScl/AI-Researcher 很接近这个需求：它的输入是自然语言 research topic，输出是按质量排序的 project proposals，并且每个 proposal 设计得足够详细，学生可以直接按步骤执行。它的 pipeline 包括 related paper search、grounded idea generation、idea deduplication、proposal generation、ranking、filtering。([GitHub][3])

---

## 2.6 Novelty check

这是冲 A 会最关键的部分之一。

系统需要对每个 idea 做：

```text
Semantic Scholar / arXiv / OpenReview 检索
相似论文查找
相同 setting 查找
相同 method 查找
相同 benchmark 查找
负面 novelty 判断
```

AI Scientist 里也有类似设计：生成 idea 后连接 Semantic Scholar API 和 web access 做 novelty filtering，避免 idea 太接近已有工作。([Nature][4])

AI Scientist 的方法部分进一步说明，它会为每个 idea 生成 title、hypothesis、experimental plan，并自评 interestingness、novelty、feasibility，然后最多进行 10 轮 literature search 来做 novelty assessment。([Nature][4])

---

## 2.7 科研计划规划

最终不是输出“可以做这个”，而是输出：

```text
3 天 quick validation plan
2 周 proof-of-concept plan
1 个月 main experiment plan
3 个月 paper plan
需要的数据/代码/模型/算力
实验优先级
最小可行实验
可能失败点
可替代路线
投稿 venue positioning
```

Agent Laboratory 和 OpenAGS 都可以借鉴这类 end-to-end research workflow。Agent Laboratory 将流程分成 Literature Review、Experimentation、Report Writing 三个阶段，并强调人类研究者仍然是 pilot，系统用于自动化文献综述、计划制定、实验执行和报告生成。([GitHub][5])

---

## 2.8 自审与反驳

在 idea 阶段就需要模拟审稿：

```text
Reviewer 1: novelty concern
Reviewer 2: technical depth concern
Reviewer 3: experiment concern
AC: contribution positioning concern
Devil's Advocate: why this is not A会
```

Academic Research Skills 里有 7-agent multi-perspective peer review，包括 EIC、dynamic reviewers、Devil’s Advocate、0–100 rubrics、traceability matrix 等，适合作为这个模块的参考。([GitHub][6])

---

# 3. 官方基础设施资料：搭系统前必须看

## 3.1 Claude Code Skills

Claude Code 官方文档说，Skill 适合在你反复粘贴同一套 instructions、checklist、多步骤流程时使用；当 CLAUDE.md 中某一段已经从“事实说明”膨胀成“流程”时，也应该拆成 Skill。Skill 可以自动触发，也可以通过 `/skill-name` 手动调用。([Claude API Docs][1])

对你的项目来说，应该把系统拆成多个 Skill，而不是一个巨大的 CLAUDE.md：

```text
research-direction-intake
literature-search
literature-review
idea-generation
novelty-check
research-planning
experiment-design
proposal-review
```

---

## 3.2 CLAUDE.md

Claude Code 官方文档强调，CLAUDE.md 是 persistent instructions，但 Claude 会把它当作 context，而不是强制配置；规则越具体、越简洁，遵循越稳定。它适合放 coding standards、workflow、project architecture 等信息。([Claude API Docs][7])

所以你的项目中，CLAUDE.md 应该只放：

```text
项目定位
总行为规则
全局科研诚信底线
目录结构
不同 Skill 的调用边界
输出 artifact 规范
```

不要把全部文献检索流程、审稿流程、写作流程都塞进 CLAUDE.md。

---

## 3.3 Subagents

Claude Code 的 subagent 适合把搜索、日志分析、文件读取这类会污染主上下文的任务隔离出去；每个 subagent 有自己的上下文窗口、工具权限和系统提示。官方文档也指出 subagents 可用于保持上下文干净、限制工具权限、复用配置、控制成本。([Claude API Docs][8])

这对你的系统非常关键。比如：

```text
Literature Search Agent
Novelty Critic Agent
Experiment Planner Agent
Reviewer Agent
GitHub Repo Scout Agent
```

这些都应该是 subagent，而不是让主 Claude 一个人干到底。

---

## 3.4 MCP

Claude Code 官方文档说明，MCP 可以把 Claude Code 连接到外部工具、数据库和 API；一旦连接，Claude 就可以直接读取和操作这些系统，而不是靠你复制粘贴。([Claude API Docs][9])

对你这个系统来说，MCP 很适合接：

```text
Semantic Scholar API
arXiv API
OpenAlex API
CrossRef API
Zotero
本地论文 PDF 库
GitHub search
OpenReview crawler
Papers with Code
```

---

## 3.5 Agent SDK

Claude Agent SDK 可以把 Claude Code 的 agent loop、工具调用、上下文管理能力作为 Python/TypeScript library 使用，用来构建生产级 agent。官方示例里，SDK agent 可以 autonomously read files、run commands、search web、edit code。([Claude API Docs][10])

如果你后续想把这个系统从 Claude Code prompt 变成一个可运行服务，Agent SDK 值得看。

---

# 4. 最相关的开源项目

## 4.1 NoviScl / AI-Researcher

**最接近你“给定方向 → 找 idea → 排序 proposal”的需求。**

它的 pipeline 是：

```text
Related Paper Search
→ Grounded Idea Generation
→ Idea Deduplication
→ Project Proposal Generation
→ Project Proposal Ranking
→ Project Proposal Filtering
```

它的 related paper search 会迭代生成搜索 query，通过 Semantic Scholar API 搜索，再用 LLM 给检索论文打相关性分数并 rerank。idea generation 可以基于 topic 和 retrieved papers 生成 ideas，还可以打开/关闭 RAG。([GitHub][3])

**可借鉴点：**

```text
- topic → ranked project proposals
- 文献 grounding 后再生成 idea
- idea deduplication
- proposal ranking
- proposal filtering
- 每个 proposal 足够详细，能让学生直接执行
```

对你来说，它可以作为 **IdeaAgent + ProposalAgent + RankingAgent** 的主要参考。

---

## 4.2 SciPIP

**适合借鉴“文献检索 + idea proposer”的核心机制。**

SciPIP 是一个 LLM-based Scientific Paper Idea Proposer。用户给 research background 后，它先进行 literature review，再生成新 idea。它强调从语义、实体、citation co-occurrence 多角度检索相关文献，然后用 dual-path idea proposal：一条路径从检索文献中推导 solution，另一条路径靠模型 brainstorming，再平衡 feasibility 和 originality。([GitHub][2])

**可借鉴点：**

```text
- idea 不是凭空生成，而是文献驱动
- 检索不只 keyword，而是 semantic/entity/citation co-occurrence
- idea generation 同时考虑 feasibility 和 originality
- 适合做给定方向的 gap mining
```

---

## 4.3 AI Scientist / AI Scientist-v2

**适合借鉴“全自动科研闭环”的结构，但不建议直接照搬。**

AI Scientist 的工作流包括 idea generation、literature search、experiment planning and implementation、result analysis、manuscript writing、peer review。Nature 文章中也说明，它会生成 idea，做 novelty filtering，然后执行实验、写论文、自动 review。([Nature][4])

AI Scientist-v2 的 ideation step 可以从高层 topic description 生成 structured research ideas，包括 hypotheses、proposed experiments、related work analysis；之后再进入实验 pipeline。([GitHub][11])

**可借鉴点：**

```text
- idea archive
- self-assessed novelty / interestingness / feasibility
- Semantic Scholar novelty check
- experiment journal
- automated reviewer
- tree-search 式实验探索
```

**但要注意：**Nature 文章也指出，目前 AI Scientist 仍不能稳定达到 top-tier 质量；它通过 workshop peer review 的例子不等于稳定达到主会水平，而且系统仍有 hallucination 和过度自信问题。([Nature][4])

所以你的系统更适合定位为：

```text
human-in-the-loop research co-pilot
```

而不是：

```text
fully autonomous paper generator
```

---

## 4.4 PaperQA2

**适合作为“论文阅读和证据问答”的底层组件。**

PaperQA2 定位为 agentic RAG for scientific papers，支持 grounded responses with in-text citations、metadata-aware embeddings、LLM reranking、contextual summarization、iterative query refinement、本地 PDF/text full-text search，并集成 Semantic Scholar、Crossref、Unpaywall 等来源。([GitHub][12])

**可借鉴点：**

```text
- 本地论文库 RAG
- 文献证据引用
- 自动补全 paper metadata
- iterative query refinement
- local PDF full-text search
```

如果你有 Zotero 文库或本地 PDF 库，这类能力非常重要。

---

## 4.5 Paper Circle

**适合借鉴“paper discovery + paper analysis + structured artifacts”。**

Paper Circle 是 2026 年的 open-source multi-agent research discovery and analysis system。它有两个 pipeline：Discovery Pipeline 和 Analysis Pipeline。Discovery Pipeline 结合 offline/online retrieval、多维评分、diversity-aware ranking；Analysis Pipeline 把单篇论文转成 typed knowledge graph，节点包括 concepts、methods、experiments、figures，并支持 graph-aware QA 和 coverage verification。([arXiv][13])

**可借鉴点：**

```text
- 多源论文发现
- 多维评分
- diversity-aware ranking
- 论文知识图谱
- coverage verification
- JSON / CSV / BibTeX / Markdown / HTML 结构化输出
```

这对你做“方向地图”和“idea 证据链”很有价值。

---

## 4.6 Academia MCP

**适合作为 Claude Code 接学术搜索工具的 MCP 参考。**

Academia MCP 是一个 MCP server，提供 scientific papers and datasets 的 search、fetch、analyze、report 工具。功能包括 arXiv search/download、ACL Anthology search、Hugging Face datasets search、Semantic Scholar citations/references、Exa/Brave/Tavily web search、网页 crawler、LaTeX compilation、PDF reading，以及可选的 LLM-powered document QA 和 research proposal workflows。([GitHub][14])

**可借鉴点：**

```text
- 直接作为 MCP 工具接入 Claude Code
- arXiv / ACL / Semantic Scholar / HuggingFace datasets
- PDF reading
- proposal workflow
- LaTeX compilation
```

这个对落地非常有用，因为它解决的是“Claude 怎么真的去查论文和读论文”的问题。

---

## 4.7 lingzhi227 / agent-research-skills

**适合直接参考 Skill 拆分方式。**

这个项目包含 31 个 Claude Code skills，覆盖从 literature search 到 slide generation 的完整 academic research lifecycle。它的 Phase 0 就包括 github-research、deep-research、literature-search、literature-review、idea-generation、novelty-assessment、research-planning。([GitHub][15])

**可借鉴点：**

```text
- 技能拆分粒度
- literature-search 多源检索
- idea-generation 的 Interestingness / Feasibility / Novelty 评分
- novelty-assessment 的 harsh critic 设计
- research-planning 的 task dependency graph
- experiment-design 的 progressive planning
```

这和你要搭的系统高度相关。

---

## 4.8 Imbad0202 / academic-research-skills

**适合借鉴完整科研 pipeline、质量门控、反幻觉机制。**

这个项目包含 Deep Research、Academic Paper、Academic Paper Reviewer、Academic Pipeline。它强调 Semantic Scholar API verification、anti-leakage protocol、VLM figure verification、score trajectory tracking、Material Passport、integrity verification 等。([GitHub][6])

它的 changelog 里还有很多非常值得借鉴的行为设计：anti-sycophancy、intent detection、dialogue health indicator、cross-model verification、style calibration、writing quality check、integrity verification overhaul 等。([GitHub][6])

**可借鉴点：**

```text
- Socratic guided mode
- PRISMA systematic review
- integrity gates
- claim verification
- anti-hallucination
- anti-sycophancy
- Devil’s Advocate reviewer
- Material Passport
- reviewer traceability matrix
```

对你的系统来说，它可以作为 **质量控制层** 的主要参考。

---

## 4.9 OpenAGS

**适合参考完整产品化形态。**

OpenAGS 是一个 open-source framework for fully autonomous scientific research，覆盖 literature review、hypothesis generation、experiments、manuscript writing、peer review，并带有 desktop workspace 和 LaTeX editor。([GitHub][16])

**可借鉴点：**

```text
- UI / workspace 设计
- 多 agent research lifecycle
- research project dashboard
- LaTeX editor integration
- project-based artifact 管理
```

如果你后续想把系统做成一个完整工作台，而不是只做 Claude Code Skill，可以重点看它。

---

## 4.10 Agent Laboratory / AgentRxiv

**适合借鉴“人类是 pilot，agent 做繁重执行”的定位。**

Agent Laboratory 明确说自己不是替代研究者，而是帮助人类研究者实现 idea；它通过 specialized LLM agents 支持 literature review、planning、experiments、report writing。([GitHub][5])

AgentRxiv 基于 Agent Laboratory，进一步让 autonomous research agents 上传、检索、继承彼此的研究；其中包括 PhD、Postdoc、ML Engineer、Professor 等角色，并支持 autonomous mode 和 co-pilot mode。([AgentRxiv][17])

**可借鉴点：**

```text
- PhD / Postdoc / ML Engineer / Professor 角色划分
- co-pilot mode
- autonomous mode
- checkpoint feedback
- research reports + code repo
```

---

## 4.11 Karpathy / autoresearch

**适合借鉴实验闭环，而不是 idea 生成。**

Karpathy 的 autoresearch 思路是：给 agent 一个小但真实的 LLM training setup，让它自动修改代码、训练 5 分钟、检查指标是否提升、保留或丢弃修改，然后重复。仓库里最重要的文件是 `program.md`，它相当于“研究组织的自然语言程序”。([GitHub][18])

**可借鉴点：**

```text
- program.md 作为研究组织规则
- propose → run → evaluate → keep/revert 的闭环
- 固定时间预算
- 单一客观指标
- 自动实验日志
```

这对你后续做 experiment loop 有价值，但不是当前 idea discovery 的核心。

---

## 4.12 PARNESS

**适合借鉴模块化与可验证性设计。**

PARNESS 提出了一些非常适合工程化的原则：pipeline 是 YAML；加 reviewer、换 LLM、插入 novelty filter 不需要改 Python，只需要 YAML edit + module registration；每个 node 独立 subprocess，retry/timeout policy 按节点声明。它还强调多数 autonomous-research systems 没有把 experiment running 和 verification 分开，因此加入 verifier-augmented experiment-runner。([arXiv][19])

**可借鉴点：**

```text
- pipeline as YAML
- module registry
- local failure isolation
- verifier-augmented experiment runner
- typed artifact
- cross-run knowledge accumulation
```

如果你要把系统做得长期可维护，这个很值得看。

---

# 5. 可参考的 Skill / 论文写作资源

## 5.1 Master-cai / Research-Paper-Writing-Skills

这是一个面向 ML/CV/NLP paper writing 的 skill package，支持 Codex、Claude Code、Gemini，内容整理自彭思达老师的公开科研笔记。仓库说明了 Claude Code 下可以全局安装到 `~/.claude/skills`，也可以安装到项目级 `.claude/skills`。([GitHub][20])

**可借鉴点：**

```text
- 顶会论文写作规范
- ML/CV/NLP paper section 写作
- claim-evidence check
- Codex / Claude Code / Gemini 多平台适配
```

---

## 5.2 K-Dense-AI / scientific-agent-skills

它的 literature-review skill 明确用于 systematic literature review、meta-analysis、scoping review、state-of-the-art investigation、research gap identification，并要求 verified citations 和 professional formatting。([GitHub][21])

**可借鉴点：**

```text
- systematic literature review trigger
- research gap identification
- citation verification
- scientific review 输出格式
```

---

## 5.3 Academic Writing Agents / Agent Review Panel

Academic Writing Agents 是一个 Claude Code plugin，把多专家 reviewer 模型带进 academic writing。Agent Review Panel 则是 4–6 个 AI reviewers 独立审查、互相辩论，再由 judge 汇总，输出 Markdown report、process log、HTML dashboard。([GitHub][22])

**可借鉴点：**

```text
- 多 reviewer 独立评估
- adversarial debate
- judge aggregation
- review report artifact
```

---

# 6. Awesome list / 资源入口

## 6.1 Awesome Auto Research Tools

这是一个自动科研工具集合，覆盖 literature review、idea generation、experiment execution、paper writing、peer review。它明确把科研流程拆成：

```text
Literature Review
→ Idea Generation
→ Novelty Check
→ Experiment Design
→ Code Implementation
→ Experiment Execution
→ Result Analysis
→ Paper Writing
→ Peer Review
```

这和你的系统目标非常贴合。([GitHub][23])

---

## 6.2 Awesome Autoresearch

这个列表收集了 autonomous improvement loops、research agents、autoresearch-style systems。其中列出了 OpenAGS、Agent Laboratory、AgentRxiv 等项目。([GitHub][24])

---

## 6.3 Awesome Research Agents / Awesome Scientific Idea Generation

这些列表适合继续追踪近期工作，尤其是 ResearchAgent、SciPIP、AI Scientist、Sparks of Science 等 idea generation 方向。([GitHub][25])

---

# 7. 最值得优先研究的项目排序

如果目标是**尽快搭一个可用的系统**，我建议优先级如下。

## 第一优先级：直接服务你的核心需求

| 优先级 | 项目                                     | 为什么重要                                                                                             |
| --- | -------------------------------------- | ------------------------------------------------------------------------------------------------- |
| 1   | **NoviScl / AI-Researcher**            | 最接近“给定 topic → 搜文献 → 生成 idea → proposal ranking”。                                                 |
| 2   | **SciPIP**                             | 专门做 scientific paper idea proposal，机制适合 idea discovery。                                           |
| 3   | **lingzhi227 / agent-research-skills** | 已经把 literature search、idea generation、novelty assessment、research planning 拆成 Claude Code skills。 |
| 4   | **Academia MCP**                       | 解决 Claude Code 真正接学术搜索、PDF、citation、dataset 的问题。                                                  |
| 5   | **PaperQA2**                           | 适合做本地文献库 RAG 和带 citation 的论文问答。                                                                   |

## 第二优先级：质量控制与系统化

| 优先级 | 项目                                       | 为什么重要                                                     |
| --- | ---------------------------------------- | --------------------------------------------------------- |
| 6   | **Imbad0202 / academic-research-skills** | 质量门控、反幻觉、审稿、自审机制非常丰富。                                     |
| 7   | **Paper Circle**                         | 适合做文献发现、结构化输出、论文知识图谱、coverage verification。               |
| 8   | **PARNESS**                              | 适合借鉴 pipeline-as-YAML、typed artifact、verification runner。 |

## 第三优先级：完整自动科研系统参考

| 优先级 | 项目                                 | 为什么重要                             |
| --- | ---------------------------------- | --------------------------------- |
| 9   | **AI Scientist / AI Scientist-v2** | 完整科研自动化范式，但不建议直接照搬。               |
| 10  | **Agent Laboratory / AgentRxiv**   | 适合借鉴 human-in-loop 和多 agent 角色划分。 |
| 11  | **OpenAGS**                        | 适合参考产品化 UI 和 workspace 设计。        |
| 12  | **Karpathy / autoresearch**        | 适合借鉴实验闭环和 program.md 思想。          |

---

# 8. 对我们项目搭建最有用的信息结晶

基于这些资源，可以结晶出一个比较清晰的系统形态：

```text
CLAUDE.md
  放全局原则、项目边界、artifact 规范、科研诚信底线

.claude/skills/
  research-intake/
  literature-search/
  literature-review/
  idea-generation/
  novelty-check/
  proposal-ranking/
  research-planning/
  reviewer-simulation/

.claude/agents/
  literature-scout.md
  novelty-critic.md
  method-designer.md
  experiment-planner.md
  reviewer-panel.md
  github-repo-scout.md

MCP tools
  Semantic Scholar
  arXiv
  OpenAlex
  CrossRef
  ACL Anthology
  Zotero / local PDF
  GitHub
  OpenReview
```

系统运行时应该像这样：

```text
用户输入研究方向
→ Intake Agent 澄清方向与约束
→ Literature Scout 搜索并整理 30–100 篇相关论文
→ Literature Review Agent 形成领域地图
→ Gap Mining Agent 找空白
→ Idea Agent 生成 10–20 个候选 idea
→ Novelty Critic 做多轮 novelty check
→ Proposal Agent 扩展成完整 proposal
→ Ranking Agent 按 novelty / feasibility / impact / resource fit 排名
→ Reviewer Panel 模拟 A 会审稿
→ Research Planner 输出 2周 / 1月 / 3月执行计划
```

最终输出 artifact 应该包括：

```text
research_brief.md
paper_bank.bib
literature_map.md
gap_analysis.md
ideas.json
novelty_check.md
ranked_proposals.md
reviewer_risks.md
research_plan.md
```

---

# 9. 最重要的判断

你的系统不应该照搬“7-Agent Paper Writing Pipeline”。

它应该是：

> **A-conference idea discovery and research planning pipeline。**

也就是：

```text
不是从 idea 开始写 paper，
而是从 direction 开始生成可信、可验证、可执行、可投稿定位的 idea。
```

最值得组合借鉴的是：

```text
NoviScl / AI-Researcher：topic → proposal ranking
SciPIP：literature-grounded idea proposer
PaperQA2：论文 RAG 与 citation grounding
Academia MCP：Claude Code 学术工具接入
lingzhi227 / agent-research-skills：Claude Code skill 拆分
Imbad0202 / academic-research-skills：质量门控与 anti-hallucination
Paper Circle：文献图谱和 coverage verification
PARNESS：模块化 pipeline 与 typed artifact
```

下一步就可以基于这些资源，开始设计我们自己的 `.claude/skills/research-idea-discovery/SKILL.md` 和配套 agents。

[1]: https://docs.anthropic.com/en/docs/claude-code/slash-commands "Extend Claude with skills - Claude Code Docs"
[2]: https://github.com/cheerss/scipip "GitHub - cheerss/SciPIP: The official repository for the Scientific Paper Idea Proposer (SciPIP) · GitHub"
[3]: https://github.com/NoviScl/AI-Researcher "GitHub - NoviScl/AI-Researcher · GitHub"
[4]: https://www.nature.com/articles/s41586-026-10265-5 "Towards end-to-end automation of AI research | Nature"
[5]: https://github.com/SamuelSchmidgall/AgentLaboratory "GitHub - SamuelSchmidgall/AgentLaboratory: Agent Laboratory is an end-to-end autonomous research workflow meant to assist you as the human researcher toward implementing your research ideas · GitHub"
[6]: https://github.com/Imbad0202/academic-research-skills "GitHub - Imbad0202/academic-research-skills: Academic Research Skills for Claude Code: research → write → review → revise → finalize · GitHub"
[7]: https://docs.anthropic.com/en/docs/claude-code/memory "How Claude remembers your project - Claude Code Docs"
[8]: https://docs.anthropic.com/ja/docs/claude-code/sub-agents "カスタムサブエージェントの作成 - Claude Code Docs"
[9]: https://docs.anthropic.com/en/docs/claude-code/mcp "Connect Claude Code to tools via MCP - Claude Code Docs"
[10]: https://docs.anthropic.com/zh-TW/docs/claude-code/sdk "Agent SDK overview - Claude Code Docs"
[11]: https://github.com/sakanaai/ai-scientist-v2 "GitHub - SakanaAI/AI-Scientist-v2: The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search · GitHub"
[12]: https://github.com/future-house/paper-qa "GitHub - Future-House/paper-qa: High accuracy RAG for answering questions from scientific documents with citations · GitHub"
[13]: https://arxiv.org/html/2604.06170v1 "Paper Circle: An Open-source Multi-agent Research Discovery and Analysis Framework"
[14]: https://github.com/IlyaGusev/academia_mcp "GitHub - IlyaGusev/academia_mcp: Academia MCP server: Tools for automatic scientific research · GitHub"
[15]: https://github.com/lingzhi227/agent-research-skills "GitHub - lingzhi227/agent-research-skills: Skills for Claude Code — deep-research: systematic academic literature review · GitHub"
[16]: https://github.com/openags/Auto-Research "GitHub - openags/auto-research: Auto Research with UI. Autonomous Generalist Scientist / AI Scientist / Agent Scientist / Robot Scientist, across all Scientific Fields. · GitHub"
[17]: https://agentrxiv.github.io/ "AgentRxiv"
[18]: https://github.com/karpathy/autoresearch "GitHub - karpathy/autoresearch: AI agents running research on single-GPU nanochat training automatically · GitHub"
[19]: https://arxiv.org/html/2605.05258v1 "PARNESS: A Paper Harness for End-to-End Automated Scientific Research with Dynamic Workflows, Full-Text Indexing, and Cross-Run Knowledge Accumulation"
[20]: https://github.com/Master-cai/Research-Paper-Writing-Skills "GitHub - Master-cai/Research-Paper-Writing-Skills: Skill package for ML/CV/NLP paper writing, curated and adapted from Prof. Peng Sida's open notes for Codex, Claude Code, and Gemini. · GitHub"
[21]: https://github.com/K-Dense-AI/claude-scientific-skills/blob/main/scientific-skills/literature-review/SKILL.md?plain=1 "scientific-agent-skills/scientific-skills/literature-review/SKILL.md at main · K-Dense-AI/scientific-agent-skills · GitHub"
[22]: https://github.com/andrehuang/academic-writing-agents?utm_source=chatgpt.com "andrehuang/academic-writing-agents: Claude Code plugin"
[23]: https://github.com/handsome-rich/Awesome-Auto-Research-Tools "GitHub - handsome-rich/Awesome-Auto-Research-Tools: A curated collection of automated research tools, covering literature search, paper reading, experiment management, and code generation to help researchers accelerate their workflow. · GitHub"
[24]: https://github.com/alvinreal/awesome-autoresearch "GitHub - alvinreal/awesome-autoresearch: A curated list of autonomous improvement loops, research agents, and autoresearch-style systems inspired by Karpathy's autoresearch. · GitHub"
[25]: https://github.com/chchenhui/awesome-research-agents?utm_source=chatgpt.com "chchenhui/awesome-research-agents"
