# Nutrient

Parse, extract from and classify documents with [Nutrient DWS](https://www.nutrient.io/api/) from a conversation with
Claude. The plugin bundles the Nutrient connector with a skill that tells Claude when to use it, so a request such as
"Parse this document" or "Extract the invoice number and total" runs through Nutrient even when the file is attached to
the chat.

## Use it

1. Add the plugin, then connect the Nutrient connector from the plugin's Connectors tab and sign in with your Nutrient
   account. In Claude Code, install it with `/plugin install nutrient --marketplace PSPDFKit-labs/nutrient-claude-plugin`.
2. Attach a PDF, Office document or image, or point to an HTTPS link, and ask Claude to parse it, convert it to Markdown,
   extract fields or tables, or classify it.
3. Claude uploads the file to your Nutrient account and returns the result: Markdown with layout, structured fields with
   a citation for each value, or labels with scores. Where Claude shows the Nutrient panel, you can review each value
   beside its source on the page.

For Claude to upload a file attached to the chat itself, `mcp.nutrient.io` must be under Settings, Capabilities,
Additional allowed domains (set by an Owner on Team and Enterprise plans). Otherwise Claude asks you to drop the file in
the Nutrient panel.

## Data

The plugin sends the documents you ask Claude to process, and the instructions for each run, to your Nutrient DWS
account through `mcp.nutrient.io`. Uploaded files are kept for 24 hours; DWS stores each run under Nutrient's storage
policy, and each run uses your DWS credits. The service also records a short generic purpose that Claude writes for each
call, with no document content, for usage analytics. Summaries and questions about a document stay with Claude's own
reading unless you ask for one of these operations.
