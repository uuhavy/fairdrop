# FairDrop contract policy v1

One deployment represents one campaign. This contract records demo points, not token balances.

## Lifecycle

`open -> review -> approved`

The owner can cancel an open or reviewing campaign, producing a terminal `cancelled` state.

- Deploy with a title, brief, reference text and pool (1–1,000,000).
- Criteria are fixed: accuracy 50, fulfillment 30, clarity 20; minimum score 60.
- Each wallet may submit once. Maximum 50 submissions. Article body: 50 characters after trimming leading/trailing whitespace minimum, 12,000 raw characters maximum.
- The owner closes submissions before grading. Articles and reference text cannot be edited.
- The owner requests one evaluation per article. Each validator independently scores the frozen inputs.
- Qualification and needs-review status must agree exactly. Criterion tolerances: 5, 3 and 2 points.
- Allocation uses largest remainders, ties by ascending wallet ID. Only eligible entries share the pool.
- Owner approval freezes the allocation. If nobody qualifies, the entire pool remains unallocated.

## Ambiguous results

An unscored or needs-review article blocks approval. The owner cannot overwrite scores or selectively exclude another author's article.

Only the author of a needs-review article may call `withdraw_unresolved(reason)`. This makes the article ineligible but preserves its body, review and reason in history. This is a voluntary opt-out, NOT an appeal or a corrected score.

If the author does not withdraw, the owner can cancel the entire campaign with a public reason, then create a new campaign with clearer reference material. No tokens are moved or locked by this prototype. This policy trades availability for protection from unilateral score changes; wallet inactivity can block completion.

## Public write methods

- submit(title, body): author wallet; phase open.
- close_submissions(): owner; open, at least one entry.
- evaluate(submission_id): owner; review, unreviewed active entry.
- withdraw_unresolved(reason): flagged entry's author; review.
- approve(): owner; review with all active reviews resolved.
- cancel(reason): owner; open or review.

## Public read methods

- get_campaign(): JSON snapshot including owner, phase, rubric, entries, allocation and audit.
- proposal(): JSON allocation during review; frozen allocation after approval. Refuses unresolved active reviews.

## Security and limits

- Prompts treat submitted text and embedded instructions as data. This reduces exposure but is not proof of prompt-injection resistance.
- JSON structure, integer ranges, decision type, explanation lengths and exact quoted evidence are validated.
- Validators independently re-score; numeric agreement alone does not independently establish every sentence of the stored explanation.
- Direct-mode tests use mocked LLM responses. They validate code and comparison rules, not real model quality or network consensus/finality.
- One submission per wallet is not one submission per human. No Sybil or plagiarism guarantees.
- The owner controls when evaluation and approval occur. This is an administrator-governed MVP, not token-voting governance.
- Deployment to a live network and UI integration remain separate milestones.

## Reproduce locally

Create a Python 3.12+ virtual environment and install requirements-contract.txt.

`python scripts/check-contract.py lint`

`python scripts/check-contract.py test`

The helper uses the official SDK and test fixtures. Cache files live in `work/genvm-cache`. Each test runs in a fresh process to respect the SDK singleton contract registry. On Windows, cleanup of the upstream temporary stdin file is deferred until it can be closed. Contract execution, storage, LLM mock matching and validator comparisons are not replaced. The first run needs network access for the official GenVM release bundle.
