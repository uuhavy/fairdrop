# FairDrop — Studio Next migration

This source is prepared for the updated hackathon requirements. A successful build is not evidence of a deployed or verified contract.

## Network
- Studio Next, chain ID 61997
- RPC: https://studio-next.genlayer.com/api
- Explorer: https://explorer-studio-dev.genlayer.com/
- SDK 2.0.0-rc.1; Transaction Kit and React adapter 0.1.0-rc.2

The SDK studioDevnet consensus configuration is preserved with the Studio Next endpoint. Bradbury addresses and pending transactions are not reused.

## Deploy on Vercel
Upload the migration files into the existing FairDrop repository, preserving their folders. Vercel uses vercel.json. Initially leave NEXT_PUBLIC_CONTRACT_ADDRESS unset. Open the website in the browser with OKX, connect, and create a campaign. Review the live fee quote, then approve the transaction in OKX. The panel tracks the consensus result. A successful deployment selects the new address in the URL.

Set NEXT_PUBLIC_CONTRACT_ADDRESS in Vercel to that new address, then redeploy. Never use a Bradbury address as the Studio Next default.

## Fees and verification limits
The kit obtains live network prices and passes its quoted distribution and feeValue to submission. No measured developer fee profile is supplied yet: estimates use network defaults. These defaults still need validation with real FairDrop deployments, submissions, AI evaluation, and approval. Do not describe these allocations as benchmarked. The campaign pool is points, not a token transfer; network fees are separate.

The Python contract has not been redeployed or verified against Studio Next in this migration. Prior Bradbury execution does not prove compatibility. Test with the current Studio Next runner and confirm the deployed contract source before submitting.

## Required live acceptance test
1. Deploy a new campaign on Studio Next and save its address and transaction ID.
2. Submit an original article using OKX.
3. Close submissions, evaluate, and inspect scores, reasons, and quoted evidence.
4. Approve the allocation; confirm stored points and audit history.
5. Reload the public URL in another browser; confirm the same state without a wallet.
6. Confirm successful execution and network finalization in the explorer.
7. Test a poor or unresolved submission separately; verify approval guards.

## Mandatory demo video
Record the real public application: explain the task and published rubric, show OKX fee review and submission, show the AI review with evidence, then owner approval and persisted allocation. Explain why independent validators check the meaningful scoring outcome and why points are not token payouts. Upload a real video and place its URL in the Portal. The video is mandatory even if the form says optional.

Do not mark the submission ready until the live test and video are complete. Replace old Bradbury deployment links in the Portal and README with verified Studio Next links.
