# Prompt Packaging Template

## Name
封装提示模板

Prompt Packaging Template

## Description
本模板用于将“实现某一功能的 prompt”标准化封装为项目内可复用的 Markdown 文件，便于团队存档与共享。

This template is used to wrap a "functional prompt" into a standardized Markdown file stored in the project, enabling team reuse and versioning.

## Prompt

```text
（用途：将“实现某一功能的 prompt”包装为本项目 `prompts` 目录下的标准化 Markdown）

输入：一个完整的“实现某一功能的 prompt”（以下简称“功能 prompt”），功能 prompt 通常包含目标、输入/输出、示例与约束。

任务：基于该“功能 prompt”生成并保存一个 Markdown 文件到仓库路径 `my-research-stack/prompts` 下，文件必须严格遵循本模板格式：

- 文件名：请为文件取一个合适的中文名（短且语义明确），并以 `.md` 为后缀，例如 `快速筛论文.md`。
- 文件内容：先写中文块再写英文块（中文在前），包含以下字段顺序：
	1. 顶部标题：英文名（一行）
	2. `## Name`：中文名 以及 英文名（各占一行）
	3. `## Description`：中文描述，随后英文描述
	4. `## Prompt`：用两个代码块分别放中文版本 prompt 与英文版本 prompt（使用 ```text ```），中文版本在前
	5. `## Use Cases`：中文用例段落，随后英文用例段落

格式要求：
- 保持内容精炼；中文与英文内容语义对等。
- 中文 prompt 与英文 prompt 内容应直观可复制粘贴到模型中使用。
- 文件首行保留英文标题（与模板一致）。

输出要求：
- 创建文件并写入完整内容（按仓库相对路径 `prompts/<中文文件名>.md`）。
- 生成完成后，返回一个简短 JSON 格式汇报行（非文件内），包含字段：`file_path`（相对路径）、`file_name`（中文文件名）、`english_name`、`short_run_cmd`（最多一行，说明如何快速用这个 prompt，例如：`cat prompts/<file>.md | pbcopy` 或 `open prompts/<file>.md`）。

自检：在写入后，输出前 8 行文件内容供人工核验。

严格遵守本模板，不要添加多余解释。
```

```text
(Purpose: wrap a "functional prompt" into a standardized Markdown stored under `my-research-stack/prompts`)

Input: a complete functional prompt describing a single functionality (goal, inputs/outputs, examples, constraints).

Task: generate and save a Markdown file under `my-research-stack/prompts` that strictly follows this template:

- Filename: pick a concise Chinese filename that clearly expresses the prompt purpose, with `.md` extension (e.g. `快速筛论文.md`).
- Content order: Chinese block first, then English block, containing:
	1. Top title line: English name
	2. `## Name`: Chinese name then English name (each on its own line)
	3. `## Description`: Chinese description, then English description
	4. `## Prompt`: two code blocks with Chinese prompt first and English prompt second (use ```text ```)
	5. `## Use Cases`: Chinese paragraph then English paragraph

Formatting rules:
- Keep content concise; Chinese and English should be semantically equivalent.
- Both Chinese and English prompts must be ready-to-use (copy/paste into a model).
- Preserve the template's top-line English title.

Output requirements:
- Create the file and write the content at `prompts/<Chinese-filename>.md` relative to the repo root.
- After creation, return a short JSON-like report line (not inside the file) containing: `file_path`, `file_name` (Chinese), `english_name`, and `short_run_cmd` (one-line hint how to view/use the prompt).

Self-check: after writing, print the first 8 lines of the created file for verification.

Strictly follow this template; do not append extra commentary.
```

## Use Cases

中文：用于将即用型 prompt 标准化存档，便于团队复用与版本管理。

English: Archive ready-to-use prompts into the project `prompts` folder in a standardized format for team reuse and versioning.