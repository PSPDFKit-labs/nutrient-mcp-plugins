# Nutrient Claude plugin: agent guidance

This repository publishes one Claude plugin, `plugins/nutrient`, and lists it in `.claude-plugin/marketplace.json`.
Anthropic's directory tracks this repository's default branch, so every merge to `main` is a release candidate.

## Changing the plugin

1. Edit the skill in `plugins/nutrient/skills/nutrient-documents/SKILL.md`. Its `description` decides when Claude loads
   it: write it as the requests a user makes. Keep the body to what Claude must do differently from the tool
   descriptions; the service's own instructions and tool descriptions carry the rest.
2. Put every tool, argument, result field and error code in a code span. `ci/check.py` fails on any that the service
   doesn't list, so a renamed tool or field shows up in CI instead of in a conversation.
3. Raise `version` in `plugins/nutrient/.claude-plugin/plugin.json` and in the marketplace entry, together.
4. Run `python3 ci/check.py` and `claude plugin validate ./plugins/nutrient` before opening a pull request.

Never change `name` in `plugin.json`: it is the plugin's permanent identity.

## Refreshing the tool snapshot

`ci/tools.json` is the catalog Hosted MCP (`hosted-mcp/` in the private Nutrient monorepo) lists to a client that renders
MCP Apps. When the service changes its tools, inputs or result fields, regenerate it from the monorepo's `hosted-mcp/`:

```sh
MCP_TEST_APPS_CATALOG_PATH=/path/to/nutrient-claude-plugin/ci/tools.json dotnet run --project tests/Nutrient.Mcp.Tests --no-build --no-restore
```

The snapshot should match the service that is live in production, since the plugin connects to production.
