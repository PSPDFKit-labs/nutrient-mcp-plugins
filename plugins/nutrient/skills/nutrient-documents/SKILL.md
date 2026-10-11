---
name: nutrient-documents
description: Use when the user asks to parse, OCR, transcribe or convert a document to Markdown, extract fields, values, line items or tables from it, or classify it, including a file attached to the chat that you could read yourself. Runs the request with the Nutrient connector, which returns OCR for scans, layout, citations for the values it finds and a stored run.
---

# Nutrient documents

Use the Nutrient connector for these requests, even when the file is attached to the chat and its content is already in
the conversation:

If the user asks you to read the file yourself, or not to send it to Nutrient, do what they ask. When the user didn't
mention Nutrient, say that the file goes to their Nutrient account as you send it.

| The user asks to | Call |
| --- | --- |
| Read, transcribe or convert to Markdown, including OCR text from a scan | `parse_document` |
| Extract fields, values, line items or tables | `extract_fields`, with a short `intent` such as "Extract the invoice number, seller and total" |
| Classify documents or sort them into categories | `classify_document`, with at least two `instructions.labels` |

For a file as the result, such as a searchable PDF, a conversion, a redaction or a signature, use `process_document`,
`redact_document` or `sign_document`.

Each run uses the user's Nutrient DWS credits. For a summary of a document or a question about it, read it yourself
unless the user asks for one of the operations above. Before running more than three files, tell the user how many runs
you will start.

## Give Nutrient the file

1. If the processing tool takes `chat_file` and the user attached the file to the chat, pass it there: the app fills in
   its `download_url`, and Nutrient fetches the file from it. Never type those values yourself. If the app didn't fill
   it in, continue with the next step.
2. Otherwise, for a file attached to the chat or on disk, call `upload_documents` with its `filename`, `content_type` and
   `path`, run the command it returns exactly as returned, and pass the printed `asset_id` to the processing tool. The
   command expires within five minutes; if it has, call `upload_documents` again. Reuse an `asset_id` for further
   operations on the same file; it expires after 24 hours.
3. If that command can't run where the file is, or fails with HTTP 403 "Host not in allowlist", don't retry it. When the
   processing tool offers `attached_file`, call it once per file with the file's `filename` and `content_type` instead of
   `asset_id`: the Nutrient panel asks the user for the file and runs the call. Tell the user to add the file in the
   panel, and don't call again. Otherwise ask the user to allow `mcp.nutrient.io` in the app's network settings (in
   Claude: Settings, Capabilities, Additional allowed domains), or to share the document as an HTTPS link, which
   `document.url` takes.
4. Never paste a document as base64 to get around an upload problem.

## Read the results

- The processing call usually returns the finished run. If its status is queued or running, wait `poll_after_seconds`,
  then call `get_run` with its `run_id` until it finishes, and use `read_result` for values the response leaves out.
- Never call a processing tool again to see a result you already have. After a timeout or an `outcome_unknown` error,
  read the known run with `get_run` instead of resubmitting. Repeating an `extract_fields` call that has an `intent` but
  no `instructions.schema` fails with `idempotency_conflict`; pass a new `idempotency_key` only to run the same work
  again on purpose.
- Report what Nutrient returned, not your own reading of the file, and report its review warnings beside the values.
  A finished run doesn't prove every value is right: keep missing values unknown and identifiers as strings.
- To process several files of one kind, extract the first, then pass its schema as `instructions.schema` with the same
  `intent` for the others, so every file returns the same fields.
