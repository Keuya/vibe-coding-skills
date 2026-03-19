[中文](./README.md)

# VibeSkills

> 🐙 An integrated AI capability stack that brings upstream projects, hundreds of skills, MCP entry points, plugin surfaces, and governance rules into one runtime.

`VibeSkills` is the public-facing name of the project. `VCO` is the governed runtime behind it. This is not a single-purpose utility repo, and it is not just a bundle of prompts that happens to know how to write code. It is an already-integrated capability system: `340` directly callable skills and capability modules, `19` absorbed upstream projects and practice sources, and `129` config-backed policies, contracts, and rules that keep skills, MCP, plugins, workflows, verification, and cleanup inside one governable execution surface.

<p align="center">
  <sub>🧠 Planning · 🛠️ Engineering · 🤖 AI · 🔬 Research · 🧬 Life Sciences · 🎨 Visualization · 🎬 Media</sub>
</p>

## ✦ What This Repository Can Help You Do From Day One

If you look at these `340` skills through the lens of real work instead of repository folders, `VibeSkills` already covers a full capability chain: requirement discovery, solution design, implementation, testing, documentation, data analysis, research support, life-science workflows, and media generation. The table below is designed as a quick-scan capability map.

| Capability Area | What It Covers | Representative Capabilities |
| --- | --- | --- |
| Requirement discovery and problem framing | Turn vague requests into clear, bounded, testable problem definitions | `brainstorming`, `create-plan`, `speckit-clarify`, `aios-analyst`, `aios-pm` |
| Product planning and task breakdown | Convert ideas into specs, plans, tasks, milestones, and execution order | `writing-plans`, `speckit-specify`, `speckit-plan`, `speckit-tasks`, `aios-po`, `aios-sm` |
| Architecture design and technical choice | Shape frontend, backend, API, data, and deployment structure | `aios-architect`, `architecture-patterns`, `context-fundamentals`, `aios-master` |
| Software engineering and code implementation | Build features, scaffold projects, integrate systems, and land multi-file work | `aios-dev`, `autonomous-builder`, `speckit-implement` |
| Debugging, repair, and refactoring | Diagnose failures, fix behavior, remove code slop, and restore maintainability | `error-resolver`, `debugging-strategies`, `systematic-debugging`, `deslop` |
| Testing and quality assurance | Design tests, verify regressions, enforce gates, and validate completion | `tdd-guide`, `aios-qa`, `code-review`, `verification-before-completion` |
| GitHub operations and release workflows | Handle issues, PRs, CI repair, review comments, deploys, and releases | `aios-devops`, `gh-fix-ci`, `github_*`, `workflow_*`, `vercel-deploy` |
| Governed workflows and multi-agent collaboration | Freeze requirements, orchestrate execution, assign work, and retain proof | `vibe`, `swarm_*`, `task_*`, `agent_*`, `hive-mind-advanced` |
| Skill activation and capability routing | Pull the right skill, MCP surface, plugin, or rule into the right stage | `vibe`, `deepagent-toolchain-plan`, `hooks_route`, `semantic-router` |
| MCP and external system integration | Connect browsers, scraping, design files, third-party services, and external context | `mcp-integration`, `playwright`, `scrapling`, `figma` |
| Documentation and knowledge capture | Write READMEs, technical docs, guides, diagrams, and reusable knowledge | `docs-write`, `docs-review`, `markdown-mermaid-writing`, `knowledge-steward` |
| Office documents and file workflows | Work with Word, PDF, Excel, CSV, conversion, formatting, and comment replies | `docx`, `pdf`, `xlsx`, `spreadsheet`, `markitdown` |
| Data analysis and statistical modeling | Run EDA, regression, statistical tests, cleaning, and reporting | `statistical-analysis`, `statsmodels`, `scikit-learn`, `polars`, `dask` |
| Machine learning and AI engineering | Cover the loop from data preparation to training, evaluation, explainability, and retrieval | `senior-ml-engineer`, `training-machine-learning-models`, `shap`, `embedding-strategies` |
| Visualization and presentation | Build charts, interactive visuals, scientific figures, slides, and showcase pages | `plotly`, `matplotlib`, `seaborn`, `datavis`, `scientific-slides` |
| Research search and academic writing | Support literature search, reviews, citations, papers, and submission prep | `research-lookup`, `literature-review`, `citation-management`, `scientific-writing` |
| Life sciences and biomedicine | Support bioinformatics, single-cell workflows, proteins, drug discovery, and scientific databases | `biopython`, `scanpy`, `scvi-tools`, `alphafold-database`, `drugbank-database` |
| Mathematics, optimization, and scientific computing | Handle symbolic derivation, Bayesian work, optimization, simulation, and quantum workflows | `math-tools`, `sympy`, `pymc-bayesian-modeling`, `pymoo`, `qiskit` |
| Images, audio, video, and media production | Generate image, speech, subtitle, video, and multimedia outputs | `generate-image`, `imagegen`, `speech`, `transcribe`, `video-studio` |

This table is meant to make the operating surface easier to scan. Instead of pushing every section to maximum density, it gives you a fast picture of what kinds of work the repo can actually cover.

