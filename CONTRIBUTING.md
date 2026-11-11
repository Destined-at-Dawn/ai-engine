# Contributing

Thanks for improving ai-engine. High-quality contributions make rules easier to understand, test, adapt, and maintain.

## Before you start

- Read [Capabilities](docs/capabilities.md) to distinguish shipped rules from reference architectures.
- Search existing Issues and Discussions before opening a duplicate topic.
- Keep public contributions free of personal data, private filesystem paths, credentials, proprietary material, and unverifiable adoption claims.

## Contribution types

- Rule fixes and additions grounded in a clear failure mode
- Agent adapters and compatibility corrections
- Documentation, translations, examples, and reproducible case studies
- Validation tooling and repository-maintenance improvements

## Rule proposal standard

A rule proposal should include:

1. The failure mode it addresses;
2. A trigger signal;
3. Concrete actions;
4. Verification steps;
5. Anti-patterns or limitations;
6. A public, anonymized example or reproducible fixture when practical.

Do not describe a private tool, personal workflow, or environment-specific automation as a general shipped capability without a linked public implementation.

## Local checks

Run the repository documentation check before opening a pull request:

```bash
node .github/scripts/verify-docs.mjs
```

The check validates metadata, rule-count consistency, required community files, and known stale claims in current-facing documentation.

## Pull request process

1. Fork the repository and create a focused branch.
2. Make the smallest coherent change.
3. Run the local check and update documentation affected by the change.
4. Explain the problem, scope, validation, and limitations in the pull request template.
5. Do not include unrelated formatting changes or generated files.

By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).
