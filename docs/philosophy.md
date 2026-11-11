# Design philosophy

## A discipline framework for AI-assisted engineering

ai-engine encodes recurring engineering failure patterns as reviewable rules. Its goal is not to make a coding model smarter; its goal is to make important workflow expectations explicit: inspect before changing, verify before declaring completion, record dead ends, and isolate concurrent work.

## How a rule should earn its place

A useful rule describes:

1. **Failure mode** — what went wrong or can predictably go wrong.
2. **Trigger** — when the rule applies.
3. **Action** — what the agent or maintainer should do.
4. **Verification** — what evidence shows the action happened.
5. **Limitation** — what the rule does not guarantee.

This structure makes rules discussable and revisable. A rule that does not improve a real decision can be simplified or removed.

## Shipped rules versus reference architectures

The repository currently ships Markdown rules, templates, and agent-integration guidance. Some rules describe broader patterns, such as backup layers, knowledge synchronization, and redundant scheduling. These are **reference architectures**, not bundled automation services.

A user who adopts those patterns must choose and operate the scripts, branch protections, storage, scheduler, credentials, and monitoring appropriate for their own environment. See [Capabilities](capabilities.md) for the public boundary.

## Evidence over claims

Claims about reliability, compatibility, usage, or automation should be linked to public artifacts whenever possible. When a statement reflects maintainer experience rather than independent evidence, label it as such. Release notes and documentation should state the tested version and known limitations.

## Evolution

The ruleset evolves through maintainer observations, user feedback, reproducible counterexamples, and contribution review. A strong contribution shows not only a new rule, but also the failure pattern it addresses and a way to validate its value.
