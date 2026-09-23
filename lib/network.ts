import { studioDevnet } from 'genlayer-js/chains';
export const STUDIO_NEXT = {
 ...studioDevnet, id: 61997, name: 'GenLayer Studio Next',
 rpcUrls: { default: { http: ['https://studio-next.genlayer.com/api'] } },
 blockExplorers: { default: { name: 'GenLayer Explorer', url: 'https://explorer-studio-dev.genlayer.com' } },
};
