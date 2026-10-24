# 实际查询附表（离线从保存材料复原）

工作线：MG/MT数据集发现。审计基准提交 `0f9eeec20bc23a421165c8cff352137ba68fac48`；本次不调用数据库。机制P06与数据P06是不同命名空间。

[详细方法](METHODS.md) · [机器可读CSV](queries_utf8.csv) · [JSON，含自动翻译/警告](queries.json) · [全部实际请求参数/URL](request_register_utf8.csv) · [原查询日志](../search_log.json)

下表是原返回，不是去重/纳入数。未显式发送排序或日期参数，不补写理想设置。辅助元数据、全文入口、项目/样本编号核验不冒充新的主题检索；完整调用另见请求表。

|ID|数据库|报告总量|实际取回|单位/截断|
|---|---|---:|---:|---|
|[E01](#query-e01)|ENA read_run|未保存/未知|267|run，可跨查询重复|
|[E02](#query-e02)|ENA read_run|未保存/未知|36|run，可跨查询重复|
|[E03](#query-e03)|ENA read_run|未保存/未知|886|run，可跨查询重复|
|[E04](#query-e04)|ENA read_run|未保存/未知|534|run，可跨查询重复|
|[E05](#query-e05)|ENA read_run|1282|1282|run，可跨查询重复|
|[E06](#query-e06)|ENA read_run|未保存/未知|374|run，可跨查询重复|
|[E07](#query-e07)|ENA read_run|未保存/未知|74|run，可跨查询重复|
|[E08](#query-e08)|ENA read_run|未保存/未知|93|run，可跨查询重复|
|[E09](#query-e09)|ENA read_run|未保存/未知|0|run，可跨查询重复|
|[E10](#query-e10)|ENA read_run|未保存/未知|0|run，可跨查询重复|
|[E11](#query-e11)|ENA read_run|未保存/未知|0|run，可跨查询重复|
|[E12](#query-e12)|ENA read_run|未保存/未知|0|run，可跨查询重复|
|[E13](#query-e13)|ENA read_run|未保存/未知|0|run，可跨查询重复|
|[E14](#query-e14)|ENA read_run|未保存/未知|680|run，可跨查询重复|
|[E15](#query-e15)|ENA read_run|未保存/未知|0|run，可跨查询重复|
|[E16](#query-e16)|ENA read_run|未保存/未知|65|run，可跨查询重复|
|[N01](#query-n01)|NCBI bioproject|25|25|BioProject记录|
|[N02](#query-n02)|NCBI bioproject|3|3|BioProject记录|
|[N03](#query-n03)|NCBI bioproject|5|5|BioProject记录|
|[N04](#query-n04)|NCBI bioproject|1|1|BioProject记录|
|[P01](#query-p01)|NCBI pubmed|51|51|PubMed ID/论文元数据|
|[P02](#query-p02)|NCBI pubmed|31|31|PubMed ID/论文元数据|
|[P03](#query-p03)|NCBI pubmed|10|10|PubMed ID/论文元数据|
|[P04](#query-p04)|NCBI pubmed|77|77|PubMed ID/论文元数据|
|[P05](#query-p05)|NCBI pubmed|3|3|PubMed ID/论文元数据|
|[P06](#query-p06)|NCBI pubmed|2125|2125|PubMed ID/论文元数据|
|[P07](#query-p07)|NCBI pubmed|0|0|PubMed ID/论文元数据|
|[P08](#query-p08)|NCBI pubmed|1|1|PubMed ID/论文元数据|
|[GSA-availability](#query-gsa-availability)|GSA|未保存/未知|未保存/未知|未查询，不能记0|

<a id="query-e01"></a>
## E01 — ENA read_run

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(study_title="*microaer*") AND (library_source="METAGENOMIC" OR library_source="METATRANSCRIPTOMIC")
```

字段：ENA read_run: study_title，兼有library_source。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：初轮多数limit=1000/offset=0；E05修复为limit=0全量；现脚本已改，实际参数见各行。报告/实际：未保存/未知 / 267。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "result": [
      "read_run"
    ],
    "query": [
      "(study_title=\"*microaer*\") AND (library_source=\"METAGENOMIC\" OR library_source=\"METATRANSCRIPTOMIC\")"
    ],
    "fields": [
      "study_accession,secondary_study_accession,run_accession,experiment_accession,sample_accession,study_title,experiment_title,sample_alias,scientific_name,library_strategy,library_source,library_layout,base_count,fastq_ftp,fastq_bytes"
    ],
    "format": [
      "json"
    ],
    "limit": [
      "1000"
    ],
    "offset": [
      "0"
    ]
  }
]
```

</details>

原始响应：[raw/ENA/250eec1d7353263eb94715bc5fadb4b29beb9cb8119fb7b6eb46a4f1af4b64b5.body](../raw/ENA/250eec1d7353263eb94715bc5fadb4b29beb9cb8119fb7b6eb46a4f1af4b64b5.body)


<a id="query-e02"></a>
## E02 — ENA read_run

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(study_title="*microox*") AND (library_source="METAGENOMIC" OR library_source="METATRANSCRIPTOMIC")
```

字段：ENA read_run: study_title，兼有library_source。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：初轮多数limit=1000/offset=0；E05修复为limit=0全量；现脚本已改，实际参数见各行。报告/实际：未保存/未知 / 36。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "result": [
      "read_run"
    ],
    "query": [
      "(study_title=\"*microox*\") AND (library_source=\"METAGENOMIC\" OR library_source=\"METATRANSCRIPTOMIC\")"
    ],
    "fields": [
      "study_accession,secondary_study_accession,run_accession,experiment_accession,sample_accession,study_title,experiment_title,sample_alias,scientific_name,library_strategy,library_source,library_layout,base_count,fastq_ftp,fastq_bytes"
    ],
    "format": [
      "json"
    ],
    "limit": [
      "1000"
    ],
    "offset": [
      "0"
    ]
  }
]
```

</details>

原始响应：[raw/ENA/297be84d00c495fcc414286bdada8d5738536a85c720dc0382fc1f59f8c96dd9.body](../raw/ENA/297be84d00c495fcc414286bdada8d5738536a85c720dc0382fc1f59f8c96dd9.body)


<a id="query-e03"></a>
## E03 — ENA read_run

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(study_title="*oxygen*" AND (study_title="*anaerob*" OR study_title="*methan*" OR study_title="*syntroph*" OR study_title="*ferment*")) AND (library_source="METAGENOMIC" OR library_source="METATRANSCRIPTOMIC")
```

字段：ENA read_run: study_title，兼有library_source。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：初轮多数limit=1000/offset=0；E05修复为limit=0全量；现脚本已改，实际参数见各行。报告/实际：未保存/未知 / 886。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "result": [
      "read_run"
    ],
    "query": [
      "(study_title=\"*oxygen*\" AND (study_title=\"*anaerob*\" OR study_title=\"*methan*\" OR study_title=\"*syntroph*\" OR study_title=\"*ferment*\")) AND (library_source=\"METAGENOMIC\" OR library_source=\"METATRANSCRIPTOMIC\")"
    ],
    "fields": [
      "study_accession,secondary_study_accession,run_accession,experiment_accession,sample_accession,study_title,experiment_title,sample_alias,scientific_name,library_strategy,library_source,library_layout,base_count,fastq_ftp,fastq_bytes"
    ],
    "format": [
      "json"
    ],
    "limit": [
      "1000"
    ],
    "offset": [
      "0"
    ]
  }
]
```

</details>

原始响应：[raw/ENA/78e75409090f328bfacc07ae534826b3248d7c9c0887f722d3789b7ab8b8aa1f.body](../raw/ENA/78e75409090f328bfacc07ae534826b3248d7c9c0887f722d3789b7ab8b8aa1f.body)


<a id="query-e04"></a>
## E04 — ENA read_run

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(study_title="*aerat*" AND (study_title="*digest*" OR study_title="*sludge*" OR study_title="*ferment*")) AND (library_source="METAGENOMIC" OR library_source="METATRANSCRIPTOMIC")
```

字段：ENA read_run: study_title，兼有library_source。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：初轮多数limit=1000/offset=0；E05修复为limit=0全量；现脚本已改，实际参数见各行。报告/实际：未保存/未知 / 534。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "result": [
      "read_run"
    ],
    "query": [
      "(study_title=\"*aerat*\" AND (study_title=\"*digest*\" OR study_title=\"*sludge*\" OR study_title=\"*ferment*\")) AND (library_source=\"METAGENOMIC\" OR library_source=\"METATRANSCRIPTOMIC\")"
    ],
    "fields": [
      "study_accession,secondary_study_accession,run_accession,experiment_accession,sample_accession,study_title,experiment_title,sample_alias,scientific_name,library_strategy,library_source,library_layout,base_count,fastq_ftp,fastq_bytes"
    ],
    "format": [
      "json"
    ],
    "limit": [
      "1000"
    ],
    "offset": [
      "0"
    ]
  }
]
```

</details>

原始响应：[raw/ENA/3132c78c5c1b439a58b76c358af1d23b002bee4952e66aa0f539172db1693ce7.body](../raw/ENA/3132c78c5c1b439a58b76c358af1d23b002bee4952e66aa0f539172db1693ce7.body)


<a id="query-e05"></a>
## E05 — ENA read_run

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(study_title="*oxygen*" AND (study_title="*sediment*" OR study_title="*soil*" OR study_title="*peat*" OR study_title="*wetland*")) AND (library_source="METAGENOMIC" OR library_source="METATRANSCRIPTOMIC")
```

字段：ENA read_run: study_title，兼有library_source。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：初轮多数limit=1000/offset=0；E05修复为limit=0全量；现脚本已改，实际参数见各行。报告/实际：1282 / 1282。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "result": [
      "read_run"
    ],
    "query": [
      "(study_title=\"*oxygen*\" AND (study_title=\"*sediment*\" OR study_title=\"*soil*\" OR study_title=\"*peat*\" OR study_title=\"*wetland*\")) AND (library_source=\"METAGENOMIC\" OR library_source=\"METATRANSCRIPTOMIC\")"
    ],
    "fields": [
      "study_accession,secondary_study_accession,run_accession,experiment_accession,sample_accession,study_title,experiment_title,sample_alias,scientific_name,library_strategy,library_source,library_layout,base_count,fastq_ftp,fastq_bytes"
    ],
    "format": [
      "json"
    ],
    "limit": [
      "0"
    ]
  }
]
```

</details>

E05失败尝试：首1000之后offset=1000请求400，旧部分返回保留在原日志superseded_partial_attempt；本行统计只使用修复后的limit=0完整1282。

原始响应：[raw/ENA/460184746e2912bd0af1a3a01417a94365565a6b85faedb111b4597d00868c0f.body](../raw/ENA/460184746e2912bd0af1a3a01417a94365565a6b85faedb111b4597d00868c0f.body)


<a id="query-e06"></a>
## E06 — ENA read_run

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(study_title="*redox*" AND (study_title="*sediment*" OR study_title="*soil*" OR study_title="*anaerob*" OR study_title="*methan*")) AND (library_source="METAGENOMIC" OR library_source="METATRANSCRIPTOMIC")
```

字段：ENA read_run: study_title，兼有library_source。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：初轮多数limit=1000/offset=0；E05修复为limit=0全量；现脚本已改，实际参数见各行。报告/实际：未保存/未知 / 374。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "result": [
      "read_run"
    ],
    "query": [
      "(study_title=\"*redox*\" AND (study_title=\"*sediment*\" OR study_title=\"*soil*\" OR study_title=\"*anaerob*\" OR study_title=\"*methan*\")) AND (library_source=\"METAGENOMIC\" OR library_source=\"METATRANSCRIPTOMIC\")"
    ],
    "fields": [
      "study_accession,secondary_study_accession,run_accession,experiment_accession,sample_accession,study_title,experiment_title,sample_alias,scientific_name,library_strategy,library_source,library_layout,base_count,fastq_ftp,fastq_bytes"
    ],
    "format": [
      "json"
    ],
    "limit": [
      "1000"
    ],
    "offset": [
      "0"
    ]
  }
]
```

</details>

原始响应：[raw/ENA/784f7309552e7b14f0a56ffc41841d204b540e055c57b2d62ccf7b8c77beb4b6.body](../raw/ENA/784f7309552e7b14f0a56ffc41841d204b540e055c57b2d62ccf7b8c77beb4b6.body)


<a id="query-e07"></a>
## E07 — ENA read_run

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(study_title="*reoxygen*") AND (library_source="METAGENOMIC" OR library_source="METATRANSCRIPTOMIC")
```

字段：ENA read_run: study_title，兼有library_source。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：初轮多数limit=1000/offset=0；E05修复为limit=0全量；现脚本已改，实际参数见各行。报告/实际：未保存/未知 / 74。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "result": [
      "read_run"
    ],
    "query": [
      "(study_title=\"*reoxygen*\") AND (library_source=\"METAGENOMIC\" OR library_source=\"METATRANSCRIPTOMIC\")"
    ],
    "fields": [
      "study_accession,secondary_study_accession,run_accession,experiment_accession,sample_accession,study_title,experiment_title,sample_alias,scientific_name,library_strategy,library_source,library_layout,base_count,fastq_ftp,fastq_bytes"
    ],
    "format": [
      "json"
    ],
    "limit": [
      "1000"
    ],
    "offset": [
      "0"
    ]
  }
]
```

</details>

原始响应：[raw/ENA/0cf57322a21730bc9393527877af0fdd0fe23128e7f40744c8b8c42214d20f44.body](../raw/ENA/0cf57322a21730bc9393527877af0fdd0fe23128e7f40744c8b8c42214d20f44.body)


<a id="query-e08"></a>
## E08 — ENA read_run

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(study_title="*intermittent*" AND (study_title="*aerat*" OR study_title="*oxygen*")) AND (library_source="METAGENOMIC" OR library_source="METATRANSCRIPTOMIC")
```

字段：ENA read_run: study_title，兼有library_source。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：初轮多数limit=1000/offset=0；E05修复为limit=0全量；现脚本已改，实际参数见各行。报告/实际：未保存/未知 / 93。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "result": [
      "read_run"
    ],
    "query": [
      "(study_title=\"*intermittent*\" AND (study_title=\"*aerat*\" OR study_title=\"*oxygen*\")) AND (library_source=\"METAGENOMIC\" OR library_source=\"METATRANSCRIPTOMIC\")"
    ],
    "fields": [
      "study_accession,secondary_study_accession,run_accession,experiment_accession,sample_accession,study_title,experiment_title,sample_alias,scientific_name,library_strategy,library_source,library_layout,base_count,fastq_ftp,fastq_bytes"
    ],
    "format": [
      "json"
    ],
    "limit": [
      "1000"
    ],
    "offset": [
      "0"
    ]
  }
]
```

</details>

原始响应：[raw/ENA/b0b3ceb41598bf99da988ec33573a7f715a02893e6051cab76dbafa76ef6aaf1.body](../raw/ENA/b0b3ceb41598bf99da988ec33573a7f715a02893e6051cab76dbafa76ef6aaf1.body)


<a id="query-e09"></a>
## E09 — ENA read_run

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(description="*oxygen exposure*" AND (description="*anaerob*" OR description="*methan*" OR description="*sediment*")) AND (library_source="METAGENOMIC" OR library_source="METATRANSCRIPTOMIC")
```

字段：ENA read_run: study_title及/或description按实际式；description是brief sequence description，不是完整BioProject摘要。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：初轮多数limit=1000/offset=0；E05修复为limit=0全量；现脚本已改，实际参数见各行。报告/实际：未保存/未知 / 0。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "result": [
      "read_run"
    ],
    "query": [
      "(description=\"*oxygen exposure*\" AND (description=\"*anaerob*\" OR description=\"*methan*\" OR description=\"*sediment*\")) AND (library_source=\"METAGENOMIC\" OR library_source=\"METATRANSCRIPTOMIC\")"
    ],
    "fields": [
      "study_accession,secondary_study_accession,run_accession,experiment_accession,sample_accession,study_title,experiment_title,sample_alias,scientific_name,library_strategy,library_source,library_layout,base_count,fastq_ftp,fastq_bytes"
    ],
    "format": [
      "json"
    ],
    "limit": [
      "1000"
    ],
    "offset": [
      "0"
    ]
  }
]
```

</details>

原始响应：[raw/ENA/8ef903cbf6623f050dc6bdbcccee0186f82f08a8922bf2f4c8af3804602a0fda.body](../raw/ENA/8ef903cbf6623f050dc6bdbcccee0186f82f08a8922bf2f4c8af3804602a0fda.body)


<a id="query-e10"></a>
## E10 — ENA read_run

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(description="*oxygen shock*" OR description="*oxygen pulse*" OR description="*oxygen intrusion*") AND (library_source="METAGENOMIC" OR library_source="METATRANSCRIPTOMIC")
```

字段：ENA read_run: study_title及/或description按实际式；description是brief sequence description，不是完整BioProject摘要。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：初轮多数limit=1000/offset=0；E05修复为limit=0全量；现脚本已改，实际参数见各行。报告/实际：未保存/未知 / 0。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "result": [
      "read_run"
    ],
    "query": [
      "(description=\"*oxygen shock*\" OR description=\"*oxygen pulse*\" OR description=\"*oxygen intrusion*\") AND (library_source=\"METAGENOMIC\" OR library_source=\"METATRANSCRIPTOMIC\")"
    ],
    "fields": [
      "study_accession,secondary_study_accession,run_accession,experiment_accession,sample_accession,study_title,experiment_title,sample_alias,scientific_name,library_strategy,library_source,library_layout,base_count,fastq_ftp,fastq_bytes"
    ],
    "format": [
      "json"
    ],
    "limit": [
      "1000"
    ],
    "offset": [
      "0"
    ]
  }
]
```

</details>

原始响应：[raw/ENA/c996c0431f81f2ea4bfa2ad184dcef69d7a75a13756ce3960f9954995cab7518.body](../raw/ENA/c996c0431f81f2ea4bfa2ad184dcef69d7a75a13756ce3960f9954995cab7518.body)


<a id="query-e11"></a>
## E11 — ENA read_run

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(study_title="*oxygen stress*" OR description="*oxygen stress*") AND (library_source="METAGENOMIC" OR library_source="METATRANSCRIPTOMIC")
```

字段：ENA read_run: study_title及/或description按实际式；description是brief sequence description，不是完整BioProject摘要。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：初轮多数limit=1000/offset=0；E05修复为limit=0全量；现脚本已改，实际参数见各行。报告/实际：未保存/未知 / 0。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "result": [
      "read_run"
    ],
    "query": [
      "(study_title=\"*oxygen stress*\" OR description=\"*oxygen stress*\") AND (library_source=\"METAGENOMIC\" OR library_source=\"METATRANSCRIPTOMIC\")"
    ],
    "fields": [
      "study_accession,secondary_study_accession,run_accession,experiment_accession,sample_accession,study_title,experiment_title,sample_alias,scientific_name,library_strategy,library_source,library_layout,base_count,fastq_ftp,fastq_bytes"
    ],
    "format": [
      "json"
    ],
    "limit": [
      "1000"
    ],
    "offset": [
      "0"
    ]
  }
]
```

</details>

原始响应：[raw/ENA/5e2ca9387a8438abdb799f92dddab66a31c9cba3552705b96b8c6a05ce0f2239.body](../raw/ENA/5e2ca9387a8438abdb799f92dddab66a31c9cba3552705b96b8c6a05ce0f2239.body)


<a id="query-e12"></a>
## E12 — ENA read_run

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(description="*redox fluctuat*" OR description="*redox oscillat*") AND (library_source="METAGENOMIC" OR library_source="METATRANSCRIPTOMIC")
```

字段：ENA read_run: study_title及/或description按实际式；description是brief sequence description，不是完整BioProject摘要。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：初轮多数limit=1000/offset=0；E05修复为limit=0全量；现脚本已改，实际参数见各行。报告/实际：未保存/未知 / 0。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "result": [
      "read_run"
    ],
    "query": [
      "(description=\"*redox fluctuat*\" OR description=\"*redox oscillat*\") AND (library_source=\"METAGENOMIC\" OR library_source=\"METATRANSCRIPTOMIC\")"
    ],
    "fields": [
      "study_accession,secondary_study_accession,run_accession,experiment_accession,sample_accession,study_title,experiment_title,sample_alias,scientific_name,library_strategy,library_source,library_layout,base_count,fastq_ftp,fastq_bytes"
    ],
    "format": [
      "json"
    ],
    "limit": [
      "1000"
    ],
    "offset": [
      "0"
    ]
  }
]
```

</details>

原始响应：[raw/ENA/e60c51224e706a1039351c12c5e02d987767e5d3d879f45ea28799823317ba4b.body](../raw/ENA/e60c51224e706a1039351c12c5e02d987767e5d3d879f45ea28799823317ba4b.body)


<a id="query-e13"></a>
## E13 — ENA read_run

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(study_title="*side-stream*aerat*" OR description="*side-stream*aerat*") AND (library_source="METAGENOMIC" OR library_source="METATRANSCRIPTOMIC")
```

字段：ENA read_run: study_title及/或description按实际式；description是brief sequence description，不是完整BioProject摘要。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：初轮多数limit=1000/offset=0；E05修复为limit=0全量；现脚本已改，实际参数见各行。报告/实际：未保存/未知 / 0。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "result": [
      "read_run"
    ],
    "query": [
      "(study_title=\"*side-stream*aerat*\" OR description=\"*side-stream*aerat*\") AND (library_source=\"METAGENOMIC\" OR library_source=\"METATRANSCRIPTOMIC\")"
    ],
    "fields": [
      "study_accession,secondary_study_accession,run_accession,experiment_accession,sample_accession,study_title,experiment_title,sample_alias,scientific_name,library_strategy,library_source,library_layout,base_count,fastq_ftp,fastq_bytes"
    ],
    "format": [
      "json"
    ],
    "limit": [
      "1000"
    ],
    "offset": [
      "0"
    ]
  }
]
```

</details>

原始响应：[raw/ENA/0b46cab6b1b90d3b9f1093607c7b6c0b469f6fb823c514bfab6a61e391227988.body](../raw/ENA/0b46cab6b1b90d3b9f1093607c7b6c0b469f6fb823c514bfab6a61e391227988.body)


<a id="query-e14"></a>
## E14 — ENA read_run

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(study_title="*oxygen*" AND library_source="METATRANSCRIPTOMIC") AND (library_source="METAGENOMIC" OR library_source="METATRANSCRIPTOMIC")
```

字段：ENA read_run: study_title，兼有library_source。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：初轮多数limit=1000/offset=0；E05修复为limit=0全量；现脚本已改，实际参数见各行。报告/实际：未保存/未知 / 680。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "result": [
      "read_run"
    ],
    "query": [
      "(study_title=\"*oxygen*\" AND library_source=\"METATRANSCRIPTOMIC\") AND (library_source=\"METAGENOMIC\" OR library_source=\"METATRANSCRIPTOMIC\")"
    ],
    "fields": [
      "study_accession,secondary_study_accession,run_accession,experiment_accession,sample_accession,study_title,experiment_title,sample_alias,scientific_name,library_strategy,library_source,library_layout,base_count,fastq_ftp,fastq_bytes"
    ],
    "format": [
      "json"
    ],
    "limit": [
      "1000"
    ],
    "offset": [
      "0"
    ]
  }
]
```

</details>

原始响应：[raw/ENA/e18dc36942540a168d990b6bfb359f80b8228657ff407d813e60c5d1ed0f1cb2.body](../raw/ENA/e18dc36942540a168d990b6bfb359f80b8228657ff407d813e60c5d1ed0f1cb2.body)


<a id="query-e15"></a>
## E15 — ENA read_run

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(study_title="*air*nanobub*" OR study_title="*oxygen*nanobub*") AND (library_source="METAGENOMIC" OR library_source="METATRANSCRIPTOMIC")
```

字段：ENA read_run: study_title，兼有library_source。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：初轮多数limit=1000/offset=0；E05修复为limit=0全量；现脚本已改，实际参数见各行。报告/实际：未保存/未知 / 0。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "result": [
      "read_run"
    ],
    "query": [
      "(study_title=\"*air*nanobub*\" OR study_title=\"*oxygen*nanobub*\") AND (library_source=\"METAGENOMIC\" OR library_source=\"METATRANSCRIPTOMIC\")"
    ],
    "fields": [
      "study_accession,secondary_study_accession,run_accession,experiment_accession,sample_accession,study_title,experiment_title,sample_alias,scientific_name,library_strategy,library_source,library_layout,base_count,fastq_ftp,fastq_bytes"
    ],
    "format": [
      "json"
    ],
    "limit": [
      "1000"
    ],
    "offset": [
      "0"
    ]
  }
]
```

</details>

原始响应：[raw/ENA/d7ccf0fdab3eaa6a5017438fdb903a948a7a7b4700468444c3f9432951159b0a.body](../raw/ENA/d7ccf0fdab3eaa6a5017438fdb903a948a7a7b4700468444c3f9432951159b0a.body)


<a id="query-e16"></a>
## E16 — ENA read_run

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(study_title="*oxygen*" AND study_title="*recover*") AND (library_source="METAGENOMIC" OR library_source="METATRANSCRIPTOMIC")
```

字段：ENA read_run: study_title，兼有library_source。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：初轮多数limit=1000/offset=0；E05修复为limit=0全量；现脚本已改，实际参数见各行。报告/实际：未保存/未知 / 65。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "result": [
      "read_run"
    ],
    "query": [
      "(study_title=\"*oxygen*\" AND study_title=\"*recover*\") AND (library_source=\"METAGENOMIC\" OR library_source=\"METATRANSCRIPTOMIC\")"
    ],
    "fields": [
      "study_accession,secondary_study_accession,run_accession,experiment_accession,sample_accession,study_title,experiment_title,sample_alias,scientific_name,library_strategy,library_source,library_layout,base_count,fastq_ftp,fastq_bytes"
    ],
    "format": [
      "json"
    ],
    "limit": [
      "1000"
    ],
    "offset": [
      "0"
    ]
  }
]
```

</details>

原始响应：[raw/ENA/db286c5600df4f5be5b1bac12a3b936132cd371128600cf39c1345243a7be36d.body](../raw/ENA/db286c5600df4f5be5b1bac12a3b936132cd371128600cf39c1345243a7be36d.body)


<a id="query-n01"></a>
## N01 — NCBI bioproject

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(microaeration OR microaerobic OR microoxic) AND (metagenom* OR metatranscriptom*)
```

字段：NCBI BioProject默认检索字段/自动映射。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：ESearch retmax=1000，retstart逐1000；EFetch每100 ID。报告/实际：25 / 25。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "db": [
      "bioproject"
    ],
    "term": [
      "(microaeration OR microaerobic OR microoxic) AND (metagenom* OR metatranscriptom*)"
    ],
    "retmode": [
      "json"
    ],
    "retmax": [
      "1000"
    ],
    "retstart": [
      "0"
    ]
  }
]
```

</details>

原始响应：[raw/NCBI/6712f89d763994280544cdb74574fd2296051239b26782dd18f4c6dac00f94c5.body](../raw/NCBI/6712f89d763994280544cdb74574fd2296051239b26782dd18f4c6dac00f94c5.body) · [raw/NCBI/e5d6dcd9ad0f489fc3f688835f7935fa521b287de6665a0a53193b8dfe68fc7c.body](../raw/NCBI/e5d6dcd9ad0f489fc3f688835f7935fa521b287de6665a0a53193b8dfe68fc7c.body)


<a id="query-n02"></a>
## N02 — NCBI bioproject

完整发送式/编号（不把数据库自动映射当原输入）：

```text
("oxygen exposure" OR "oxygen shock" OR "oxygen pulse" OR "oxygen intrusion" OR reoxygenation) AND (anaerob* OR methanogen* OR syntroph* OR sediment OR fermentation) AND (metagenom* OR metatranscriptom*)
```

字段：NCBI BioProject默认检索字段/自动映射。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：ESearch retmax=1000，retstart逐1000；EFetch每100 ID。报告/实际：3 / 3。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "db": [
      "bioproject"
    ],
    "term": [
      "(\"oxygen exposure\" OR \"oxygen shock\" OR \"oxygen pulse\" OR \"oxygen intrusion\" OR reoxygenation) AND (anaerob* OR methanogen* OR syntroph* OR sediment OR fermentation) AND (metagenom* OR metatranscriptom*)"
    ],
    "retmode": [
      "json"
    ],
    "retmax": [
      "1000"
    ],
    "retstart": [
      "0"
    ]
  }
]
```

</details>

原始响应：[raw/NCBI/06730f51886f3e8dc78e0ad6f4c2ae23e703eee08acb70e3bc97ea39acd55086.body](../raw/NCBI/06730f51886f3e8dc78e0ad6f4c2ae23e703eee08acb70e3bc97ea39acd55086.body) · [raw/NCBI/6732d18fece6754a42cac556aa40e9e68c1b7bf72c0febb337ad3ce44ff4fff0.body](../raw/NCBI/6732d18fece6754a42cac556aa40e9e68c1b7bf72c0febb337ad3ce44ff4fff0.body)


<a id="query-n03"></a>
## N03 — NCBI bioproject

完整发送式/编号（不把数据库自动映射当原输入）：

```text
("redox fluctuation" OR "redox oscillation" OR "intermittent aeration" OR "side-stream aeration") AND (metagenom* OR metatranscriptom*)
```

字段：NCBI BioProject默认检索字段/自动映射。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：ESearch retmax=1000，retstart逐1000；EFetch每100 ID。报告/实际：5 / 5。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "db": [
      "bioproject"
    ],
    "term": [
      "(\"redox fluctuation\" OR \"redox oscillation\" OR \"intermittent aeration\" OR \"side-stream aeration\") AND (metagenom* OR metatranscriptom*)"
    ],
    "retmode": [
      "json"
    ],
    "retmax": [
      "1000"
    ],
    "retstart": [
      "0"
    ]
  }
]
```

</details>

接口警告/解释边界：
```json
{
  "warnings": {
    "phrasesignored": [],
    "quotedphrasesnotfound": [
      "\"redox oscillation\"",
      "\"side-stream aeration\""
    ],
    "outputmessages": []
  },
  "interpretation": null
}
```

原始响应：[raw/NCBI/47753d58694f85b825af56ec0a30597e5b037322145b299d1747233c3c8e8af4.body](../raw/NCBI/47753d58694f85b825af56ec0a30597e5b037322145b299d1747233c3c8e8af4.body) · [raw/NCBI/a6c3267605269b116f1c0a404d3c063ad12e992018b38119e94119119c597f39.body](../raw/NCBI/a6c3267605269b116f1c0a404d3c063ad12e992018b38119e94119119c597f39.body)


<a id="query-n04"></a>
## N04 — NCBI bioproject

完整发送式/编号（不把数据库自动映射当原输入）：

```text
oxygen AND ("anaerobic digestion" OR methanogenic OR syntrophic) AND (metatranscriptom* OR "RNA-Seq")
```

字段：NCBI BioProject默认检索字段/自动映射。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：ESearch retmax=1000，retstart逐1000；EFetch每100 ID。报告/实际：1 / 1。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "db": [
      "bioproject"
    ],
    "term": [
      "oxygen AND (\"anaerobic digestion\" OR methanogenic OR syntrophic) AND (metatranscriptom* OR \"RNA-Seq\")"
    ],
    "retmode": [
      "json"
    ],
    "retmax": [
      "1000"
    ],
    "retstart": [
      "0"
    ]
  }
]
```

</details>

原始响应：[raw/NCBI/294872d6e1445d5a8a3bcc0373f0228339fa588a33c39050952e31152e739807.body](../raw/NCBI/294872d6e1445d5a8a3bcc0373f0228339fa588a33c39050952e31152e739807.body) · [raw/NCBI/4f3c978176716630ab858dda492b7b78a0d9d2a97b774c3c6a9e785414b96020.body](../raw/NCBI/4f3c978176716630ab858dda492b7b78a0d9d2a97b774c3c6a9e785414b96020.body)


<a id="query-p01"></a>
## P01 — NCBI pubmed

完整发送式/编号（不把数据库自动映射当原输入）：

```text
(microaerat*[Title/Abstract] OR microaerob*[Title/Abstract] OR microoxic[Title/Abstract]) AND (anaerob*[Title/Abstract] OR methanogen*[Title/Abstract] OR syntroph*[Title/Abstract] OR digester*[Title/Abstract] OR fermentation[Title/Abstract]) AND (metagenom*[Title/Abstract] OR metatranscriptom*[Title/Abstract] OR shotgun[Title/Abstract])
```

字段：NCBI PubMed：显式[Title/Abstract]仅P01，其余自动映射。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：ESearch retmax=1000，retstart逐1000；EFetch每100 ID。报告/实际：51 / 51。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "db": [
      "pubmed"
    ],
    "term": [
      "(microaerat*[Title/Abstract] OR microaerob*[Title/Abstract] OR microoxic[Title/Abstract]) AND (anaerob*[Title/Abstract] OR methanogen*[Title/Abstract] OR syntroph*[Title/Abstract] OR digester*[Title/Abstract] OR fermentation[Title/Abstract]) AND (metagenom*[Title/Abstract] OR metatranscriptom*[Title/Abstract] OR shotgun[Title/Abstract])"
    ],
    "retmode": [
      "json"
    ],
    "retmax": [
      "1000"
    ],
    "retstart": [
      "0"
    ]
  }
]
```

</details>

原始响应：[raw/NCBI/a9c357c057a3f1639e00b67103f76778f4ee8d1515f87454b55a583b920f3315.body](../raw/NCBI/a9c357c057a3f1639e00b67103f76778f4ee8d1515f87454b55a583b920f3315.body) · [raw/NCBI/0ba8085ac338a9537052d09e1ca6ae3a7df54e9cb746210fe835a8ae043a4220.body](../raw/NCBI/0ba8085ac338a9537052d09e1ca6ae3a7df54e9cb746210fe835a8ae043a4220.body)


<a id="query-p02"></a>
## P02 — NCBI pubmed

完整发送式/编号（不把数据库自动映射当原输入）：

```text
("oxygen exposure" OR "oxygen shock" OR "oxygen pulse" OR "oxygen intrusion" OR "oxygen stress" OR reoxygenation) AND (anaerob* OR methanogen* OR sediment* OR ferment*) AND (metagenom* OR metatranscriptom* OR "RNA-Seq")
```

字段：NCBI PubMed：显式[Title/Abstract]仅P01，其余自动映射。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：ESearch retmax=1000，retstart逐1000；EFetch每100 ID。报告/实际：31 / 31。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "db": [
      "pubmed"
    ],
    "term": [
      "(\"oxygen exposure\" OR \"oxygen shock\" OR \"oxygen pulse\" OR \"oxygen intrusion\" OR \"oxygen stress\" OR reoxygenation) AND (anaerob* OR methanogen* OR sediment* OR ferment*) AND (metagenom* OR metatranscriptom* OR \"RNA-Seq\")"
    ],
    "retmode": [
      "json"
    ],
    "retmax": [
      "1000"
    ],
    "retstart": [
      "0"
    ]
  }
]
```

</details>

原始响应：[raw/NCBI/4754076f60dbd25e03e797fea5bdc90d4a8c132187efc0612bd25ebaf619dd9a.body](../raw/NCBI/4754076f60dbd25e03e797fea5bdc90d4a8c132187efc0612bd25ebaf619dd9a.body) · [raw/NCBI/5cfb62c91f28be865edca78302f21fa0e80f17a7e26588a2b2e9e5f225cfe595.body](../raw/NCBI/5cfb62c91f28be865edca78302f21fa0e80f17a7e26588a2b2e9e5f225cfe595.body)


<a id="query-p03"></a>
## P03 — NCBI pubmed

完整发送式/编号（不把数据库自动映射当原输入）：

```text
("redox fluctuation" OR "redox oscillation" OR "intermittent aeration" OR "side-stream aeration") AND (anaerob* OR soil OR sediment OR digester) AND (metagenom* OR metatranscriptom*)
```

字段：NCBI PubMed：显式[Title/Abstract]仅P01，其余自动映射。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：ESearch retmax=1000，retstart逐1000；EFetch每100 ID。报告/实际：10 / 10。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "db": [
      "pubmed"
    ],
    "term": [
      "(\"redox fluctuation\" OR \"redox oscillation\" OR \"intermittent aeration\" OR \"side-stream aeration\") AND (anaerob* OR soil OR sediment OR digester) AND (metagenom* OR metatranscriptom*)"
    ],
    "retmode": [
      "json"
    ],
    "retmax": [
      "1000"
    ],
    "retstart": [
      "0"
    ]
  }
]
```

</details>

接口警告/解释边界：
```json
{
  "warnings": {
    "phrasesignored": [],
    "quotedphrasesnotfound": [
      "\"side-stream aeration\""
    ],
    "outputmessages": []
  },
  "interpretation": null
}
```

原始响应：[raw/NCBI/673fef0cd551f38032dc6f0619bd1f4fd6e7941f68435732a92eefd80a9e273f.body](../raw/NCBI/673fef0cd551f38032dc6f0619bd1f4fd6e7941f68435732a92eefd80a9e273f.body) · [raw/NCBI/e1db9444f899549a17fb4c5cc9bc0e2446001465ae63e783adf14809b1442078.body](../raw/NCBI/e1db9444f899549a17fb4c5cc9bc0e2446001465ae63e783adf14809b1442078.body)


<a id="query-p04"></a>
## P04 — NCBI pubmed

完整发送式/编号（不把数据库自动映射当原输入）：

```text
oxygen AND (sediment OR wetland OR peat) AND metatranscriptom*
```

字段：NCBI PubMed：显式[Title/Abstract]仅P01，其余自动映射。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：ESearch retmax=1000，retstart逐1000；EFetch每100 ID。报告/实际：77 / 77。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "db": [
      "pubmed"
    ],
    "term": [
      "oxygen AND (sediment OR wetland OR peat) AND metatranscriptom*"
    ],
    "retmode": [
      "json"
    ],
    "retmax": [
      "1000"
    ],
    "retstart": [
      "0"
    ]
  }
]
```

</details>

原始响应：[raw/NCBI/9c5582f28bd8cc5c355ce89910690b36d75357f8c93642b1a485d9fd34dd6529.body](../raw/NCBI/9c5582f28bd8cc5c355ce89910690b36d75357f8c93642b1a485d9fd34dd6529.body) · [raw/NCBI/09d0c48cc6ebc6d90251c5374173d36b02bdb47f836cae9b0a58a2f0b4a22a35.body](../raw/NCBI/09d0c48cc6ebc6d90251c5374173d36b02bdb47f836cae9b0a58a2f0b4a22a35.body)


<a id="query-p05"></a>
## P05 — 追踪已发现项目的关联论文

完整发送式/编号（不把数据库自动映射当原输入）：

```text
"microaerophilic activated sludge"
```

字段：NCBI PubMed：显式[Title/Abstract]仅P01，其余自动映射。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：ESearch retmax=1000，retstart逐1000；EFetch每100 ID。报告/实际：3 / 3。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "db": [
      "pubmed"
    ],
    "term": [
      "\"microaerophilic activated sludge\""
    ],
    "retmode": [
      "json"
    ],
    "retmax": [
      "1000"
    ],
    "retstart": [
      "0"
    ]
  }
]
```

</details>

原始响应：[raw/NCBI/03b1de316613cadb668f505dee1a1697ea84a954102e9c87e20339d9e5a93e4c.body](../raw/NCBI/03b1de316613cadb668f505dee1a1697ea84a954102e9c87e20339d9e5a93e4c.body) · [raw/NCBI/9ef3b97e57b28c8924f3a26ee23c4422996a201664fbc4b92be610f566ef65c3.body](../raw/NCBI/9ef3b97e57b28c8924f3a26ee23c4422996a201664fbc4b92be610f566ef65c3.body)


<a id="query-p06"></a>
## P06 — 追踪已发现项目的关联论文

完整发送式/编号（不把数据库自动映射当原输入）：

```text
"Methane oxidation as a community function"
```

字段：NCBI PubMed：显式[Title/Abstract]仅P01，其余自动映射。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：ESearch retmax=1000，retstart逐1000；EFetch每100 ID。报告/实际：2125 / 2125。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "db": [
      "pubmed"
    ],
    "term": [
      "\"Methane oxidation as a community function\""
    ],
    "retmode": [
      "json"
    ],
    "retmax": [
      "1000"
    ],
    "retstart": [
      "0"
    ]
  },
  {
    "db": [
      "pubmed"
    ],
    "term": [
      "\"Methane oxidation as a community function\""
    ],
    "retmode": [
      "json"
    ],
    "retmax": [
      "1000"
    ],
    "retstart": [
      "1000"
    ]
  },
  {
    "db": [
      "pubmed"
    ],
    "term": [
      "\"Methane oxidation as a community function\""
    ],
    "retmode": [
      "json"
    ],
    "retmax": [
      "1000"
    ],
    "retstart": [
      "2000"
    ]
  }
]
```

</details>

接口警告/解释边界：
```json
{
  "warnings": {
    "phrasesignored": [],
    "quotedphrasesnotfound": [
      "\"Methane oxidation as a community function\""
    ],
    "outputmessages": []
  },
  "interpretation": "NCBI未识别引号短语，实际扩展为methane×oxidation×community×function；2125条完整保存，宽泛扩展记录不当范围筛选完成"
}
```

原始响应：[raw/NCBI/2c98c931a20b0b4b3d15e4f39bc8dd5f688650289df2230a30f730fc549d9d80.body](../raw/NCBI/2c98c931a20b0b4b3d15e4f39bc8dd5f688650289df2230a30f730fc549d9d80.body) · [raw/NCBI/d9f3bcd65e73474e62acce51cbedd8d68e5cd57267221e2ba49866e87241ea32.body](../raw/NCBI/d9f3bcd65e73474e62acce51cbedd8d68e5cd57267221e2ba49866e87241ea32.body) · [raw/NCBI/52e472823c6abb87f1bf2309cc5c1ef97056bc375601dc67ecdeee1e9a058f6b.body](../raw/NCBI/52e472823c6abb87f1bf2309cc5c1ef97056bc375601dc67ecdeee1e9a058f6b.body) · [raw/NCBI/d43039d0afe2ccb9d4c555dea349aa8356968adaaa1db4d768c116da2f19f221.body](../raw/NCBI/d43039d0afe2ccb9d4c555dea349aa8356968adaaa1db4d768c116da2f19f221.body) · [raw/NCBI/31ab5a976080115ea29f83b50c86efd3f14ea04cd5102be9a88b2a63f1e0c533.body](../raw/NCBI/31ab5a976080115ea29f83b50c86efd3f14ea04cd5102be9a88b2a63f1e0c533.body) · [raw/NCBI/601e12c2dddf72b1874601005320ef6e1dd71c04bec794b19c77afe5b04fa217.body](../raw/NCBI/601e12c2dddf72b1874601005320ef6e1dd71c04bec794b19c77afe5b04fa217.body) · [raw/NCBI/863e1adc64fc7079316bfb5f12b86c02fb0085e72978511e95d4520981794eb8.body](../raw/NCBI/863e1adc64fc7079316bfb5f12b86c02fb0085e72978511e95d4520981794eb8.body) · [raw/NCBI/7db6f217d12112e5589349cf649d665a207407bdb46b0b92679ee3fe80fc6ddf.body](../raw/NCBI/7db6f217d12112e5589349cf649d665a207407bdb46b0b92679ee3fe80fc6ddf.body) · [raw/NCBI/53267a1d9c5e1e34ac01c7dff77ef0253a34e9bf5006ccb587fd0728e86737df.body](../raw/NCBI/53267a1d9c5e1e34ac01c7dff77ef0253a34e9bf5006ccb587fd0728e86737df.body) · [raw/NCBI/378d365ad71f3f2371c3f0892719672996e17336660d845340c118545d6c9a47.body](../raw/NCBI/378d365ad71f3f2371c3f0892719672996e17336660d845340c118545d6c9a47.body) · [raw/NCBI/4c7b9de88dc3c2b30f7806e60e8ba11074b3948ba15c7089ac42c3b2eb226dd9.body](../raw/NCBI/4c7b9de88dc3c2b30f7806e60e8ba11074b3948ba15c7089ac42c3b2eb226dd9.body) · [raw/NCBI/e007918e0d5bc6d6e063a10a3a00bae1272c760eb9d5814d8febb4170fa936a2.body](../raw/NCBI/e007918e0d5bc6d6e063a10a3a00bae1272c760eb9d5814d8febb4170fa936a2.body) · [raw/NCBI/36328184af1a8747e4473dc767f2753f5f61f250c369017f68b452c5d63ba90a.body](../raw/NCBI/36328184af1a8747e4473dc767f2753f5f61f250c369017f68b452c5d63ba90a.body) · [raw/NCBI/5434c258f8cfc2645860272d72a03fc556079e55482b49f9755b57a6ed88ab2e.body](../raw/NCBI/5434c258f8cfc2645860272d72a03fc556079e55482b49f9755b57a6ed88ab2e.body) · [raw/NCBI/b5dbc4b11c758bb5d06e74bee57013575c71abc050719a9ad3c0be79fe25a327.body](../raw/NCBI/b5dbc4b11c758bb5d06e74bee57013575c71abc050719a9ad3c0be79fe25a327.body) · [raw/NCBI/e166bfe4cd7869ec8a1ec5334e976cbb79eb0000a28977d529a4b257b2903f1c.body](../raw/NCBI/e166bfe4cd7869ec8a1ec5334e976cbb79eb0000a28977d529a4b257b2903f1c.body) · [raw/NCBI/9f0afb58872cb4fe7e3ed1114c3a4673bdf15aad570f05eed0c85abd969489db.body](../raw/NCBI/9f0afb58872cb4fe7e3ed1114c3a4673bdf15aad570f05eed0c85abd969489db.body) · [raw/NCBI/1986329a541e64ec6ec832c62ee17bee05ca3f6c784fb52bd53d2341f1a1f8d9.body](../raw/NCBI/1986329a541e64ec6ec832c62ee17bee05ca3f6c784fb52bd53d2341f1a1f8d9.body) · [raw/NCBI/0f5aa9393cb001be9b43ebc00fa6dbd5ef008f8325893561d1771591c5588295.body](../raw/NCBI/0f5aa9393cb001be9b43ebc00fa6dbd5ef008f8325893561d1771591c5588295.body) · [raw/NCBI/4a15f72ee4b0c825158c071d117d51c715121b711fb8ffc8dab8f150fb161feb.body](../raw/NCBI/4a15f72ee4b0c825158c071d117d51c715121b711fb8ffc8dab8f150fb161feb.body) · [raw/NCBI/c9eebf9127a809d7210a2b464902c8437a9296f95429f104f93a853a509ff669.body](../raw/NCBI/c9eebf9127a809d7210a2b464902c8437a9296f95429f104f93a853a509ff669.body) · [raw/NCBI/9b400e063fe3ee851bf45cabca119d2e9e8b30c0b7402341643c02a3ea232a44.body](../raw/NCBI/9b400e063fe3ee851bf45cabca119d2e9e8b30c0b7402341643c02a3ea232a44.body) · [raw/NCBI/cfc7af329ca2b6a6948e25003e2b6ddc6f91b2e2dc3e867e63108f407191f658.body](../raw/NCBI/cfc7af329ca2b6a6948e25003e2b6ddc6f91b2e2dc3e867e63108f407191f658.body) · [raw/NCBI/19425513fa3b5b061d69bb65bc25087c4ecbb124ff7c568573cc28087715120e.body](../raw/NCBI/19425513fa3b5b061d69bb65bc25087c4ecbb124ff7c568573cc28087715120e.body) · [raw/NCBI/de1a958f6f96347bafd90ce89139b1a80c444c81a8cbe2d36031d8295bb350fc.body](../raw/NCBI/de1a958f6f96347bafd90ce89139b1a80c444c81a8cbe2d36031d8295bb350fc.body)


<a id="query-p07"></a>
## P07 — 追踪已发现项目的关联论文

完整发送式/编号（不把数据库自动映射当原输入）：

```text
"Transcriptome-SIP"
```

字段：NCBI PubMed：显式[Title/Abstract]仅P01，其余自动映射。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：ESearch retmax=1000，retstart逐1000；EFetch每100 ID。报告/实际：0 / 0。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "db": [
      "pubmed"
    ],
    "term": [
      "\"Transcriptome-SIP\""
    ],
    "retmode": [
      "json"
    ],
    "retmax": [
      "1000"
    ],
    "retstart": [
      "0"
    ]
  }
]
```

</details>

接口警告/解释边界：
```json
{
  "warnings": {
    "phrasesignored": [],
    "quotedphrasesnotfound": [
      "\"Transcriptome-SIP\""
    ],
    "outputmessages": [
      "No items found."
    ]
  },
  "interpretation": null
}
```

原始响应：[raw/NCBI/ff637d728136cd55f5319fdf4b523dcc0b96b9e98a424069580c60c2414ba92b.body](../raw/NCBI/ff637d728136cd55f5319fdf4b523dcc0b96b9e98a424069580c60c2414ba92b.body)


<a id="query-p08"></a>
## P08 — 追踪已发现项目的关联论文

完整发送式/编号（不把数据库自动映射当原输入）：

```text
"Intermittent Oxygen Supply" AND "Trichloroethene"
```

字段：NCBI PubMed：显式[Title/Abstract]仅P01，其余自动映射。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：ESearch retmax=1000，retstart逐1000；EFetch每100 ID。报告/实际：1 / 1。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[
  {
    "db": [
      "pubmed"
    ],
    "term": [
      "\"Intermittent Oxygen Supply\" AND \"Trichloroethene\""
    ],
    "retmode": [
      "json"
    ],
    "retmax": [
      "1000"
    ],
    "retstart": [
      "0"
    ]
  }
]
```

</details>

接口警告/解释边界：
```json
{
  "warnings": {
    "phrasesignored": [],
    "quotedphrasesnotfound": [
      "\"Intermittent Oxygen Supply\""
    ],
    "outputmessages": []
  },
  "interpretation": null
}
```

原始响应：[raw/NCBI/0782a04599f5622c960eec619f6c2d2a122424021b08895071d6c7296370dc44.body](../raw/NCBI/0782a04599f5622c960eec619f6c2d2a122424021b08895071d6c7296370dc44.body) · [raw/NCBI/6d142984126f272173a3951d6e16ea510ac421991cbb19c4a7c43d73cb82f97f.body](../raw/NCBI/6d142984126f272173a3951d6e16ea510ac421991cbb19c4a7c43d73cb82f97f.body)


<a id="query-gsa-availability"></a>
## GSA-availability — GSA

完整发送式/编号（不把数据库自动映射当原输入）：

```text
未执行数据库检索；仅GSA入口测试
```

字段：不适用。日期：2026-10-24。时间过滤：未发送发表/提交日期过滤。

排序：未显式指定；服务端默认。分页：未执行。报告/实际：未保存/未知 / 未保存/未知。

<details><summary>保存的请求参数（包括实际分页）</summary>

```json
[]
```

</details>

原始响应：[raw/GSA/c718d2bbdeae064bd679e23dac7323bf82630547c44b43f3585e1925035d17e7.body](../raw/GSA/c718d2bbdeae064bd679e23dac7323bf82630547c44b43f3585e1925035d17e7.body)

## 辅助调用与复现边界

请求附表逐条保留数据库、参数、时间、状态、响应文件；查询当日数据库会更新，重放只能复现方法，不保证未来数量相同。原主题脚本具写入/续跑行为，不应为本次文档审计直接重跑。

逐项目SRA精确编号ESearch（retmax=200，每200分页）及EFetch（每100）、ENA filereport、PubMed→SRA ELink/UID ESummary、BioProject Publication反查、3个Assembly编号查询都列于请求附表；它们是编号核验/关联或派生数据核验，不是同一组广泛主题检索。GSA没有实际查询。
