"use client";
import { useEffect, useRef } from "react";
import { flushSync } from "react-dom";
import type { Campaign, Entry } from "./fairdrop";
type Tool={name:string;description:string;inputSchema:object;annotations:object;execute:(input:unknown)=>unknown};
export function useFairdropTools(campaign:Campaign,show:(entry:Entry)=>void){
 const state=useRef({campaign,show});
 useEffect(()=>{state.current={campaign,show};},[campaign,show]);
 useEffect(()=>{
  const context=(document as Document & {modelContext?:{registerTool:(tool:Tool,options:{signal:AbortSignal})=>void|Promise<void>}}).modelContext;
  if(!context?.registerTool)return;
  const lifecycle=new AbortController();
  const register=(tool:Tool)=>{try{void Promise.resolve(context.registerTool(tool,{signal:lifecycle.signal})).catch(()=>{});}catch{/* Optional browser capability. */}};
  register({name:"read_fairdrop_campaign",description:"Read the current browser-local FairDrop prototype campaign. Sample scores are fixtures, not GenLayer decisions.",inputSchema:{type:"object",properties:{},additionalProperties:false},annotations:{readOnlyHint:true,untrustedContentHint:true},execute:()=>state.current.campaign});
  register({name:"show_fairdrop_submission",description:"Open an existing submission and its explanation in the visible review dialog. Does not evaluate or approve it.",inputSchema:{type:"object",properties:{id:{type:"string"}},required:["id"],additionalProperties:false},annotations:{readOnlyHint:false,untrustedContentHint:true},execute:(input)=>{if(!input||typeof input!=="object"||!("id" in input)||typeof input.id!=="string")throw new Error("Submission id required");const entry=state.current.campaign.entries.find(e=>e.id===(input as {id:string}).id);if(!entry)throw new Error("Submission not found");flushSync(()=>state.current.show(entry));return {id:entry.id,opened:true,sample:entry.sample};}});
  return ()=>lifecycle.abort();
 },[]);
}