## 🧭 If You Break These Areas Down Further

The top-level table is for fast orientation. The deeper value of the repository becomes clearer when you look at it as a set of working surfaces rather than as a list of folders or skill names.

### 🧩 Planning, Architecture, And Delivery

- **Requirement discovery and problem framing**: Covers requirement interviews, problem definition, boundary detection, constraint intake, success criteria, and risk anticipation. The point is not to let AI sprint immediately, but to make the task legible first.
- **Product planning and task breakdown**: Covers specs, plans, tasks, milestones, dependencies, prioritization, and delivery order, so a large idea can become schedulable, trackable, and incrementally shippable.
- **Architecture design and technical choice**: Covers frontend structure, backend boundaries, API design, data layers, deployment layers, pattern choice, and stack comparison, so structural drift and rework get handled early.
- **Software engineering and code implementation**: Covers feature work, scaffolding, cross-file edits, module integration, engineering hardening, and automation, so plans actually become runnable implementation.
- **Debugging, repair, and refactoring**: Covers error diagnosis, root-cause isolation, behavior repair, slop cleanup, structural refactoring, and maintainability recovery, not just superficial patching.
- **Testing and quality assurance**: Covers unit tests, property-based tests, regression checks, acceptance validation, quality gates, and completion verification, so “it seems okay” becomes “there is evidence.”
- **Code review and engineering standards**: Covers review, risk checks, maintainability assessment, security review, performance review, and change recommendations, so code can stay workable over time.

### 🔗 Governance, Routing, And External Surfaces

- **GitHub operations and release workflows**: Covers issue and PR flow, CI repair, review-comment handling, release branches, deployment records, and go-live steps, so delivery does not stop at the local worktree.
- **Governed workflows and multi-agent collaboration**: Covers requirement freeze, staged execution, task assignment, proof artifacts, cleanup, and multi-agent coordination, so complex work happens inside a governed frame rather than inside a black box.
- **Skill activation and capability routing**: Covers rule-based routing, semantic routing, staged triggers, capability orchestration, and dormant-skill wake-up, addressing the common problem that capability exists but does not reliably activate.
- **MCP and external system integration**: Covers browser automation, extraction, design-to-code, third-party service hooks, plugin entry points, and external context intake, pulling fragmented tools into one runtime.
- **Documentation and knowledge capture**: Covers READMEs, technical guides, operating manuals, standards docs, diagrams, knowledge entries, and reports, so results remain reusable instead of staying trapped in chat history.
- **Office documents and file workflows**: Covers Word, PDF, Excel, CSV, conversion, comment replies, formatting retention, and document organization, filling a layer of real work that many AI repos ignore.

### 🔬 Data, AI, Research, And Professional Domains

- **Data analysis and statistical modeling**: Covers EDA, regression, hypothesis testing, metric systems, cleaning, transformation, distribution analysis, and reporting, turning raw data into interpretable conclusions.
- **Machine learning and AI engineering**: Covers model training, evaluation, feature work, explainability, embeddings, RAG, experiment tracking, and governed ML workflows. This is not just “the repo can train models”; it is a fuller AI engineering loop.
- **Research search and academic writing**: Covers literature search, review writing, citation management, paper drafting, submission prep, rebuttal writing, and academic standards. The strength here is the workflow chain, not a single isolated tool.
- **Life sciences and biomedicine**: Covers bioinformatics, single-cell analysis, protein structure, drug discovery, clinical-trial data, scientific databases, and lab-platform integration. This is one of the clearest differentiators in the repo.
- **Mathematics, optimization, and scientific computing**: Covers symbolic derivation, Bayesian modeling, multi-objective optimization, simulation, quantum computing, and scientific modeling for exact and advanced technical work.

### 🎨 Visualization, Presentation, And Media Output

- **Visualization and presentation**: Covers chart generation, interactive visualization, scientific figures, slide decks, web presentation, and information design, so outputs can become readable and presentable artifacts.
- **Images, audio, video, and media production**: Covers image generation, infographics, speech synthesis, subtitle generation, video production, and media packaging, supporting the path from static visuals to full multimedia delivery.

If you connect these layers back into a single flow, the repository is really covering a full working path: understand the request, create the plan, shape the architecture, implement, verify, collaborate, publish, then extend into documentation, data work, AI engineering, research workflows, life sciences, visualization, and media. That breadth is why governance and standardization matter here. Skill count alone is not enough.

The three clearest differentiators remain AI engineering, research writing, and life sciences. Many repositories mention machine learning or research support, but often only as scattered tool fragments. The difference here is that these areas are already organized into workflow chains instead of sitting as isolated capability points.

## 📦 What Is Already Integrated

This repository did not try to invent everything from scratch. It continuously absorbs mature methods, structures, and workflows that have already proven useful elsewhere, then governs them inside one system.

