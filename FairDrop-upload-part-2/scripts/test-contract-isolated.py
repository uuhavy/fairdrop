"""Fresh process per test preserves the SDK's one-contract-per-interpreter rule."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess, sys, json, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
runner=ROOT/'scripts/check-contract.py'
base=[sys.executable,'-X','utf8',str(runner)]
collected=subprocess.run([*base,'collect'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
if collected.returncode:
 print(collected.stdout,collected.stderr);raise SystemExit(collected.returncode)
nodes=[line.strip() for line in collected.stdout.splitlines() if line.startswith('tests/test_fairdrop.py::')]
if not nodes:raise RuntimeError('No contract tests collected')
reports=ROOT/'work/contract-test-reports';reports.mkdir(exist_ok=True)
def run(item):
 index,node=item
 xml=reports/f'{index:03}.xml'
 r=subprocess.run([*base,'single',node,'--junitxml='+str(xml)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
 (reports/f'{index:03}.txt').write_text(r.stdout+'\n'+r.stderr,encoding='utf-8')
 return {'test':node,'exit_code':r.returncode,'xml':str(xml),'output':r.stdout if r.returncode else ''}
results=[]
# Separate local processes, with the official SDK unchanged in each process.
with ThreadPoolExecutor(max_workers=3) as pool:
 for future in as_completed([pool.submit(run,item) for item in enumerate(nodes)]):
  r=future.result();results.append(r)
  print(('PASS ' if r['exit_code']==0 else 'FAIL ')+r['test'],flush=True)
  if r['exit_code']:print(r['output'],flush=True)
root=ET.Element('testsuites')
for r in results:
 p=Path(r['xml'])
 if p.exists():
  for suite in ET.parse(p).getroot():root.append(suite)
ET.ElementTree(root).write(ROOT/'outputs/FairDrop-contract-tests.xml',encoding='utf-8',xml_declaration=True)
summary={'total':len(results),'passed':sum(r['exit_code']==0 for r in results),'failed':sum(r['exit_code']!=0 for r in results),'mode':'Official genlayer-test Direct Mode; isolated processes; mocked LLMs','results':[{k:v for k,v in r.items() if k in ['test','exit_code']} for r in results]}
(ROOT/'outputs/FairDrop-contract-test-summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(f"RESULT: {summary['passed']}/{summary['total']} passed",flush=True)
raise SystemExit(1 if summary['failed'] else 0)
