import sys,json
sys.path.insert(0,'results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/scripts')
from online_search import get,blocked
from prepare import T,read,dump
out=[]
for sid,url in [('S03','https://link.springer.com/article/10.1007/s00253-012-4616-9'),('S04','https://www.sciencedirect.com/science/article/pii/S0301479705000988'),('S05','https://onlinelibrary.wiley.com/doi/pdf/10.1002/bit.260330612')]:
 try:
  blocked.clear();b,path=get(url,{},'Publisher',sid+'_public');out.append({'seed_key':sid,'path':path,'bytes':len(b),'status':'response saved; body must be checked'})
 except Exception as e:out.append({'seed_key':sid,'status':'failed','error':str(e)})
 dump(T/'publisher_fulltext_attempts.json',out)
