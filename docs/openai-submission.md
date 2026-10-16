# OpenAI submission handoff

This extends Oli's existing package. Check its current draft in [OpenAI Plugins](https://platform.openai.com/plugins)
before uploading; submission status has not been inspected. No application, deployment or legal acceptance was performed.

## Build and verify

```sh
python3 ci/check.py
claude plugin validate ./plugins/nutrient
python3 -m unittest discover -s ci -p 'test_*.py' -v
python3 ci/package_openai.py
```

Candidate: `dist/nutrient-openai-1.0.1.zip`; the builder prints its SHA-256. Only six reviewed files are packaged at one
root. Private files and local app mappings are excluded, symlinks rejected, and referenced resources checked. Tests
cover credential fields/headers, app mappings, annotation types and reproducibility. This is not a general secret detector.
The ZIP stays out of Git. Reproducibility assumes the same Python/zlib environment.

OpenAI still supports this Codex layout (`.codex-plugin/plugin.json`, `.mcp.json`). The current portable schemas were
fetched for comparison; they do not validate this legacy format. Root `plugin.json`/`mcp.json` are recommended for new
packages, but migration is unnecessary here. The portable MCP schema currently rejects server extensions that OpenAI's
OAuth guide documents. Resolve that discrepancy with OpenAI before migrating; don't silently remove authentication.

The existing connection uses OAuth discovery, with no embedded credentials, fixed headers or authentication overrides.
The public portal supports OAuth, mixed and no-auth connections, not an API-key setup flow. Do not switch this protected
service to no-auth.

## Checked on 16 October 2026

| Evidence | Result / limit |
| --- | --- |
| Repository | Its instructions identify this package; Oli's [merged ChatGPT fix](https://github.com/PSPDFKit/PSPDFKit/pull/60270) references it. [Earlier directory work](https://github.com/PSPDFKit/PSPDFKit/pull/60047) is merged. No second package was created. |
| Local checks | Listing limits, required URLs, existing logo, five positive/three negative cases and both catalogs pass. Claude validation and an isolated Codex marketplace install pass. These are not portal or conversation tests. |
| Public URLs | Setup, product, privacy, terms, support and all three PDF fixtures returned HTTP 200. Reachability does not establish legal coverage. |
| Transport | Unauthenticated POST initialize returned 401 with a Bearer challenge naming `https://mcp.nutrient.io/.well-known/oauth-protected-resource/mcp`. GET `/mcp` returned 405, allowing POST. |
| Discovery | Resource metadata names the exact endpoint and `https://api.nutrient.io`. Authorization metadata advertises DCR, PKCE S256 and refresh. No registration or sign-in was attempted. |
| Catalogs | Base `f624c7c83c116204fe25b2078dbf27c4790013fc` records release-build-14 snapshots: 13 Apps-client tools, nine ChatGPT tools, all with explicit boolean hints. No authenticated production scan was run. |
| Host routing | Hosted README/`ToolFilters.cs` confirm ChatGPT hides local-file tools. The skill now avoids calling them, including its upload fallback. Live behavior remains untested. |

## Submission blockers

| Owner | Next step |
| --- | --- |
| Oli / OpenAI org owner | Confirm existing draft, global-residency project, Nutrient business verification and Apps Management Write. Complete the portal's domain challenge without replacing another plugin's token. Statuses unknown. |
| DWS account owner | Supply an approved sample-data reviewer account with credits, entitlements and Viewer region ready. It must work without MFA, codes, magic links or private-network hurdles. Do not weaken an existing account. Enter credentials only in the secure portal, never Git/ZIP. |
| Demo owner | Record OAuth, attached PDF, finished result, page evidence and usage in ChatGPT. Add the accessible `review.demo_recording_url` once real; it is absent. Keep secrets out of the recording. |
| Product / privacy / security | Resolve prohibited PHI, PCI data, government identifiers and authentication secrets. Establish reviewed input/processing safeguards or narrow the service surface; a skill instruction alone is insufficient. Verify retention, subprocessors, logging and Viewer copies against public disclosures. |
| Service owner | Test OAuth registration, PKCE, exact redirects, issuer/audience/expiry/scopes, refresh, revocation and wrong-account/tenant boundaries. Test the actual ChatGPT listing, panel domain/CSP, CORS and downloads with the reviewer account. |
| Oli | Scan skills/tools, resolve findings, check country availability, commerce and attestations, then submit only after owner review. None of those portal actions was performed here. |

The public [setup page](https://www.nutrient.io/mcp/) links to a legacy local-server guide promoting SSN, PHI and PCI
examples. Product/website owners should review those claims for ChatGPT. Hosted fixes belong in
`PSPDFKit/PSPDFKit/hosted-mcp` with its HTTP tests; website changes and production promotion remain separate owner work.

## Live review cases

Keep the existing manifest's five positive and three negative cases. Expected behaviors are targets, not audit results.
Record tools, arguments, outcomes, confirmations and redacted evidence with package SHA and production version.

| Case | Verify |
| --- | --- |
| Invoice URL / `extract_fields` | Fixture values, citations and page highlights agree. |
| Attached menu / `parse_document` | Real `chat_file`, no second upload or invented URL; Markdown and panel load. |
| Contract / `classify_document` | Requested label and confidence come from Nutrient. |
| Invoice / `generate_schema` | Schema only; no extraction or stored run. |
| Credits / `get_account_usage` | Reviewer account's current usage only. |
| Coffee names; delete documents; write agreement | No Nutrient call or implied unsupported action. |

Also test missing attachment metadata (ask for an HTTPS link, not an unlisted upload tool), explicit refusal to send data
to Nutrient, low credits, pending-run continuation without resubmission and adversarial document text. Review restricted-data
requests with synthetic placeholders, never actual restricted data. Results remain pending.

## Annotation notes for review

Parse/extract/classify queue work and retain artifacts: read-only is false. Arbitrary document URLs make open-world true.
Their additive/non-destructive claim needs confirmation against all modes and billing effects. Schema generation is
marked read-only because source documents no retained run or charge, but remains open-world. Account/run/result/job reads
and Studio links are bounded-account reads. Review's Viewer copy is a separate persisted artifact: check app-only writes too.

ChatGPT hides Processor/signing/redaction tools but the service leaves them callable for older panels. Confirm the scan
reviews that surface; hiding a tool does not establish compliance. Do not hand-edit snapshots to clear a finding.
Guidelines say annotation justifications are no longer required; the review page still discusses them. Keep factual
explanations ready and check the actual portal.

Sources: [submission / field limits](https://developers.openai.com/plugins/deploy/submission),
[review requirements](https://developers.openai.com/plugins/deploy/app-review),
[package guide](https://developers.openai.com/plugins/build/plugins),
[MCP server guide](https://developers.openai.com/plugins/build/mcp-server),
[guidelines](https://developers.openai.com/plugins/plugin-guidelines),
[portable manifest schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json),
[portable MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json). Recheck before upload.
