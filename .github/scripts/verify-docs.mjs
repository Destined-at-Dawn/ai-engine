import { existsSync, readdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const meta = JSON.parse(readFileSync(join(root, "project-meta.json"), "utf8"));
const errors = [];

function filesRecursively(directory) {
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const path = join(directory, entry.name);
    return entry.isDirectory() ? filesRecursively(path) : [path];
  });
}

const ruleDirectory = join(root, ".claude", "rules");
const actualRuleCount = filesRecursively(ruleDirectory).filter((path) => path.endsWith(".md")).length;
if (actualRuleCount !== meta.rule_count) {
  errors.push(`project-meta.json declares ${meta.rule_count} rule files, but found ${actualRuleCount}.`);
}

for (const path of [
  "README.md",
  "README.en.md",
  "CONTRIBUTING.md",
  "SECURITY.md",
  "CODE_OF_CONDUCT.md",
  "docs/capabilities.md",
  "docs/agent-install.md",
  "docs/compatibility.md",
  "adapters/codex.md",
  "adapters/codex/AGENTS.md.example",
  ".github/PULL_REQUEST_TEMPLATE.md",
  "tools/agent-coord/coord.py",
  "tools/agent-coord/test_coord.py",
  "tools/agent-coord/README.md",
]) {
  if (!existsSync(join(root, path))) errors.push(`Required community or documentation file is missing: ${path}`);
}

const currentFacingDocs = [
  "README.md",
  "README.en.md",
  "docs/agent-install.md",
  "docs/compatibility.md",
  "docs/philosophy.md",
  "adapters/codex.md",
  "adapters/cursor.md",
  "adapters/gemini-cli.md",
  "docs/capabilities.md",
];
const staleCurrentState = /(?:niuma-engine\s+v4\.0|v4\.0\s*\(29\s*rules?\)|\b29\s+(?:rules?|条规则)\b|\b3[34]\s+(?:rules?|条规则|个规则文件|Markdown rule files)\b|v5\.[01]\.0\s*\/\s*34)/iu;
for (const path of currentFacingDocs) {
  const text = readFileSync(join(root, path), "utf8");
  if (staleCurrentState.test(text)) errors.push(`Stale current-state wording found in ${path}.`);
}

if (errors.length) {
  console.error("Documentation verification failed:");
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log(`Documentation verification passed: v${meta.current_version}, ${actualRuleCount} rule files.`);
