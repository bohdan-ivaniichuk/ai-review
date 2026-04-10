# ai-review

Learning repo for experimenting with **automated code review** workflows and tooling.

## Goals

We will try different scenarios to see what works best for feedback quality, speed, and fit with our process:

### 1. CodeRabbit

Evaluate [CodeRabbit](https://coderabbit.ai/) for pull-request reviews: comments, suggestions, and how it behaves on small vs. large diffs.

### 2. Custom pipeline (Claude API)

Build a **custom pipeline** that calls the **Claude API** (or compatible endpoints) to review changes—e.g. on PR events or in CI—so we can tune prompts, context, and guardrails.

**Possible extensions**

- Integrations with **boards** (e.g. Jira, Linear, GitHub Projects) to link review output or status to tasks.
- Room to iterate on cost, latency, and review depth.

## Repo layout

This section will grow as we add scripts, workflows, and config for each scenario.

---

*This README is the starting point; we will extend it as experiments land.*
