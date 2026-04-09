### this is to write a README.md for a github repo.

```text

# Prompt: Generate a Professional Open-Source README from Repository Structure

You are a senior developer advocate and technical writer. Create a polished `README.md` directly in this repository based on the actual project files and scripts.

## Goal
Write a professional, credible, and easy-to-scan README for an open-source engineering/research project. Keep the style modern and confident, but practical and honest.

## Writing Principles (Soft Guidance)
- Prioritize clarity over verbosity.
- Match the structure to this project (do not force a fixed template).
- Explain what users can do *now* (quickstart first, then deeper details).
- Keep claims grounded in repository evidence.
- Prefer short paragraphs + concrete bullets.
- Use section names that feel natural for this project.
- Add light human warmth in wording while keeping technical credibility.

## Required Workflow
1. Inspect the repository tree and key files (`README.md`, config files, launch scripts, eval scripts, assets, paper links if present).
2. If a paper source file exists (for example `original_paper.tex`), extract core terminology and claims from abstract/introduction/contributions for wording alignment.
3. Infer the real runnable paths/commands from code, not assumptions.
4. Draft a complete `README.md` with a logical flow.
5. Insert project images from `assets/` at meaningful positions if available.
6. Ensure all commands are executable as written (paths/filenames must exist).

## Content Expectations
Include the following *when applicable*:
- A title line with optional logo inline (if logo exists).
- Compact badge row (paper, license, language/runtime).
- Add a one-line project description/tagline directly under the badges (or title block).
- Add one short human-friendly line (for example, a polite star/support message) without sounding promotional.
- Overview that naturally integrates key capabilities (avoid duplicated sections).
- In the overview, align bullet points with the paper's stated core contributions when a paper source exists.
- Benchmark/dataset section with concise per-task descriptions.
- Start the benchmark section with an academically meaningful positioning sentence (not a purely structural sentence like “X is split into A/B”).
- Skills/modules section describing major components and their roles.
- A setup step that includes `git clone`, `cd`, and Conda environment creation from `environment.yaml` (when such file exists).
- Quickstart with environment setup from `.env.template` to `.env` (avoid embedding secret exports in README).
- Run instructions for main execution modes (can be merged in one code block with inline comments).
- Evaluation entrypoint usage.
- A short license section (for example: MIT + `LICENSE` file reference).
- Citation in BibTeX format if paper metadata is available.
- A small centered footer line adapted to the current project identity (team/project name + repository link + back-to-top link).

## Adaptation Rules
- If a typical section is not relevant, omit it cleanly.
- If this repository has custom terminology, prefer repository-native names.
- If multiple run modes exist, present them side-by-side with minimal friction.
- If there are optional/internal parts, label them clearly without clutter.

## Quality Bar
- Tone: professional, concise, and welcoming.
- Include a small amount of human warmth (1-2 lines max), while keeping a research/engineering tone.
- Formatting: clean Markdown with consistent heading levels.
- Prefer an emoji prefix for major `##` sections when it matches the project tone.
- Use selective bold emphasis for key ideas (capabilities, guarantees, major components), but avoid over-formatting.
- Prefer paper-aligned language for technical claims, and avoid claims not supported by repository artifacts.
- Improve sentence quality by favoring contribution-driven phrasing over directory-driven phrasing (describe *why it matters*, then *where it is*).
- Keep instructional microcopy concise; compress long explanatory sentences when one clear line is enough.
- No placeholder commands that do not map to real files.
- Never expose local absolute paths (e.g., `/Users/...`); use repo-relative paths or placeholders such as `<YOUR_CLONED_PROJECT_DIR>`.
- No secrets or private endpoints in text.
- Keep command snippets short and copy-paste friendly.

Now create or overwrite `README.md` accordingly.

```
