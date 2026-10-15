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
   with citations for the values it finds, or labels with scores. Where the Nutrient panel appears, you can review each value
   beside its source on the page.

In ChatGPT, Nutrient fetches a file attached to the chat from the link ChatGPT provides. In Claude, for Claude to upload
an attached file itself, `mcp.nutrient.io` must be under Settings, Capabilities, Additional allowed domains (set by an
Owner on Team and Enterprise plans); otherwise Claude asks you to drop the file in the Nutrient panel.

## Data

The plugin sends the documents you ask the assistant to process, and the instructions for each run, to your Nutrient
DWS account through `mcp.nutrient.io`; it sends them nowhere else. To send a file from your computer, or one attached
to the chat, the assistant runs a one-time curl command that the connector returns: it uploads only the files you named
to `mcp.nutrient.io` and expires within five minutes. Uploaded files are kept for 24 hours. DWS keeps each run for your
plan's retention period, and each run uses your DWS credits. Opening a document in the Nutrient panel's full-screen
review stores a copy in DWS Viewer, which stays until you delete it and counts toward your plan's document limit.
The panel's document viewer also reports usage metrics to Nutrient: which viewer features are used, the viewer's
product and license details, a random identifier it keeps in the browser, and the document's DWS Viewer ID, or a hash
of the file's first 16 KB when it shows a local copy. The metrics include no document content.
Summaries and questions about a document stay with the assistant's own reading unless you ask for one of these
operations.

Privacy policy: https://www.nutrient.io/legal/privacy/

## Troubleshooting

- **HTTP 403 "Host not in allowlist" when uploading:** allow `mcp.nutrient.io` in the app's network settings (in Claude:
  Settings, Capabilities, Additional allowed domains), or drop the file in the Nutrient panel when it asks for it.
- **The connector asks you to connect or reconnect:** sign in again from the plugin's or the connector's settings.
- **`permission_denied`:** your Nutrient account doesn't include the product the request needs, such as Data Extraction
  or Processor. Check your plan in the DWS dashboard.
- **Not enough credits:** a run stops before processing when your DWS credits run out; add credits in the DWS dashboard.

## Support

- Help with the plugin or your Nutrient account: https://www.nutrient.io/company/contact/ or https://www.nutrient.io/support/request/
- Report a security vulnerability: https://www.nutrient.io/security/report-vulnerability/
