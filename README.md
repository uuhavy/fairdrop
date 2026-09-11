# FairDrop

**Transparent AI reviews. Community contribution rewards.**

FairDrop is an AI Governance hackathon project built on GenLayer Bradbury. Organizers define an educational task, reference material and point pool. Contributors submit articles, validators evaluate them, and the campaign owner approves the final point allocation.

## Observed demo

The project owner completed deployment, submission, evaluation and approval through the English website using OKX Wallet. Screenshots show a 100/100 review and an approved 1,000-point allocation.

- Network: GenLayer Bradbury testnet (chain 4221)
- Website-created campaign: `0xd46dF8accb9346D3a5AB0ABCe06E1BCc91ACe55f`
- [Contract explorer](https://explorer-bradbury.genlayer.com/address/0xd46dF8accb9346D3a5AB0ABCe06E1BCc91ACe55f)
- Earlier Studio-created default campaign: `0xf6Bb13d8f1458bbb651744D9670F3846F5d386A2` (98/100 review)
- Public website: not published yet. Localhost is not the final submission URL.

These are observed examples, not a measured model-accuracy benchmark. Allocations are **points only**; no tokens are transferred. Reads use latest non-final state and are labeled accordingly. Campaign approval and network finalization are distinct.

## Run locally

Requires Node.js 22.13+ and npm.

```sh
npm run install:ci
npm run dev
```

Open http://localhost:5173/ or the completed website campaign at:

```text
http://localhost:5173/?contract=0xd46dF8accb9346D3a5AB0ABCe06E1BCc91ACe55f
```

Reading the campaign does not require a wallet. To create a campaign or submit an article, open the site in a browser with OKX Wallet, connect to Bradbury, and review each transaction before signing. No seed phrase or private key is used by the app.

```sh
npm run build
npx tsc --noEmit
```

## Reviewer walkthrough

1. Open the completed campaign URL above. Confirm Approved, one submission and one review.
2. Read the submission, its 50/50 accuracy, 30/30 fulfillment and 20/20 clarity scores, review reasons and evidence.
3. Open Allocation: the owner wallet has 1,000 points. Open History to inspect the stored audit trail.
4. To try a fresh campaign, connect OKX and choose Create campaign. Review the populated constructor values and deploy.
5. Check transaction result. A successful deployment selects its new address in the URL. Save that URL.
6. Submit an article, check the transaction, close submissions, evaluate, and approve the point allocation. Each write requires a wallet signature.

The app retains the pending transaction hash locally. Check its result before resending. ACCEPTED alone is not proof of execution success; the app also checks FINISHED_WITH_RETURN.

## Architecture

- `app/page.tsx`: live English campaign UI, reviews, allocation and audit history.
- `components/wallet-actions.tsx`: OKX connection, deployment, submissions and owner actions.
- `app/api/campaign/route.ts`: read-only GenLayer SDK endpoint with address and response validation.
- `lib/live-campaign.ts`: campaign response schema and default deployment.
- `contracts/fairdrop.py`: Python Intelligent Contract; `public/fairdrop.py` is the identical source used for browser deployment.
- `app/demo`: explicitly labeled browser-local prototype with fixture scores.

The web app uses React, Vinext/Vite, Radix UI, Zod and the official genlayer-js SDK. It uses no application database for campaign state.

## Contract policy

Each deployment has immutable criteria and reference material. The rubric weights accuracy 50, fulfillment 30 and clarity 20; qualification requires 60/100. There is one submission per wallet and a maximum of 50 entries.

Validators independently score the frozen content. The custom verifier requires agreement on whether review is unresolved and whether the score qualifies, with per-criterion tolerances [5,3,2]. Evidence must be exact quotes from the submission. An entry cannot be re-evaluated to shop for scores.

The owner closes submissions, evaluates entries and approves allocation. Qualifying entries share the pool with largest-remainder integer rounding and ascending ID tie breaks. Unresolved reviews block approval. The author can withdraw an unresolved entry with a reason; the owner can cancel a campaign. These two methods currently require Studio because the website does not expose them. See `contracts/POLICY.md`.

## Validation and limitations

44 isolated official SDK Direct Mode tests passed during development. These test contract behavior with controlled model outputs; they are not full network or live-model tests. TypeScript, production build, live SDK reads and website API reads have also passed. The owner manually verified one full website/OKX campaign.

Install `requirements-contract.txt` in a Python 3.12+ virtual environment, then run:

```sh
python scripts/check-contract.py lint
python scripts/check-contract.py test
```

The wrapper stores SDK artifacts in `work/genvm-cache`; first use may download a substantial runtime. See `contracts/VALIDATION.md`. The 20 cases in `tests/review-benchmark.json` remain an unrun live-model benchmark.

Limitations: no token distribution, identity verification, Sybil protection, plagiarism detection or formal appeals. Validator agreement does not guarantee truth. Explanation equivalence is not separately verified semantically. New wallets and edge cases need broader network testing. The public website and final submission assets remain pending.
