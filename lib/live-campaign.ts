import { z } from 'zod';
export const CONTRACT = process.env.NEXT_PUBLIC_CONTRACT_ADDRESS || '';
export const EXPLORER = `https://explorer-studio-dev.genlayer.com/address/${CONTRACT}`;
const address = z.string().regex(/^0x[0-9a-fA-F]{40}$/);
const review = z.object({scores: z.tuple([z.number().int().min(0).max(50),z.number().int().min(0).max(30),z.number().int().min(0).max(20)]), reasons:z.array(z.string()).length(3), evidence:z.array(z.string()), needs_review:z.boolean()});
export const campaignSchema = z.object({
 title:z.string(), brief:z.string(), reference:z.string(), pool:z.number().int().min(1).max(1000000),
 phase:z.enum(['open','review','approved','cancelled']), owner:address, rubric_version:z.literal(1),
 weights:z.tuple([z.literal(50),z.literal(30),z.literal(20)]), threshold:z.literal(60),
 entries:z.array(z.object({id:address,title:z.string(),body:z.string(),review:review.nullable(),withdrawn:z.boolean()})),
 allocations:z.record(z.string(),z.number().int().nonnegative()),audit:z.array(z.string())
});
export type LiveCampaign = z.infer<typeof campaignSchema>;
export function parseCampaign(raw:unknown):LiveCampaign {return campaignSchema.parse(typeof raw==='string'?JSON.parse(raw):raw);}
