import { createClient } from 'genlayer-js';
import { testnetBradbury } from 'genlayer-js/chains';
import { TransactionHashVariant } from 'genlayer-js/types';
import { CONTRACT, parseCampaign } from '@/lib/live-campaign';

export async function GET(request: Request) {
 const address = new URL(request.url).searchParams.get('address') || CONTRACT;
 if (!/^0x[0-9a-fA-F]{40}$/.test(address)) return Response.json({error:'Invalid address'},{status:400});
 let timer: ReturnType<typeof setTimeout> | undefined;
 try {
  const client = createClient({chain:testnetBradbury});
  const raw = await Promise.race([
   client.readContract({address:address as `0x${string}`,functionName:'get_campaign',args:[],transactionHashVariant:TransactionHashVariant.LATEST_NONFINAL}),
   new Promise<never>((_,reject)=>{timer=setTimeout(()=>reject(new Error('Read timeout')),25000);})
  ]);
  return Response.json(parseCampaign(raw),{headers:{'Cache-Control':'no-store'}});
 } catch(error) {
  console.error('FairDrop contract read failed',error);
  return Response.json({error:'Unable to read the Bradbury campaign. Please retry.'},{status:502,headers:{'Cache-Control':'no-store'}});
 } finally {if(timer)clearTimeout(timer);}
}
