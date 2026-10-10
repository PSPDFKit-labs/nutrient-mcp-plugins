# Nutrient

Parse, extract from and classify documents with [Nutrient DWS](https://www.nutrient.io/api/) from a conversation with
Claude, ChatGPT or Codex. The plugin bundles the Nutrient connector with a skill that tells the assistant when to use it,
so a request such as "Parse this document" or "Extract the invoice number and total" runs through Nutrient even when the
file is attached to the chat.

## Use it

1. Add the plugin, then connect the Nutrient connector and sign in with your Nutrient account. In Claude Code, install it
   with `/plugin install nutrient --marketplace PSPDFKit-labs/nutrient-mcp-plugins`; in Codex, with
   `codex plugin marketplace add PSPDFKit-labs/nutrient-mcp-plugins` and `codex plugin add nutrient@nutrient`.
2. Attach a PDF, Office document or image, point to a file on disk or an HTTPS link, and ask to parse it, convert it to
   Markdown, extract fields or tables, or classify it.
3. The assistant sends the file to your Nutrient account and returns the result: Markdown with layout, structured fields
   with a citation for each value, or labels with scores. Where the Nutrient panel appears, you can review each value
   beside its source on the page.

In ChatGPT, Nutrient fetches a file attached to the chat from the link ChatGPT provides. In Claude, for Claude to upload
an attached file itself, `mcp.nutrient.io` must be under Settings, Capabilities, Additional allowed domains (set by an
Owner on Team and Enterprise plans); otherwise Claude asks you to drop the file in the Nutrient panel.

## Data

The plugin sends the documents you ask the assistant to process, and the instructions for each run, to your Nutrient
DWS account through `mcp.nutrient.io`. Uploaded files are kept for 24 hours; DWS stores each run under Nutrient's
storage policy, and each run uses your DWS credits. The service also records a short generic purpose that the assistant
writes for each call, with no document content, for usage analytics. Summaries and questions about a document stay with
the assistant's own reading unless you ask for one of these operations.
