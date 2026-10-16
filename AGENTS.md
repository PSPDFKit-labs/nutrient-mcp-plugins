# Nutrient MCP plugins: agent guidance

This repository publishes one plugin, `plugins/nutrient`, to Claude and to OpenAI (ChatGPT and Codex). Claude reads
`.claude-plugin/plugin.json`, OpenAI reads `.codex-plugin/plugin.json`, and both share `.mcp.json`, `skills/` and the
README and license. `.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json` list it for each host.
Anthropic's directory tracks this repository's default branch, so every merge to `main` is a release candidate there;
OpenAI's directory takes a ZIP of `plugins/nutrient`, uploaded for each release.

## Changing the plugin

1. Edit the skill in `plugins/nutrient/skills/nutrient-documents/SKILL.md`. Its `description` decides when Claude loads
   it: write it as the requests a user makes. Keep the body to what Claude must do differently from the tool
   descriptions; the service's own instructions and tool descriptions carry the rest. Keep it host-neutral: it runs in
   Claude, ChatGPT and Codex, and each takes a file differently (`chat_file`, `upload_documents`, `attached_file`).
2. Put every tool, argument, result field and error code in a code span. `ci/check.py` fails on any that the service
   doesn't list, so a renamed tool or field shows up in CI instead of in a conversation.
3. Raise `version` in `plugins/nutrient/.claude-plugin/plugin.json`, `plugins/nutrient/.codex-plugin/plugin.json` and
   the Claude marketplace entry, together.
4. Run `python3 ci/check.py` and `claude plugin validate ./plugins/nutrient` before opening a pull request. To try the
   OpenAI side without touching your Codex setup, run `codex plugin marketplace add .` and
   `codex plugin add nutrient@nutrient` with `CODEX_HOME` set to an empty folder.

Never change `name` in `plugin.json`: it is the plugin's permanent identity.

For packaging changes, also run `python3 -m unittest discover -s ci -p 'test_*.py'`. The ZIP uses an explicit file list
in `ci/package_openai.py`; add new referenced resources there deliberately. Never add reviewer access or local app mappings.
See [the submission handoff](docs/openai-submission.md) for checks that still require the owner and a live ChatGPT run.

## Refreshing the tool snapshot

`ci/tools.json` and `ci/tools-chatgpt.json` are the catalogs Hosted MCP (`hosted-mcp/` in the private Nutrient monorepo)
lists to a client that renders MCP Apps (Claude) and to ChatGPT. When the service changes its tools, inputs or result fields, regenerate it from the monorepo's `hosted-mcp/`:

```sh
MCP_TEST_APPS_CATALOG_PATH=/path/to/nutrient-mcp-plugins/ci/tools.json \
MCP_TEST_CHATGPT_CATALOG_PATH=/path/to/nutrient-mcp-plugins/ci/tools-chatgpt.json \
  dotnet run --project tests/Nutrient.Mcp.Tests --no-build --no-restore
```

The snapshot should match the service that is live in production, since the plugin connects to production.

## Submitting to OpenAI

Build the ZIP with `python3 ci/package_openai.py`. It runs `ci/check.py`, then writes
`dist/nutrient-openai-<version>.zip` from the plugin folder without Claude's manifest, so OpenAI reads only
`.codex-plugin/plugin.json`, and prints its files and SHA-256. The same commit always produces the same bytes.

Upload it in OpenAI's developer dashboard from a project with global data residency; an organization owner or a member
with Apps Management Write submits, after the organization's identity is verified. The review metadata lives in
`.codex-plugin/plugin.json` under `extensions.com.openai`: five positive and three negative test cases, `commerce`, the
release notes and, once recorded, `demo_recording_url`. `ci/check.py` enforces the case counts and fields, and that each
case triggers a tool ChatGPT is listed. Imported cases are read-only in the dashboard, so change them here and upload a
new ZIP. Run every positive case with the reviewer account before submitting. Reviewer credentials go only in the
dashboard's Review details; the ZIP rejects them. OpenAI also verifies the domain: the dashboard issues a challenge token that must be served as plain text at
`https://mcp.nutrient.io/.well-known/openai-apps-challenge` (or on an eligible parent domain) before review.
