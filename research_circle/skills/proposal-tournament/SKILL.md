# Skill: proposal-tournament

## Purpose

用多 reviewer 对抗式评审筛选 proposal，并输出可执行修订动作。

## Inputs

- `idea_tree.json`
- `safe_claims.md`
- `taste_scores.json`

## Outputs

- `runs/<run_id>/artifacts/proposal_tournament.md`
- `runs/<run_id>/artifacts/reviewer_objections.json`
- `runs/<run_id>/artifacts/revision_actions.md`
- `runs/<run_id>/artifacts/ranked_proposals.md`
- `runs/<run_id>/checkpoints/proposal-tournament.json`

## Reviewer Roles

- taste_critic
- novelty_prosecutor
- systems_reviewer
- theory_reviewer
- empirical_reviewer
- benchmark_validity_auditor
- venue_reviewer
- domain_skeptic

## Score Dimensions

- novelty_robustness
- research_taste
- defensibility
- thesis_clarity
- experimental_validity
- related_work_survivability
- venue_fit
- long_term_influence
- resource_realism

## Procedure

1. 组织多 reviewer 交叉评审与反驳。
2. 输出 objections、revision actions、route comparison。
3. 形成 1-3 条 ranked proposals，并保留 aggressive route 选项。

## Stop Conditions

- `ranked_proposals.md` 至少包含 conservative/main-track 两条可比较路线。
- 每条 proposal 给出 taste、defensibility、representative-work potential 评分。

## Human Checkpoint

- 必需：人类审批最终 shortlist。

