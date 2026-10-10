# Nutrient Claude plugin

Parse, extract from and classify documents with [Nutrient DWS](https://www.nutrient.io/api/) in Claude: claude.ai,
the desktop app, Cowork and Claude Code. The plugin bundles the Nutrient connector (`https://mcp.nutrient.io/mcp`)
with a skill that tells Claude when to use it, so a request such as "Parse this document" or "Extract the invoice number
and total" runs through Nutrient, even when the file is attached to the chat.

## Install

- **Claude Code**: `/plugin install nutrient --marketplace PSPDFKit-labs/nutrient-claude-plugin`
- **claude.ai, desktop and Cowork**: open Customize, Plugins, Add, Add marketplace, and enter
  `https://github.com/PSPDFKit-labs/nutrient-claude-plugin`. Then add the Nutrient plugin and connect its connector from
  the plugin's Connectors tab with your Nutrient account.

On Team and Enterprise plans, an Owner can roll the plugin out to the whole organization.

## Why a plugin

claude.ai doesn't pass a connector's server instructions to the model, and by default it loads only the connector's tool
names until Claude searches for a tool. With the connector alone, Claude usually reads an attached document itself. The
skill's description stays in Claude's context and routes parse, OCR, Markdown, extraction and classification requests
to Nutrient. In a small claude.ai test of six requests with an invoice attached, the plugin got 5 to call the connector,
against 1 with the connector alone.

Other MCP clients, such as ChatGPT, Cursor or VS Code, connect to `https://mcp.nutrient.io/mcp` directly.

## Contents

- [`plugins/nutrient`](plugins/nutrient): the plugin, with its [README](plugins/nutrient/README.md), which says what it
  sends to Nutrient
- [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json): lists the plugin, so this repository works as a
  marketplace
- [`ci/check.py`](ci/check.py): checks the plugin against [`ci/tools.json`](ci/tools.json), a snapshot of the service's
  tools; see [AGENTS.md](AGENTS.md) for changing the skill and refreshing the snapshot

## License

[MIT](LICENSE)
