# VCO Routing Stability Gate

- Mode: `default`
- Generated: `2026-03-15T12:56:05`
- Gate Passed: `True`
- Stricter Rules Ready: `True`

## Metrics

- route_stability: `1` (threshold `0.75`)
- top1_top2_gap: `0.3416` (threshold `0.051`)
- fallback_rate: `0` (threshold `0.85`)
- misroute_rate: `0.1` (threshold `0.3`)

## Group Stability

- `orchestration-planning`: stability=`1` dominant=`orchestration-core|writing-plans`
- `code-quality-review`: stability=`1` dominant=`code-quality|code-reviewer`
- `data-ml-research`: stability=`1` dominant=`data-ml|scikit-learn`
- `docs-media-coding-xlsx`: stability=`1` dominant=`docs-media|xlsx`
- `docs-media-coding-tabular`: stability=`1` dominant=`docs-media|spreadsheet`
- `integration-devops-ci-debug`: stability=`1` dominant=`integration-devops|gh-fix-ci`
- `integration-devops-sentry-debug`: stability=`1` dominant=`integration-devops|sentry`
- `ai-llm-research-openai-docs`: stability=`1` dominant=`ai-llm|openai-docs`
- `ai-llm-research-embedding`: stability=`1` dominant=`ai-llm|embedding-strategies`
- `research-design-planning`: stability=`1` dominant=`research-design|designing-experiments`
- `aios-core-planning-pm`: stability=`1` dominant=`aios-core|aios-pm`
- `aios-core-planning-po`: stability=`1` dominant=`aios-core|aios-po`
