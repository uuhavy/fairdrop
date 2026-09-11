# FairDrop — Contract validation report

Validated: 2026-09-10

## Result

- **44/44 tests passed** using the official genlayer-test Direct Mode with mocked LLM responses.
- **genvm-linter check passed**: AST checks and SDK semantic validation.
- ABI extracted successfully: 4 constructor arguments, 6 write methods, 2 read methods; no payable methods.
- Runtime release bundle checksum matched the digest published by the official GitHub release.
- Contract SHA-256: `0666809962ef2c39005708fd475095c4f039d8906dbb4f6b07ce4f6b42370af5`.

## What was verified

Complete campaign flow; owner-only actions; one submission per wallet; submission closing; state guards; duplicate evaluation prevention; cancellation and approval finality within contract state; voluntary author withdrawal of unresolved entries; malformed AI outputs; score ranges and exact source quotes; independent validator agreement and disagreement; qualification threshold disagreement; forged leader scores; leader errors; no-eligible-entry allocation; deterministic tie-breaking; and serialization of the nondeterministic closure.

Sample allocation test: scores 90, 80, 30; threshold 60; pool 1,000 -> allocations 529, 471, 0.

## Changes made

- Explicit JSON response format for the SDK LLM call.
- Malformed validator output returns disagreement.
- Clear missing-submission errors and raw text length limits.
- Proposal is available only during review or after approval.
- Author-only withdrawal for flagged submissions, preserving the review and reason.
- Owner may cancel a whole campaign with a recorded reason; cannot edit scores or selectively exclude other authors.
- Rubric and threshold exposed in the campaign snapshot.

## Tool versions and portability

Python 3.12; genlayer-test 0.29.2; genvm-linter 0.11.0; pytest 9.1.1.
GenVM bundle: v0.3.0-rc7, SHA-256 `e218a1854214681560351051f76fe2b878545cf3409455ef372d57014a88ca67`.
The contract keeps its explicit runtime dependency hash. The linter reports an informational notice that a newer runner exists; this is not a validation failure.

The helper directs SDK caches to the project workspace and runs each test in a fresh process to respect the SDK's singleton contract registry. On Windows it defers deletion of the upstream temporary stdin file. It does not replace contract execution, storage or validator comparisons. A pytest assert-rewrite warning for the already-imported gltest package is non-fatal.

## Limits — not verified yet

Direct Mode runs Python and official SDK storage abstractions in memory. It does NOT execute the full WASM/network stack. LLM responses are fixtures; tests do not measure model accuracy, prompt-injection resistance in real models, validator economics, transaction fees or network finality.

No contract is deployed to Studio or testnet yet. No deployment address or transaction link is claimed. No tokens transfer. The website still uses its separate prototype data adapter.

20 unrun benchmark articles are included for subsequent live-model evaluation. Their expectations are qualitative draft labels, not measured results.

## Next step

Deploy with the intended campaign-owner wallet on the selected GenLayer test environment, record the real contract address and deployment transaction, run a small real review campaign, then integrate the English website with wallet signing and finalized contract reads.

## Sources

- https://docs.genlayer.com/api-references/genlayer-test
- https://docs.genlayer.com/api-references/genlayer-linter
- https://github.com/genlayerlabs/genvm/releases/tag/v0.3.0-rc7
