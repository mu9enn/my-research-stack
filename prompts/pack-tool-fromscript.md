# Pack Tool From Script Prompt

## Name
封装 Python 脚本为团队工具 模板

Pack a Python script into team tool template

## Description
中文描述

将已有的 Python 脚本封装为团队统一的“工具”模板，生成主模块、FastAPI 服务与客户端工具，并产出可复制的验证命令与最小复现实例。

English description

Wrap an existing Python script into the team's standardized "tool" template: produce the main module, a FastAPI API server, and a client ToolManager, plus reproducible verification steps.

## Prompt

```text
你将把一个已有的 Python 脚本封装成我们团队统一的“工具”模板。任务目标、约束、输出目录和验收标准都在下面严格列明，请按步骤完成并自检。

任务概述

深入阅读并理解提供的原始脚本（完整源码），为它选择一个合适的短名 【tool_name】（英式小写且用下划线分词，例如 fix_pdb、gmx_prepare_complex），该名字应能清楚表达脚本功能。
在仓库中创建路径： /root/lwj/wll/code/DrugAgentTools/sxy_local/tool_src/【tool_name】/as_tool，并在 .../tool_src/【tool_name】 放置 readme.md。
在 .../as_tool 下创建并实现三个文件，接口需与现有示例（example、ref）风格一致：
fix 模块：fix_... 或 prepare_... 的核心模块，例如 fix_pdb.py / prepare_complex.py，导出一个可被程序调用的函数（主入口名示例：repair_pdb(...) 或 prepare_complex(...)），并提供 CLI（if __name__=="__main__"）输出 JSON。
API 服务：api_server_*.py，基于 FastAPI，暴露 /api/<主函数> 接口，接收 Pydantic 模型并返回模块函数的结果。
客户端：tool_factory.py，实现 ToolManager 类和 call_<tool>() 方法，默认指向 http://localhost:<port>，并在 description 字段按本规范写明用途与参数。

Description 写法（强制标准）

必须严格遵守下面三段结构（示例）：
一句话功能简介（一句话）
Args: 列出所有输入参数，类型与含义（逐行）
Return: 描述返回结构与字段说明

示例（few-shot）：
is_valid_smiles 示例：
"""Check if the input SMILES string is valid
Args:
smiles_list (List[str]): List of input SMILES strings
Return:
status (str): success/partial_success/error
msg (str): message
valid_res (List[dict]): List of dict, each containing the keys 'smiles' and 'is_valid'.
--smiles (str): A SMILES string of smiles_list
--is_valid (bool): Is the SMILES valid or not"""
fix_pdb 示例简短句：
"""使用 PDBFixer 修复 PDB 文件，返回修复结果和输出路径。
Args:
input_path (str): 输入 PDB 文件路径（必需）。
output_path (str): 输出 PDB 文件路径（必需）。
add_hydrogens (bool): 是否添加氢原子（--add-hydrogens）。
Return:
status (str): success/error
msg (str): 人类可读的信息
output_file (str | None): 修复后的文件路径（成功时返回）"""

封装细则（必须满足）

模块函数签名必须清晰、可编程调用（不要只保留 CLI）。
CLI：与原脚本参数一致，--help 显示原参数说明；脚本运行应输出 JSON（print JSON）。
API：端点名为 /api/<短名>（例如 /api/fix_pdb），端口建议 1000X 系列（如 10008 / 10009），可在本地用 uvicorn 启动。
客户端：ToolManager 包含 tool 描述（名称/endpoint/method/description），并提供超时参数与异常返回格式：{"status":"error","msg":...}。
README：在 .../tool_src/【tool_name】/readme.md 写入“三步验证命令”（启动 API、用 tool_factory 调用、在环境中直接运行 CLI），示例要给出 micromamba run -n <env> 或 conda activate 的命令，并说明环境依赖（如 gmx/obabel/pdbfixer/add_hydrogen_plus.py 等）。

实现输出（必须创建的文件）

/root/lwj/wll/code/DrugAgentTools/sxy_local/tool_src/【tool_name】/as_tool/ 包含：
【tool_name】.py（主模块，导出 main 函数/具体函数并提供 CLI）
api_server_【tool_name】.py（FastAPI 服务）
tool_factory.py（ToolManager 客户端）
/root/lwj/wll/code/DrugAgentTools/sxy_local/tool_src/【tool_name】/readme.md 包含三步验证命令与说明。

验收标准（检查项）

代码风格与示例 example / ref 一致（导入方式、返回 dict 结构）。
description 严格采用“功能句 + Args + Return”格式，列齐所有参数。
CLI：python <module>.py -i ... -o ... 能运行并返回 JSON（或在缺依赖时返回明确错误 JSON）。
API：uvicorn api_server_...:app --app-dir <path> --host 0.0.0.0 --port <port> --reload 能启动并健康检查 /health 返回 {"status":"healthy"}。
客户端：ToolManager.call_<tool>() 在 API 可用时能返回 JSON；在 API 不可达时返回 {"status":"error","msg":...}。
README 中的三步命令可复制粘贴执行并能复现验证过程（或给出替代的 conda 命令）。

自检流程（自动/人工复核）

代码静态检查：能 import 新模块并显示 help()；CLI --help 显示参数。
运行 API：在目标环境（示例名 tool_env）用 uvicorn 启动，访问 http://localhost:<port>/health，应返回 JSON。
客户端调用：执行 python - <<'PY' ... 的一次示例，确认 JSON 返回并且 work_dir 或 output_file（如适用）存在。
CLI 运行：用 micromamba/conda run -n <env> 直接运行主模块的一次示例（不必执行长时间 MD——如有长任务，传 --no-md 或 full_md=False），检查是否生成预期中间输出。

Prompt-engineering 技巧与 few-shot

给出 2 个短示例（示例 1：fix_pdb，示例 2：gmx_prepare_complex），展示期望的 description、API 路径與 tool_factory 返回格式（在实际使用之前请替换为真实脚本）。
要求模型在生成代码和文件后列出“自检清单”并执行（尽量自动化执行步骤 1-3）。
要求在每次修改后只提交最小变更补丁（用 apply_patch 风格），并报告新增/修改的文件路径。
要求在生成文件时把模块导入路径写为相对包路径（如 from tool_src.gmxMMPBSA_scripts.prepare_complex_v4 import ComplexPreparation），以便在项目根目录运行。

few-shot 示例（短）

示例 A（fix_pdb 简要）：
tool_name: fix_pdb
主模块导出 repair_pdb(input_path, output_path, add_hydrogens=False, ph=7.0, ...) -> dict
API: /api/fix_pdb
客户端: ToolManager.call_fix_pdb(input_path, output_path, ...) -> dict
description：见之前示例（功能句 + Args + Return）

示例 B（gmx_prepare_complex 简要）：
tool_name: gmx_prepare_complex
主模块导出 prepare_complex(protein, ligand, work_dir='.', full_md=False, ...) -> dict
API: /api/prepare_complex
客户端: ToolManager.call_prepare_complex(payload) -> dict
README: 三步验证命令（启动 API、client 调用、直接 CLI）

交付格式（对接 CI / 开发者）

修改以补丁方式提交（列出新增/修改文件）
附带一个短的验证脚本/命令片段，便于 reviewer 一键复现最小功能（例如只做“诊断/不执行长任务”模式）

结束语

完成后请把 tool_name、新增文件路径與短的“如何运行一次快速验证”的命令行摘要返回給我（不超过 6 行），並执行自检清单中至少第 1-3 步（能在当前环境中执行的則执行并报告結果；若受限則給出明确说明）。
```


## Use Cases

中文：把分散的脚本快速标准化为团队工具，便于 CI/服务化和复现。

English: Standardize ad-hoc scripts into reproducible team tools for CI, API access, and developer onboarding.
