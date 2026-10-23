"""Locate terms in SHA-bound parsed pages. Hits never determine a screening conclusion."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PATTERNS={
 'target_terms':r'metagenom\w*|metatranscriptom\w*|shotgun|\bRNA[ -]?seq(?:uencing)?\b|whole[ -]communit\w*.{0,30}(?:DNA|RNA)|宏基因组|宏转录组|鸟枪法|群落.{0,12}(?:DNA|RNA|转录组)',
 'non_target_or_molecular_context':r'\b(?:16S|18S|ITS|amplicon|DGGE|qPCR|RT[ -]?qPCR|PICRUSt\w*|Tax4Fun\w*|DNA|RNA|sequenc\w*|Illumina|MiSeq)\b|扩增子|引物|核酸提取|测序|高通量|功能预测',
 'data_statement':r'accession\w*|deposited|data availab\w*|upon request|on request|available.{0,30}request|BioProject|SRA|ENA|DDBJ|MG[ -]RAST|GEO|GSA|\bPRJ(?:NA|EB|DB|CA)\d+|\b[SED][RAX][RSPX]\d+|\bGSE\d+|数据.{0,12}(?:获取|索取|公开|存储)|项目号|登录号|序列号'
}
def main():
    out=[]
    paths=sorted((ROOT/'parsed').glob('*.json'))+sorted((ROOT/'parsed_attachments').glob('*.json'))
    for path in paths:
        obj=json.loads(path.read_text());hits=[]
        pages=obj.get('pages') or [{'pdf_page':None,'text':t,'location':f'DOCX paragraph {i+1}'} for i,t in enumerate(obj.get('paragraphs',[]))]
        for page in pages:
            for kind,pattern in PATTERNS.items():
                for m in re.finditer(pattern,page['text'],re.I):
                    hits.append({'kind':kind,'pdf_page':page['pdf_page'],'location':page.get('location',''),'term':m.group(),'context':page['text'][max(0,m.start()-180):m.end()+350]})
        out.append({'record_id':obj['record_id'],'source_path':obj['source_path'],'source_sha256':obj['source_sha256'],'patterns':PATTERNS,'hits':hits,'note':'定位工具；无命中仍须阅读完整方法，不能据此自动分类。'})
    (ROOT/'term_location_log.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print([(o['record_id'],len(o['hits']),sum(h['kind']=='target_terms' for h in o['hits'])) for o in out])
if __name__=='__main__':main()