| Resource Layer | Current Depth | Why It Matters |
| --- | --- | --- |
| Skills and capability modules | `340` directly callable skills and capability modules | Cover the full work chain from requirement discovery, planning, and coding to verification, documentation, research, and media generation |
| MCP, plugins, and browser entry points | Multiple external-tool and context surfaces | Bring web services, designs, documents, search, and automation flows into the same runtime |
| Upstream projects and practice sources | `19` high-value projects and working traditions | Absorb proven strengths into one system instead of forcing people to manually assemble an ecosystem |
| Governance rules and contracts | `129` config-backed policies, contracts, and rules | Constrain clarification, planning, execution, verification, traceability, cleanup, and rollback so the system remains maintainable over time |

The project continuously integrates and governs strengths from `superpower`, `claude-scientific-skills`, `get-shit-done`, `aios-core`, `OpenSpec`, `ralph-claude-code`, and `SuperClaude_Framework`, pulling their advantages in prompt organization, skill accumulation, plan-driven execution, governed workflows, scientific support, and engineering discipline into one operating surface.

That is one of the clearest differences between `VibeSkills` and an ordinary prompt collection or skills index. What you are looking at is not a static directory. It is an integrated capability network that can be routed, governed, verified, and maintained.

## ✨ Why It Feels Different Right Away

Most skill repositories mainly answer one question: what is available here?

`VibeSkills` is more concerned with a different set of questions:

- what should be called now, instead of forcing you to manually search the ecosystem
- what should happen first, instead of letting the model sprint straight into execution
- which capabilities can be safely combined, and where boundaries need to stay explicit
- how outcomes get verified, retained, and kept out of long-term black-box drift

It is not about stacking more capability.
It is about integrating activation, governance, verification, and review into a system that can hold up under real use.

## ⚠️ The Pain Points It Is Trying To Solve

If you already use AI heavily, you have probably seen some version of these failures:

- there are too many skills, but no clear answer for which one fits the current moment
- skill activation rates are low, so capability exists in the repo but rarely gets triggered, remembered, or connected to the actual workflow
- projects, plugins, and workflows overlap with one another and then conflict with one another
- models start executing before the task is actually clear
- work ends without verification, evidence, or rollback surfaces
- the workflow gets more powerful over time, but also harder to understand

`VibeSkills` does not pretend these problems disappear on their own.
Its value is that it treats them as real design problems.

The `VCO` ecosystem is also trying to solve a very practical issue: not that there are too few skills, but that too many capabilities stay dormant and their real activation rate stays low. Through routing decisions, MCP and plugin entry points, workflow orchestration, and governance rules, the system tries to pull the right capability into the right stage of work instead of leaving it asleep in the repository.

## ⚙️ How It Works

You can think about it as three layers.

### 1. 🧠 Smart routing

In the right situations, you should not need to remember the exact skill name first.

`VibeSkills` combines rule-based routing and AI-assisted routing so the right capability is more likely to be activated in the right context. Part of what the `VCO` ecosystem is trying to solve is low skill activation rate, so more capabilities can enter the execution surface at the right moment instead of remaining technically present but practically unused.

### 2. 🧭 Governed workflows

This is not only about calling tools.
It is also about how work gets done in a stable way.

That is why the system tries to keep requirement clarification, confirmation, execution, verification, review, and traceability inside one working flow instead of letting the model sprint into a black box.

### 3. 🧩 Integrated capabilities

This is not just a pile of skills.

It also includes plugins, project integrations, workflow design, AI norms, safety boundaries, maintenance lessons, and the mistakes I have already made and do not want to repeat. `VCO` is the runtime layer that keeps those capabilities organized instead of leaving them scattered in unrelated places.

## 👥 Who It Is For

`VibeSkills` is mainly for:

- ordinary people who want AI to help more reliably
- heavy AI, agent, and automation users
- individuals or small teams who want more disciplined AI workflows
- anyone tired of a skill ecosystem that is rich in options but poor in usability

If you only want a single-purpose utility, this repo may be heavier than you need.
If you want AI to become steadier, easier to manage, and more useful over time, it is a much better fit.

## 🚀 Start Here

One important point first: this is not a traditional standalone app repository. It is a **skills-format project**, so the normal way to use it is to invoke the skill through the host environment instead of treating it like a regular CLI program.

- In Claude Code, use `/vibe`
- In Codex, use `$vibe`

If you want the shortest path to understanding the system before you install it:

- [`docs/quick-start.en.md`](./docs/quick-start.en.md)
- [`docs/manifesto.en.md`](./docs/manifesto.en.md)

If you are ready to install after that, use the one-step AI-assisted path:

- [`docs/install/one-click-install-release-copy.en.md`](./docs/install/one-click-install-release-copy.en.md)

If you are already a heavier user and want fuller installation detail:

- [`docs/install/recommended-full-path.en.md`](./docs/install/recommended-full-path.en.md)
- [`docs/cold-start-install-paths.en.md`](./docs/cold-start-install-paths.en.md)

## 📐 Project Philosophy

The core idea of `VibeSkills` is standardization. Only when requirement clarification, planning, execution, verification, traceability, and rollback are turned into reusable order does human intent become clearer, model execution become steadier, and long-term maintenance keep technical debt lower.

The project is not trying to make AI look more magical. It is trying to let people focus on describing goals while the remaining work can be carried, verified, and maintained inside a standardized workflow that is more callable, more governable, and more sustainable over time.
