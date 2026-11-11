# Cursor Adapter

## Integration Method

Cursor loads `.md` files under `.cursor/rules/` as project rules.

### Quick Integration

```bash
# Option 1: Symlink (recommended — auto-syncs)
mkdir -p .cursor/rules
ln -s ../../.claude/rules/* .cursor/rules/
ln -s ../../CLAUDE.md .cursor/rules/ai-engine-entry.md

# Option 2: Copy (one-time)
cp .claude/rules/* .cursor/rules/
cp CLAUDE.md .cursor/rules/ai-engine-entry.md
```

### Rule Loading
Cursor loads all `.md` files under `.cursor/rules/` as project rules. With ai-engine v5.2.0, this means all 47 rules are active.

### Minimal Install
Not every project needs all 47 rules. Pick by pain point:
- Copy only the rules matching your current problems
- See README.md "按痛点安装" section for guidance

### Notes
- Symlinks keep rules in sync when you `git pull` updates
- Memory file paths (memory/) are unchanged
