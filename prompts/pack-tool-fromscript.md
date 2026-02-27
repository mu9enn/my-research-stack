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
你是一名 Drug Screening Agent 工具封装专家。请把“单个源代码文件”封装为完整工具文件夹，并严格遵守以下规范与步骤。你必须直接产出代码并完成自检，不要只给建议。

【输入信息】
- SOURCE_CODE: {SOURCE_CODE_ABS_PATH}   # 例如 .../tool_src/xxx/as_tool/xxx_main.py
- TOOL_ROOT: /root/lwj/wll/code/DrugAgentTools/sxy_local/tool_src
- RESULT_ROOT: /root/lwj/wll/code/DrugAgentTools/sxy_local/tool_result/{tool_name}_result
- TOOL_NAME: {可留空；若留空请你基于功能自动命名为英小写下划线}
- API_PORT: {100xx}
- ENV_NAME: {conda_or_micromamba_env_name}

【总目标】
从 SOURCE_CODE 生成并落盘一个完整封装目录：
{TOOL_ROOT}/{tool_name}/
  readme.md
  as_tool/
    {tool_name}.py                # wrapper 主模块（可编程入口 + CLI JSON）
    api_server_{tool_name}.py     # FastAPI
    tool_factory.py               # ToolManager 客户端

==================================================
一、封装原则（强制）
==================================================
1) 优先“委托源代码”，禁止重写核心算法  
- wrapper 必须优先通过 importlib 或直接 import 复用 SOURCE_CODE 的 parser/main/核心函数。
- 仅做参数整形、路径管理、错误处理、结果结构化。
- 保留源脚本 stdout/stderr（不要吞日志），但 wrapper 最终要返回结构化 dict，CLI 最终 print JSON。

2) 输入参数最小暴露  
- 仅暴露业务核心参数（由 SOURCE_CODE 的“使用示例/核心入口签名/argparse 主参数”推导）。
- 输出路径类参数（如 output_dir/out_dir/save_dir）默认不对外暴露，统一由 wrapper 内部自动生成。
- 非核心但 SOURCE_CODE 必需参数：在 wrapper 内提供合理默认值。

3) 输出统一结构  
所有成功/失败分支都返回：
{
  "status": "success|error|partial_success",
  "msg": "...",
  ...关键业务字段...
}
- 若产出文件：返回 output_dir / 关键文件路径
- 若产出指标：返回 metrics/pred_scores/affinity 等具体字段
- 禁止泛化字段名 data/extra（除非确实不可避免）

4) 结果目录策略  
- 固定根目录 RESULT_ROOT。
- 每次运行创建唯一子目录：{tool_name}_{timestamp}_{short_uuid}，避免覆盖。
- dry-run 也要创建可追踪目录并返回 output_dir。

5) description 强制格式（tool_factory）  
必须是三段：
- 首句：一句话功能与适用场景（英文，不得写“this wraps...”）
- Args:
  name (type): meaning, default...
- Return:
  field (type): meaning...

==================================================
二、你必须执行的实现步骤
==================================================
Step 1. 深读 SOURCE_CODE，提取真实接口
- 找以下信息并列出：
  a) 主入口函数/CLI 入口（main/build_parser/run_*）
  b) 核心必需参数、可选参数、默认值、类型
  c) 真实输出（文件、目录、指标、日志）
  d) 失败模式（常见异常、参数错误）
- 若 SOURCE_CODE 与示例注释冲突，以“函数签名 + argparse 定义 + return/输出行为”为准。

Step 2. 生成 wrapper：as_tool/{tool_name}.py
- 对外暴露一个程序化入口：run_{tool_name}(...) -> dict
- 提供 CLI：python {tool_name}.py ...，最终 stdout 输出 JSON
- wrapper 内实现：
  - mode/参数归一化（必要时支持兼容别名）
  - 自动创建 run_dir（RESULT_ROOT 下）
  - 调用 SOURCE_CODE（优先 importlib + main/build_parser 或核心函数）
  - 捕获异常并返回 {"status":"error","msg":...}
  - 解析关键结果（指标/关键文件路径）并放入返回 dict
- 若委托执行期间需要改写 `sys.argv`/cwd，执行后必须恢复现场。

Step 3. 生成 API：api_server_{tool_name}.py
- FastAPI + `/health` 返回 {"status":"healthy"}
- POST `/api/{tool_name}`，请求模型字段与 wrapper 暴露参数严格一致（不要多、不要少）
- API 只负责参数接收与调用 wrapper，不复制业务逻辑
- 返回 wrapper 原样 dict

Step 4. 生成 ToolManager：tool_factory.py
- `self.tools["{tool_name}"]` 至少包含 endpoint/method/description
- `description` 严格按“首句 + Args + Return”多行格式
- 提供 `call_{tool_name}(payload: dict, timeout: Optional[int]=None) -> dict`
- API 不可达或异常时，统一返回 {"status":"error","msg": "..."}。

Step 5. 生成 readme.md（3步验证）
必须包含可复制命令：
1) 启动 API（uvicorn）
2) ToolManager 调用示例（python heredoc）
3) 直接 CLI 调用示例（尽量提供轻量参数，如 dry-run）
并注明环境依赖与安装提示（conda/micromamba）。

==================================================
三、一致性与防错修复（必须自动执行）
==================================================
你必须做以下“对齐检查”，并自动修复不一致：
1) wrapper 签名 vs API RequestModel 字段：完全一致
2) API 字段 vs tool_factory description Args：完全一致
3) wrapper 返回字段 vs tool_factory description Return：完全一致
4) 命名统一：禁止同时出现 out_dir/output_dir/save_dir 混用
5) CLI flag 到 wrapper 参数映射表：在最终说明中列出
6) 对 SOURCE_CODE 不支持的参数，禁止透传（避免 argparse unrecognized arguments）

==================================================
四、验收与自检（必须执行并报告）
==================================================
A. 静态检查
- 对 4 个关键文件做语法/诊断检查，确保无错误：
  - as_tool/{tool_name}.py
  - as_tool/api_server_{tool_name}.py
  - as_tool/tool_factory.py
  - SOURCE_CODE
B. 运行级最小验证（能跑则跑）
1) `python as_tool/{tool_name}.py --help`
2) dry-run CLI 一次，检查返回 JSON 与 output_dir
3) 启动 API 后请求 `/health`
4) 用 ToolManager 发起一次最小 payload，检查 JSON 返回
- 若环境限制无法完整执行，明确写“已完成到哪一步 + 阻塞原因 + 替代验证命令”。

==================================================
五、输出格式（你最终回复必须包含）
==================================================
1) 变更清单：新增/修改文件路径
2) 调用链摘要：SOURCE_CODE -> wrapper -> API -> ToolManager（每层职责一句话）
3) CLI flag -> wrapper 参数映射表
4) 最终 description 文本（可直接粘贴到 tool_factory）
5) 自检结果（步骤A/B逐条通过或失败原因）
6) 一键最小复现命令（不超过6行）

注意：
- 仅做最小必要改动，不改无关文件。
- 保持现有代码风格。
- 若发现潜在 500 高风险点（参数不匹配、返回字段漂移、透传未知参数），必须在本次一次性修复。
```


## Use Cases

中文：把分散的脚本快速标准化为团队工具，便于 CI/服务化和复现。

English: Standardize ad-hoc scripts into reproducible team tools for CI, API access, and developer onboarding.
