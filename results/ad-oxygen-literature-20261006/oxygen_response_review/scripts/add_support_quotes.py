#!/usr/bin/env python3
"""Add independently located response excerpts alongside treatment excerpts."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NEEDLES={
'32301184':'PFOR directly inactivated',
'24222618':'10-fold increase in the resistance',
'38129989':'52.0',
'25706146':'Methane production and protein content',
'36083837':'took almost 1 year',
'33326896':'Collectively, cytochrome bd oxidase and ROS defenders may play roles',
'32515155':'acetate production from oleate was higher',
'29725720':'Oxygen levels remained below the detection limit',
'37918493':'key genes associated with the reverse methanogenesis',
'25398869':'thicker cell envelope',
'37382539':'protective role of cysteine',
'38953644':'cell lysates showed superoxide scavenging activity',
'26431975':'increase in ethanol concentration and decreased acetate',
'27663027':'growth rate and yield were increased',
'33147001':'putative reactive oxygen species (ROS) scavenger genes',
'29312168':'maintained RNA transcripts',
'34409684':'up to 2000',
'38580315':'higher expression levels in the H-ORP samples',
'40057977':'decoupling of respiration',
'39608160':'sludge capacitance and electron transfer capacity',
}
def norm(t):return ' '.join(t.split())
def run():
 for f in sorted((ROOT/'decisions').glob('*.json')):
  r=json.loads(f.read_text());needle=NEEDLES[r['pmid']];s=json.loads((ROOT/'evidence_sources'/f'{r["id"]}.json').read_text());ps=[p for p in s['paragraphs'] if norm(needle).lower() in norm(p['text']).lower()]
  # Alternative wording in JATS versus PubMed/PDF. Fail rather than invent.
  alternatives={'32301184':'These data show that in aerated','40057977':'oxygen inhibits transcription activity','34409684':'2000','25706146':'methane production','32515155':'0.41','29312168':'RNA transcripts attributed to sulfide'}
  if not ps and r['pmid'] in alternatives:
   needle=alternatives[r['pmid']];ps=[p for p in s['paragraphs'] if needle.lower() in norm(p['text']).lower()]
  if not ps:raise ValueError((r['id'],needle))
  p=next((p for p in ps if '/body[' in p['locator']),ps[0]);t=norm(p['text']);start=t.lower().index(needle.lower());quote=t[max(0,start-30):min(len(t),start+len(needle)+130)]
  r['evidence'].update(additional_quote=quote,additional_quote_location=p['locator'],additional_quote_section=p['section'])
  f.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print(r['id'],p['locator'])
if __name__=='__main__':run()
