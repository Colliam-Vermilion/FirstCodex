# 实际查询附表（离线从保存材料复原）

工作线：厌氧氧响应机制。审计基准提交 `0f9eeec20bc23a421165c8cff352137ba68fac48`；本次不调用数据库。机制P06与数据P06是不同命名空间。

[详细方法](METHODS.md) · [机器可读CSV](queries_utf8.csv) · [JSON，含自动翻译/警告](queries.json) · [全部实际请求参数/URL](request_register_utf8.csv) · [原查询日志](../search_log.json)

下表是原返回，不是去重/纳入数。未显式发送排序或日期参数，不补写理想设置。辅助元数据、全文入口、项目/样本编号核验不冒充新的主题检索；完整调用另见请求表。

|ID|数据库|报告总量|实际取回|单位/截断|
|---|---|---:|---:|---|
|[P01](#query-p01)|PubMed|34|34|论文元数据；完整ID/EFetch|
|[P02](#query-p02)|PubMed|62|62|论文元数据；完整ID/EFetch|
|[P03](#query-p03)|PubMed|57|57|论文元数据；完整ID/EFetch|
|[P04](#query-p04)|PubMed|51|51|论文元数据；完整ID/EFetch|
|[P05](#query-p05)|PubMed|48|48|论文元数据；完整ID/EFetch|
|[P06](#query-p06)|PubMed|26|26|论文元数据；完整ID/EFetch|
|[P07](#query-p07)|PubMed|54|54|论文元数据；完整ID/EFetch|
|[P08](#query-p08)|PubMed|17|17|论文元数据；完整ID/EFetch|
|[P09](#query-p09)|PubMed|23|23|论文元数据；完整ID/EFetch|
|[P10](#query-p10)|PubMed|186|186|论文元数据；完整ID/EFetch|
|[P11](#query-p11)|PubMed|29|29|论文元数据；完整ID/EFetch|
|[P12](#query-p12)|PubMed|85|85|论文元数据；完整ID/EFetch|
|[P13](#query-p13)|PubMed|42|42|论文元数据；完整ID/EFetch|
|[P14](#query-p14)|PubMed|9|9|论文元数据；完整ID/EFetch|
|[C01](#query-c01)|Crossref|1162769|100|论文条目；每组仅首100，尾部未取|
|[C02](#query-c02)|Crossref|358038|100|论文条目；每组仅首100，尾部未取|
|[C03](#query-c03)|Crossref|816537|100|论文条目；每组仅首100，尾部未取|
|[O01](#query-o01)|OpenAlex|64|64|works；cursor结束，未触上限|
|[O02](#query-o02)|OpenAlex|10|10|works；cursor结束，未触上限|
|[O03](#query-o03)|OpenAlex|5|5|works；cursor结束，未触上限|
|[P15](#query-p15)|PubMed|3|3|论文元数据；完整ID/EFetch|
|[P16](#query-p16)|PubMed|5|5|论文元数据；完整ID/EFetch|
|[P17](#query-p17)|PubMed|1|1|论文元数据；完整ID/EFetch|
|[T01](#query-t01)|PubMed|4|4|指定PMID元数据，非全面早期检索|
|[F01](#query-f01)|OpenAlex|32|32|前向引文，非支持性验证|

<a id="query-p01"></a>
## P01 — methanogen oxygen tolerance

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(methanogen* AND ("oxygen exposure" OR "oxygen stress" OR "oxygen tolerance" OR aerotolerance OR "oxygen shock")) AND ("2012/01/01"[Date - Publication] : "2026/10/24"[Date - Publication])
```

字段：PubMed automatic term mapping; actual translation retained in raw ESearch。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：['pub date']。分页：ESearch retmax=9999一次完整ID；EFetch每100 ID。报告/实际：34 / 34。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "db": [
    "pubmed"
  ],
  "term": [
    "(methanogen* AND (\"oxygen exposure\" OR \"oxygen stress\" OR \"oxygen tolerance\" OR aerotolerance OR \"oxygen shock\")) AND (\"2012/01/01\"[Date - Publication] : \"2026/10/24\"[Date - Publication])"
  ],
  "retmode": [
    "json"
  ],
  "retmax": [
    "9999"
  ],
  "sort": [
    "pub date"
  ]
}
```

</details>

原始响应：[raw/pubmed/P01_search.json](../raw/pubmed/P01_search.json) · [raw/pubmed/P01_fetch_00000.xml](../raw/pubmed/P01_fetch_00000.xml)


<a id="query-p02"></a>
## P02 — oxygen detoxification enzymes

完整发送式/编号（不把数据库自动映射当原输入）：

```text
((anaerob* OR methanogen* OR Clostrid* OR Desulfovibrio) AND (rubrerythrin OR "superoxide reductase" OR flavodiiron) AND (oxygen OR oxidative)) AND ("2012/01/01"[Date - Publication] : "2026/10/24"[Date - Publication])
```

字段：PubMed automatic term mapping; actual translation retained in raw ESearch。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：['pub date']。分页：ESearch retmax=9999一次完整ID；EFetch每100 ID。报告/实际：62 / 62。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "db": [
    "pubmed"
  ],
  "term": [
    "((anaerob* OR methanogen* OR Clostrid* OR Desulfovibrio) AND (rubrerythrin OR \"superoxide reductase\" OR flavodiiron) AND (oxygen OR oxidative)) AND (\"2012/01/01\"[Date - Publication] : \"2026/10/24\"[Date - Publication])"
  ],
  "retmode": [
    "json"
  ],
  "retmax": [
    "9999"
  ],
  "sort": [
    "pub date"
  ]
}
```

</details>

原始响应：[raw/pubmed/P02_search.json](../raw/pubmed/P02_search.json) · [raw/pubmed/P02_fetch_00000.xml](../raw/pubmed/P02_fetch_00000.xml)


<a id="query-p03"></a>
## P03 — gut anaerobe exposure

完整发送式/编号（不把数据库自动映射当原输入）：

```text
((Bacteroides OR "Faecalibacterium prausnitzii" OR "Clostridioides difficile") AND ("oxygen exposure" OR aerotolerance OR "oxygen tolerance" OR "oxygen detoxification")) AND ("2012/01/01"[Date - Publication] : "2026/10/24"[Date - Publication])
```

字段：PubMed automatic term mapping; actual translation retained in raw ESearch。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：['pub date']。分页：ESearch retmax=9999一次完整ID；EFetch每100 ID。报告/实际：57 / 57。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "db": [
    "pubmed"
  ],
  "term": [
    "((Bacteroides OR \"Faecalibacterium prausnitzii\" OR \"Clostridioides difficile\") AND (\"oxygen exposure\" OR aerotolerance OR \"oxygen tolerance\" OR \"oxygen detoxification\")) AND (\"2012/01/01\"[Date - Publication] : \"2026/10/24\"[Date - Publication])"
  ],
  "retmode": [
    "json"
  ],
  "retmax": [
    "9999"
  ],
  "sort": [
    "pub date"
  ]
}
```

</details>

原始响应：[raw/pubmed/P03_search.json](../raw/pubmed/P03_search.json) · [raw/pubmed/P03_fetch_00000.xml](../raw/pubmed/P03_fetch_00000.xml)


<a id="query-p04"></a>
## P04 — syntrophic protection

完整发送式/编号（不把数据库自动映射当原输入）：

```text
((syntroph* OR "cross feeding" OR "cross-feeding" OR coculture OR "co-culture") AND (methanogen* OR anaerob*) AND (oxygen OR microoxic) AND (protect* OR scaveng* OR toleran*)) AND ("2012/01/01"[Date - Publication] : "2026/10/24"[Date - Publication])
```

字段：PubMed automatic term mapping; actual translation retained in raw ESearch。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：['pub date']。分页：ESearch retmax=9999一次完整ID；EFetch每100 ID。报告/实际：51 / 51。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "db": [
    "pubmed"
  ],
  "term": [
    "((syntroph* OR \"cross feeding\" OR \"cross-feeding\" OR coculture OR \"co-culture\") AND (methanogen* OR anaerob*) AND (oxygen OR microoxic) AND (protect* OR scaveng* OR toleran*)) AND (\"2012/01/01\"[Date - Publication] : \"2026/10/24\"[Date - Publication])"
  ],
  "retmode": [
    "json"
  ],
  "retmax": [
    "9999"
  ],
  "sort": [
    "pub date"
  ]
}
```

</details>

原始响应：[raw/pubmed/P04_search.json](../raw/pubmed/P04_search.json) · [raw/pubmed/P04_fetch_00000.xml](../raw/pubmed/P04_fetch_00000.xml)


<a id="query-p05"></a>
## P05 — spatial protection

完整发送式/编号（不把数据库自动映射当原输入）：

```text
((anaerobic OR methanogenic) AND (granul* OR biofilm OR aggregat*) AND ("oxygen gradient" OR microelectrode OR "oxygen penetration" OR "oxygen diffusion")) AND ("2012/01/01"[Date - Publication] : "2026/10/24"[Date - Publication])
```

字段：PubMed automatic term mapping; actual translation retained in raw ESearch。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：['pub date']。分页：ESearch retmax=9999一次完整ID；EFetch每100 ID。报告/实际：48 / 48。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "db": [
    "pubmed"
  ],
  "term": [
    "((anaerobic OR methanogenic) AND (granul* OR biofilm OR aggregat*) AND (\"oxygen gradient\" OR microelectrode OR \"oxygen penetration\" OR \"oxygen diffusion\")) AND (\"2012/01/01\"[Date - Publication] : \"2026/10/24\"[Date - Publication])"
  ],
  "retmode": [
    "json"
  ],
  "retmax": [
    "9999"
  ],
  "sort": [
    "pub date"
  ]
}
```

</details>

原始响应：[raw/pubmed/P05_search.json](../raw/pubmed/P05_search.json) · [raw/pubmed/P05_fetch_00000.xml](../raw/pubmed/P05_fetch_00000.xml)


<a id="query-p06"></a>
## P06 — sediment oxygen pulse

完整发送式/编号（不把数据库自动映射当原输入）：

```text
((sediment OR "waterlogged soil" OR "paddy soil") AND ("oxygen exposure" OR "oxygen pulse" OR reoxygenation OR "oxygen intrusion") AND (microb* OR methanogen* OR ferment*)) AND ("2012/01/01"[Date - Publication] : "2026/10/24"[Date - Publication])
```

字段：PubMed automatic term mapping; actual translation retained in raw ESearch。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：['pub date']。分页：ESearch retmax=9999一次完整ID；EFetch每100 ID。报告/实际：26 / 26。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "db": [
    "pubmed"
  ],
  "term": [
    "((sediment OR \"waterlogged soil\" OR \"paddy soil\") AND (\"oxygen exposure\" OR \"oxygen pulse\" OR reoxygenation OR \"oxygen intrusion\") AND (microb* OR methanogen* OR ferment*)) AND (\"2012/01/01\"[Date - Publication] : \"2026/10/24\"[Date - Publication])"
  ],
  "retmode": [
    "json"
  ],
  "retmax": [
    "9999"
  ],
  "sort": [
    "pub date"
  ]
}
```

</details>

原始响应：[raw/pubmed/P06_search.json](../raw/pubmed/P06_search.json) · [raw/pubmed/P06_fetch_00000.xml](../raw/pubmed/P06_fetch_00000.xml)


<a id="query-p07"></a>
## P07 — redox fluctuation peat wetland

完整发送式/编号（不把数据库自动映射当原输入）：

```text
((peat OR wetland OR "flooded soil") AND ("redox fluctuation" OR "redox oscillation" OR reoxygenation OR "oxygen exposure") AND (microb* OR methanogen* OR metabol*)) AND ("2012/01/01"[Date - Publication] : "2026/10/24"[Date - Publication])
```

字段：PubMed automatic term mapping; actual translation retained in raw ESearch。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：['pub date']。分页：ESearch retmax=9999一次完整ID；EFetch每100 ID。报告/实际：54 / 54。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "db": [
    "pubmed"
  ],
  "term": [
    "((peat OR wetland OR \"flooded soil\") AND (\"redox fluctuation\" OR \"redox oscillation\" OR reoxygenation OR \"oxygen exposure\") AND (microb* OR methanogen* OR metabol*)) AND (\"2012/01/01\"[Date - Publication] : \"2026/10/24\"[Date - Publication])"
  ],
  "retmode": [
    "json"
  ],
  "retmax": [
    "9999"
  ],
  "sort": [
    "pub date"
  ]
}
```

</details>

原始响应：[raw/pubmed/P07_search.json](../raw/pubmed/P07_search.json) · [raw/pubmed/P07_fetch_00000.xml](../raw/pubmed/P07_fetch_00000.xml)


<a id="query-p08"></a>
## P08 — gut oxygen metabolic response

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(("gut microbiota" OR "intestinal bacteria" OR "gut anaerobes") AND ("oxygen exposure" OR microoxic OR "oxygen tolerance") AND (metaboli* OR physiolog* OR scaveng*)) AND ("2012/01/01"[Date - Publication] : "2026/10/24"[Date - Publication])
```

字段：PubMed automatic term mapping; actual translation retained in raw ESearch。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：['pub date']。分页：ESearch retmax=9999一次完整ID；EFetch每100 ID。报告/实际：17 / 17。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "db": [
    "pubmed"
  ],
  "term": [
    "((\"gut microbiota\" OR \"intestinal bacteria\" OR \"gut anaerobes\") AND (\"oxygen exposure\" OR microoxic OR \"oxygen tolerance\") AND (metaboli* OR physiolog* OR scaveng*)) AND (\"2012/01/01\"[Date - Publication] : \"2026/10/24\"[Date - Publication])"
  ],
  "retmode": [
    "json"
  ],
  "retmax": [
    "9999"
  ],
  "sort": [
    "pub date"
  ]
}
```

</details>

原始响应：[raw/pubmed/P08_search.json](../raw/pubmed/P08_search.json) · [raw/pubmed/P08_fetch_00000.xml](../raw/pubmed/P08_fetch_00000.xml)


<a id="query-p09"></a>
## P09 — rumen scavenging

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(rumen AND ("oxygen scavenging" OR "oxygen consumption" OR "oxygen exposure" OR aerotolerance OR "oxygen tolerance")) AND ("2012/01/01"[Date - Publication] : "2026/10/24"[Date - Publication])
```

字段：PubMed automatic term mapping; actual translation retained in raw ESearch。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：['pub date']。分页：ESearch retmax=9999一次完整ID；EFetch每100 ID。报告/实际：23 / 23。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "db": [
    "pubmed"
  ],
  "term": [
    "(rumen AND (\"oxygen scavenging\" OR \"oxygen consumption\" OR \"oxygen exposure\" OR aerotolerance OR \"oxygen tolerance\")) AND (\"2012/01/01\"[Date - Publication] : \"2026/10/24\"[Date - Publication])"
  ],
  "retmode": [
    "json"
  ],
  "retmax": [
    "9999"
  ],
  "sort": [
    "pub date"
  ]
}
```

</details>

原始响应：[raw/pubmed/P09_search.json](../raw/pubmed/P09_search.json) · [raw/pubmed/P09_fetch_00000.xml](../raw/pubmed/P09_fetch_00000.xml)


<a id="query-p10"></a>
## P10 — oxygen damage sensitive enzymes

完整发送式/编号（不把数据库自动映射当原输入）：

```text
((anaerob* OR methanogen*) AND (oxygen OR superoxide) AND ("iron-sulfur" OR "enzyme inactivation" OR "pyruvate formate lyase")) AND ("2012/01/01"[Date - Publication] : "2026/10/24"[Date - Publication])
```

字段：PubMed automatic term mapping; actual translation retained in raw ESearch。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：['pub date']。分页：ESearch retmax=9999一次完整ID；EFetch每100 ID。报告/实际：186 / 186。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "db": [
    "pubmed"
  ],
  "term": [
    "((anaerob* OR methanogen*) AND (oxygen OR superoxide) AND (\"iron-sulfur\" OR \"enzyme inactivation\" OR \"pyruvate formate lyase\")) AND (\"2012/01/01\"[Date - Publication] : \"2026/10/24\"[Date - Publication])"
  ],
  "retmode": [
    "json"
  ],
  "retmax": [
    "9999"
  ],
  "sort": [
    "pub date"
  ]
}
```

</details>

原始响应：[raw/pubmed/P10_search.json](../raw/pubmed/P10_search.json) · [raw/pubmed/P10_fetch_00000.xml](../raw/pubmed/P10_fetch_00000.xml) · [raw/pubmed/P10_fetch_00100.xml](../raw/pubmed/P10_fetch_00100.xml)


<a id="query-p11"></a>
## P11 — methanogen microoxia metabolism

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(methanogen* AND (microoxic OR microaerobic OR "oxygen limitation" OR "oxygen reduction") AND (metaboli* OR transcript* OR respir* OR physiolog*)) AND ("2012/01/01"[Date - Publication] : "2026/10/24"[Date - Publication])
```

字段：PubMed automatic term mapping; actual translation retained in raw ESearch。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：['pub date']。分页：ESearch retmax=9999一次完整ID；EFetch每100 ID。报告/实际：29 / 29。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "db": [
    "pubmed"
  ],
  "term": [
    "(methanogen* AND (microoxic OR microaerobic OR \"oxygen limitation\" OR \"oxygen reduction\") AND (metaboli* OR transcript* OR respir* OR physiolog*)) AND (\"2012/01/01\"[Date - Publication] : \"2026/10/24\"[Date - Publication])"
  ],
  "retmode": [
    "json"
  ],
  "retmax": [
    "9999"
  ],
  "sort": [
    "pub date"
  ]
}
```

</details>

原始响应：[raw/pubmed/P11_search.json](../raw/pubmed/P11_search.json) · [raw/pubmed/P11_fetch_00000.xml](../raw/pubmed/P11_fetch_00000.xml)


<a id="query-p12"></a>
## P12 — recovery repeated exposure

完整发送式/编号（不把数据库自动映射当原输入）：

```text
((anaerob* OR methanogen*) AND ("oxygen shock" OR "oxygen exposure" OR "oxygen pulse" OR "intermittent aeration") AND (recover* OR adapt* OR repeated)) AND ("2012/01/01"[Date - Publication] : "2026/10/24"[Date - Publication])
```

字段：PubMed automatic term mapping; actual translation retained in raw ESearch。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：['pub date']。分页：ESearch retmax=9999一次完整ID；EFetch每100 ID。报告/实际：85 / 85。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "db": [
    "pubmed"
  ],
  "term": [
    "((anaerob* OR methanogen*) AND (\"oxygen shock\" OR \"oxygen exposure\" OR \"oxygen pulse\" OR \"intermittent aeration\") AND (recover* OR adapt* OR repeated)) AND (\"2012/01/01\"[Date - Publication] : \"2026/10/24\"[Date - Publication])"
  ],
  "retmode": [
    "json"
  ],
  "retmax": [
    "9999"
  ],
  "sort": [
    "pub date"
  ]
}
```

</details>

原始响应：[raw/pubmed/P12_search.json](../raw/pubmed/P12_search.json) · [raw/pubmed/P12_fetch_00000.xml](../raw/pubmed/P12_fetch_00000.xml)


<a id="query-p13"></a>
## P13 — AD mechanistic response

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(("anaerobic digestion" OR "methanogenic sludge") AND (microaeration OR "oxygen shock" OR "oxygen exposure") AND (microbial OR enzyme OR metabol* OR syntroph*)) AND ("2012/01/01"[Date - Publication] : "2026/10/24"[Date - Publication])
```

字段：PubMed automatic term mapping; actual translation retained in raw ESearch。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：['pub date']。分页：ESearch retmax=9999一次完整ID；EFetch每100 ID。报告/实际：42 / 42。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "db": [
    "pubmed"
  ],
  "term": [
    "((\"anaerobic digestion\" OR \"methanogenic sludge\") AND (microaeration OR \"oxygen shock\" OR \"oxygen exposure\") AND (microbial OR enzyme OR metabol* OR syntroph*)) AND (\"2012/01/01\"[Date - Publication] : \"2026/10/24\"[Date - Publication])"
  ],
  "retmode": [
    "json"
  ],
  "retmax": [
    "9999"
  ],
  "sort": [
    "pub date"
  ]
}
```

</details>

原始响应：[raw/pubmed/P13_search.json](../raw/pubmed/P13_search.json) · [raw/pubmed/P13_fetch_00000.xml](../raw/pubmed/P13_fetch_00000.xml)


<a id="query-p14"></a>
## P14 — fermenter metabolic switch

完整发送式/编号（不把数据库自动映射当原输入）：

```text
((Clostridium OR "fermentative bacteria" OR "strict anaerobes") AND (microoxic OR "oxygen exposure" OR "oxygen stress") AND (ferment* OR "electron flow" OR "redox balance")) AND ("2012/01/01"[Date - Publication] : "2026/10/24"[Date - Publication])
```

字段：PubMed automatic term mapping; actual translation retained in raw ESearch。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：['pub date']。分页：ESearch retmax=9999一次完整ID；EFetch每100 ID。报告/实际：9 / 9。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "db": [
    "pubmed"
  ],
  "term": [
    "((Clostridium OR \"fermentative bacteria\" OR \"strict anaerobes\") AND (microoxic OR \"oxygen exposure\" OR \"oxygen stress\") AND (ferment* OR \"electron flow\" OR \"redox balance\")) AND (\"2012/01/01\"[Date - Publication] : \"2026/10/24\"[Date - Publication])"
  ],
  "retmode": [
    "json"
  ],
  "retmax": [
    "9999"
  ],
  "sort": [
    "pub date"
  ]
}
```

</details>

原始响应：[raw/pubmed/P14_search.json](../raw/pubmed/P14_search.json) · [raw/pubmed/P14_fetch_00000.xml](../raw/pubmed/P14_fetch_00000.xml)


<a id="query-c01"></a>
## C01 — Crossref

完整发送式/编号（不把数据库自动映射当原输入）：

```text
methanogen oxygen exposure oxidative stress
```

字段：query.bibliographic。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：未显式指定；服务端默认，不推定固定排序。分页：仅首100；未取下一页。报告/实际：1162769 / 100。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "query.bibliographic": [
    "methanogen oxygen exposure oxidative stress"
  ],
  "filter": [
    "from-pub-date:2012-01-01,until-pub-date:2026-10-24"
  ],
  "rows": [
    "100"
  ]
}
```

</details>

未取回报告尾部：**1162669**；没有证据显示后续补齐。

原始响应：[raw/crossref/C01_search.json](../raw/crossref/C01_search.json)


<a id="query-c02"></a>
## C02 — Crossref

完整发送式/编号（不把数据库自动映射当原输入）：

```text
anaerobic oxygen tolerance rubrerythrin
```

字段：query.bibliographic。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：未显式指定；服务端默认，不推定固定排序。分页：仅首100；未取下一页。报告/实际：358038 / 100。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "query.bibliographic": [
    "anaerobic oxygen tolerance rubrerythrin"
  ],
  "filter": [
    "from-pub-date:2012-01-01,until-pub-date:2026-10-24"
  ],
  "rows": [
    "100"
  ]
}
```

</details>

未取回报告尾部：**357938**；没有证据显示后续补齐。

原始响应：[raw/crossref/C02_search.json](../raw/crossref/C02_search.json)


<a id="query-c03"></a>
## C03 — Crossref

完整发送式/编号（不把数据库自动映射当原输入）：

```text
oxygen pulse sediment microbial recovery
```

字段：query.bibliographic。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：未显式指定；服务端默认，不推定固定排序。分页：仅首100；未取下一页。报告/实际：816537 / 100。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "query.bibliographic": [
    "oxygen pulse sediment microbial recovery"
  ],
  "filter": [
    "from-pub-date:2012-01-01,until-pub-date:2026-10-24"
  ],
  "rows": [
    "100"
  ]
}
```

</details>

未取回报告尾部：**816437**；没有证据显示后续补齐。

原始响应：[raw/crossref/C03_search.json](../raw/crossref/C03_search.json)


<a id="query-o01"></a>
## O01 — OpenAlex

完整发送式/编号（不把数据库自动映射当原输入）：

```text
methanogen oxygen exposure
```

字段：title_and_abstract.search。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：未显式指定；服务端默认，不推定固定排序。分页：cursor，per-page=200；3主题有1000脚本上限，实际未触及；F01按日志终止。报告/实际：64 / 64。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "filter": [
    "from_publication_date:2012-01-01,to_publication_date:2026-10-24,title_and_abstract.search:methanogen oxygen exposure"
  ],
  "per-page": [
    "200"
  ],
  "cursor": [
    "*"
  ]
}
```

</details>

原始响应：[raw/openalex/O01_page_000.json](../raw/openalex/O01_page_000.json)


<a id="query-o02"></a>
## O02 — OpenAlex

完整发送式/编号（不把数据库自动映射当原输入）：

```text
anaerobe rubrerythrin oxygen
```

字段：title_and_abstract.search。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：未显式指定；服务端默认，不推定固定排序。分页：cursor，per-page=200；3主题有1000脚本上限，实际未触及；F01按日志终止。报告/实际：10 / 10。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "filter": [
    "from_publication_date:2012-01-01,to_publication_date:2026-10-24,title_and_abstract.search:anaerobe rubrerythrin oxygen"
  ],
  "per-page": [
    "200"
  ],
  "cursor": [
    "*"
  ]
}
```

</details>

原始响应：[raw/openalex/O02_page_000.json](../raw/openalex/O02_page_000.json)


<a id="query-o03"></a>
## O03 — OpenAlex

完整发送式/编号（不把数据库自动映射当原输入）：

```text
syntrophic oxygen protection
```

字段：title_and_abstract.search。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：未显式指定；服务端默认，不推定固定排序。分页：cursor，per-page=200；3主题有1000脚本上限，实际未触及；F01按日志终止。报告/实际：5 / 5。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "filter": [
    "from_publication_date:2012-01-01,to_publication_date:2026-10-24,title_and_abstract.search:syntrophic oxygen protection"
  ],
  "per-page": [
    "200"
  ],
  "cursor": [
    "*"
  ]
}
```

</details>

原始响应：[raw/openalex/O03_page_000.json](../raw/openalex/O03_page_000.json)


<a id="query-p15"></a>
## P15 — hit-driven expansion: PFOR direct oxygen damage

完整发送式/编号（不把数据库自动映射当原输入）：

```text
((Bacteroides OR Desulfovibrio OR anaerob*) AND (PFOR OR "pyruvate ferredoxin oxidoreductase" OR "pyruvate formate lyase") AND ("oxygen sensitivity" OR "oxygen damage" OR "oxygen exposure" OR "oxygen inactivation")) AND ("2012/01/01"[Date - Publication] : "2026/10/24"[Date - Publication])
```

字段：PubMed automatic term mapping; actual translation retained in raw ESearch。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：['pub date']。分页：ESearch retmax=9999一次完整ID；EFetch每100 ID。报告/实际：3 / 3。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "db": [
    "pubmed"
  ],
  "term": [
    "((Bacteroides OR Desulfovibrio OR anaerob*) AND (PFOR OR \"pyruvate ferredoxin oxidoreductase\" OR \"pyruvate formate lyase\") AND (\"oxygen sensitivity\" OR \"oxygen damage\" OR \"oxygen exposure\" OR \"oxygen inactivation\")) AND (\"2012/01/01\"[Date - Publication] : \"2026/10/24\"[Date - Publication])"
  ],
  "retmode": [
    "json"
  ],
  "retmax": [
    "9999"
  ],
  "sort": [
    "pub date"
  ]
}
```

</details>

原始响应：[raw/pubmed/P15_search.json](../raw/pubmed/P15_search.json) · [raw/pubmed/P15_fetch_00000.xml](../raw/pubmed/P15_fetch_00000.xml)


<a id="query-p16"></a>
## P16 — hit-driven expansion: cytochrome bd oxygen protection

完整发送式/编号（不把数据库自动映射当原输入）：

```text
((methanogen* OR "gut anaerobes" OR Akkermansia OR Proteiniphilum) AND ("cytochrome bd" OR "bd-type") AND (oxygen OR microaer*)) AND ("2012/01/01"[Date - Publication] : "2026/10/24"[Date - Publication])
```

字段：PubMed automatic term mapping; actual translation retained in raw ESearch。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：['pub date']。分页：ESearch retmax=9999一次完整ID；EFetch每100 ID。报告/实际：5 / 5。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "db": [
    "pubmed"
  ],
  "term": [
    "((methanogen* OR \"gut anaerobes\" OR Akkermansia OR Proteiniphilum) AND (\"cytochrome bd\" OR \"bd-type\") AND (oxygen OR microaer*)) AND (\"2012/01/01\"[Date - Publication] : \"2026/10/24\"[Date - Publication])"
  ],
  "retmode": [
    "json"
  ],
  "retmax": [
    "9999"
  ],
  "sort": [
    "pub date"
  ]
}
```

</details>

原始响应：[raw/pubmed/P16_search.json](../raw/pubmed/P16_search.json) · [raw/pubmed/P16_fetch_00000.xml](../raw/pubmed/P16_fetch_00000.xml)


<a id="query-p17"></a>
## P17 — hit-driven expansion: selenium redox response

完整发送式/编号（不把数据库自动映射当原输入）：

```text
((methanogen* OR "hydrogenotrophic community") AND (selenoproteome OR selenocysteine) AND ("oxidative stress" OR oxygen)) AND ("2012/01/01"[Date - Publication] : "2026/10/24"[Date - Publication])
```

字段：PubMed automatic term mapping; actual translation retained in raw ESearch。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：['pub date']。分页：ESearch retmax=9999一次完整ID；EFetch每100 ID。报告/实际：1 / 1。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "db": [
    "pubmed"
  ],
  "term": [
    "((methanogen* OR \"hydrogenotrophic community\") AND (selenoproteome OR selenocysteine) AND (\"oxidative stress\" OR oxygen)) AND (\"2012/01/01\"[Date - Publication] : \"2026/10/24\"[Date - Publication])"
  ],
  "retmode": [
    "json"
  ],
  "retmax": [
    "9999"
  ],
  "sort": [
    "pub date"
  ]
}
```

</details>

原始响应：[raw/pubmed/P17_search.json](../raw/pubmed/P17_search.json) · [raw/pubmed/P17_fetch_00000.xml](../raw/pubmed/P17_fetch_00000.xml)


<a id="query-t01"></a>
## T01 — Backward trace, selected original mechanisms from actual source references

完整发送式/编号（不把数据库自动映射当原输入）：

```text
EFetch PMID 14749831,11260473,18161989,29559534
```

字段：known PMID lookup, not keyword discovery。日期：2026-10-24。时间过滤：不设时间过滤；4个指定PMID含3篇2012年前。

排序：未显式指定；服务端默认，不推定固定排序。分页：固定4 PMID，无发现分页。报告/实际：4 / 4。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "db": [
    "pubmed"
  ],
  "id": [
    "14749831,11260473,18161989,29559534"
  ],
  "retmode": [
    "xml"
  ]
}
```

</details>

原始响应：[raw/trace/T01_fetch_00000.xml](../raw/trace/T01_fetch_00000.xml)


<a id="query-f01"></a>
## F01 — Forward citation trace from B. thetaiotaomicron 2020

完整发送式/编号（不把数据库自动映射当原输入）：

```text
cites:W3016413973,from_publication_date:2012-01-01,to_publication_date:2026-10-24
```

字段：cites filter。日期：2026-10-24。时间过滤：2012-01-01—2026-10-24。

排序：未显式指定；服务端默认，不推定固定排序。分页：cursor，per-page=200；3主题有1000脚本上限，实际未触及；F01按日志终止。报告/实际：32 / 32。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
{
  "filter": [
    "cites:W3016413973,from_publication_date:2012-01-01,to_publication_date:2026-10-24"
  ],
  "per-page": [
    "200"
  ],
  "cursor": [
    "*"
  ]
}
```

</details>

原始响应：[raw/openalex/F01_page_000.json](../raw/openalex/F01_page_000.json)

## 辅助调用与复现边界

请求附表逐条保留数据库、参数、时间、状态、响应文件；查询当日数据库会更新，重放只能复现方法，不保证未来数量相同。原主题脚本具写入/续跑行为，不应为本次文档审计直接重跑。

首20 DOI指标批量、8篇机制支持PMID及全文入口、全池31批DOI补元数据，均在请求附表并与主题查询分开；不计入1,147。未执行扩展词见[术语记录](../term_expansions.json)，尤其riboflavin、PerR、sigma B和rumen yeast不能称已新增检索。
