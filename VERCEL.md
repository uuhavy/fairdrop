# Deploy FairDrop to Vercel

This repository supports a Next.js deployment on Vercel alongside its existing Sites/Vinext build. Contract addresses and on-chain campaign data do not change when the website host changes.

1. Import `uuhavy/fairdrop` at https://vercel.com/new.
2. Use the repository root (`./`) and the Next.js framework preset. The committed `vercel.json` sets the install command, Next.js build command, `.next` output and a 60-second API function limit. Do not override these with the Vinext build command.
3. Deploy. No private key, wallet seed phrase or API key is required by this application.
4. Open the actual deployment URL and append `/?contract=0xCC3382eCCF9A7aa0203B19D73232164C4d20D9c1`.
5. Check the campaign data, score, Allocation and History. Test OKX in the browser where the extension is installed; connecting to the new domain may request wallet permission again.
6. Use the verified production URL in README and the hackathon form. Do not replace the current public URL before the Vercel deployment has passed these checks.

Local equivalent of the Vercel build:

```sh
npm run install:ci
node node_modules/next/dist/bin/next build --webpack
node node_modules/next/dist/bin/next start
```

The existing `npm run build` remains the Sites/Vinext build. `tsconfig.vercel.json` checks the application separately from generated artifacts and Sites build tooling.
