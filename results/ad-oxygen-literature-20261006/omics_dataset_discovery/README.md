# 测序数据集发现与关联论文检索

已暂存机制综述进度；原omics_screening、oxygen_response_review均不修改。基准提交见baseline.json。

当前D001已完成22篇既有目标文章的可用性审计（21MG＋1MT），并访问NCBI SRA/ENA核实9个项目号。7个项目有公开群落raw reads；旧文章已关联49run，完整项目又发现2个厌氧WGS run，共51个群落候选run/48个BioSample。BioSample不等于独立生物重复。

当前明确可建立5项供氧—对照比较，来自2个项目（PRJNA1013451四项共享反应器/时间，PRJNA1287080一项）；不当5项独立研究。其他项目缺映射、匹配对照或公开run。PRJNA1013451由两篇论文复用，不重复统计。

[累计Excel](omics_dataset_discovery_cumulative.xlsx) · [项目表](data_projects_master_utf8.csv) · [样本/run映射](samples_runs_mapping_utf8.csv) · [22篇可用性审计](existing_articles_availability_audit.json) · [关联论文RIS](associated_papers.ris) · [统计](summary.json)

NCBI和ENA API本轮实际成功；GSA入口403。7项目抽检FASTQ HTTPS HEAD均被当前环境代理403拦截：可核官方文件清单，不能声称文件下载验证成功，亦不能把代理失败当作数据未公开。本轮不下载FASTQ、不重新下载论文、不代联系作者。

项目级元数据缓存、官方完整响应、请求状态/URL/时间/分页和错误独立保存。下一步在既有审计基础上，双向扩展官方项目平台及关联论文。全文方法和数据声明依据旧evidence路径/页码复用，不从零重筛原全文库。
