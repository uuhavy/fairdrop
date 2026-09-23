# FairDrop

FairDrop is an AI governance application for reviewing community contributions against a public brief and allocating campaign points after owner approval.

Website: https://fairdrop-three.vercel.app/

## Network

All live campaign reads and wallet operations use **GenLayer Studio Next**, chain ID **61997**:
- RPC: https://studio-next.genlayer.com/api
- Explorer: https://explorer-studio-dev.genlayer.com/
- Configuration: `lib/network.ts`
- Server reader: `app/api/campaign/route.ts`
- OKX connection, network guards, deployment and writes: `components/wallet-actions.tsx`

The SDK studioDevnet consensus configuration is preserved while selecting the Studio Next endpoint. Bradbury contract addresses do not migrate automatically. No Bradbury address is supplied as the default campaign.

## Run and deploy

Use Node.js 22.13 or later. Run `npm ci`, then `npx next dev -p 5173`. Production build: `npx next build --webpack`. Vercel settings are in `vercel.json`.

Deploy a new campaign through the application using OKX. The Transaction Kit panel estimates fees, shows a quote for approval, and tracks execution. Points are not GEN or token payouts; network transaction fees are separate.

After verifying a real deployment, set `NEXT_PUBLIC_CONTRACT_ADDRESS` in Vercel to its Studio Next address and redeploy. Share `https://fairdrop-three.vercel.app/?contract=YOUR_STUDIO_NEXT_ADDRESS`. The placeholder is not a deployed address.

## Verify the workflow

1. Connect OKX and create a campaign with a brief, reference material and point pool.
2. Review the fee quote and confirm deployment in OKX.
3. Submit an original article and confirm its transaction.
4. As owner, close submissions and evaluate the contribution.
5. Inspect scores, reasons and evidence; approve an eligible allocation.
6. Reload the shared campaign URL without a wallet and verify persisted results. Confirm finalization in the explorer.

## Why GenLayer

The Python Intelligent Contract stores the immutable campaign rubric, submissions, reviews and approved allocation. AI evaluates accuracy, brief fulfillment and clarity. Validators independently evaluate the meaningful scoring outcome, including qualification threshold agreement and score tolerances. Owner approval is required before deterministic point allocation. Validator agreement does not establish absolute truth.

## Limits and submission status

The migration build has passed, but deployment and end-to-end execution on Studio Next must be verified with a real wallet. Fee estimates currently use network defaults, not a measured FairDrop fee profile. The sandbox route is an illustrative local demo, not proof of a live contract.

A **real demo video is mandatory** for the hackathon. The submission is not ready until the Studio Next contract, full public workflow and video URL have been verified. See [STUDIO-NEXT.md](STUDIO-NEXT.md) for the migration checklist.
