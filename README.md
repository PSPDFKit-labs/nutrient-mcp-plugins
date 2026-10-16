# Nutrient MCP plugins

Parse, extract from and classify documents with [Nutrient DWS](https://www.nutrient.io/api/) in Claude, ChatGPT and
Codex. The plugin bundles the Nutrient connector (`https://mcp.nutrient.io/mcp`) with a skill that tells the assistant
when to use it, so a request such as "Parse this document" or "Extract the invoice number and total" runs through
Nutrient, even when the file is attached to the chat.

## Install

- **Claude Code**: `/plugin install nutrient --marketplace PSPDFKit-labs/nutrient-mcp-plugins`
- **claude.ai, Claude desktop and Cowork**: open Customize, Plugins, Add, Add marketplace, and enter
  `https://github.com/PSPDFKit-labs/nutrient-mcp-plugins`. Then add the Nutrient plugin and connect its connector from
  the plugin's Connectors tab with your Nutrient account.
- **Codex**: `codex plugin marketplace add PSPDFKit-labs/nutrient-mcp-plugins`, then
  `codex plugin add nutrient@nutrient`, and sign in with your Nutrient account when Codex asks.

On Team and Enterprise plans, an Owner can roll the plugin out to the whole organization.

## Contents

- [`plugins/nutrient`](plugins/nutrient): the plugin, with its [README](plugins/nutrient/README.md), which says what it
  sends to Nutrient. Claude reads `.claude-plugin/plugin.json` and OpenAI reads `.codex-plugin/plugin.json`; both use
  the same connector (`.mcp.json`) and skill.
- [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) and
  [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json): list the plugin, so this repository works as a
  marketplace for Claude and for Codex
- [`ci/check.py`](ci/check.py): checks the plugin against [`ci/tools.json`](ci/tools.json), a snapshot of the service's
  tools; see [AGENTS.md](AGENTS.md) for changing the skill and refreshing the snapshot

## OpenAI submission

The existing submission package is built with `python3 ci/package_openai.py`. See the
[submission handoff](docs/openai-submission.md) for validation, review cases and remaining owner steps. A passing local
build is not a completed directory review.

## License

[MIT](LICENSE)
