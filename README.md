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

## Contents

- [`plugins/nutrient`](plugins/nutrient): the plugin, with its [README](plugins/nutrient/README.md), which says what it
  sends to Nutrient
- [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json): lists the plugin, so this repository works as a
  marketplace
- [`ci/check.py`](ci/check.py): checks the plugin against [`ci/tools.json`](ci/tools.json), a snapshot of the service's
  tools; see [AGENTS.md](AGENTS.md) for changing the skill and refreshing the snapshot

## License

[MIT](LICENSE)
