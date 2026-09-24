# FairDrop Studio Next deployment fix

Confirmed failed transaction: `0x7533afd42df9923ab92314fc8404b3cd2ccc8b1a2ae8f24180757b48a811a704`.
The network returned `FINISHED_WITH_ERROR`; the leader reported `invalid_contract runner malformed`.

Changes:
- Pin the Python runner shipped in Studio v0.123.0-rc.7 and GenVM v0.6.0-rc5.
- Migrate imports, Contract/storage namespaces and the non-deterministic API.
- Reject malformed validator replies under the new exception type.
- Include Transaction Kit CSS and clear pending state from the completed tracking result, including execution failure.
- Pin updated local test tools. The mock adapter preserves the new SDK's raw-text LLM envelope; it does not alter scoring or validator logic.

Upload the changed files with their folder structure. Both contracts/fairdrop.py and public/fairdrop.py are required. Wait for Vercel Ready, refresh the page, connect OKX and use Check transaction result once to clear the old failed transaction. Then create a new campaign with the updated source. Save its URL and transaction ID for verification.

Local mocked tests do not verify live LLM consensus or real fee sufficiency. A successful Studio Next deployment and public end-to-end workflow are still required before resubmission, together with the mandatory demo video.

Validation: 44/44 official Direct Mode tests passed with mocked LLMs; contract lint/schema validation passed; Next.js production build and TypeScript passed. Runtime source: https://github.com/genlayerlabs/genlayer-studio/blob/v0.123.0-rc.7/examples/contracts/_hello_world.py
