# 方法审计及README恢复记录

2026-10-25先从保存材料重建了两条扩展工作线的方法，随后按用户要求恢复全项目介绍：**主体方法不整体折叠、不用最新任务替代前面阶段。** 原文献数据、分类、人工判断、原件、累计表和进度均不因文档变更而修改。

## 当前研究介绍

[完整项目七阶段](../README.md) · [仓库入口](../../../README.md) · [章节恢复对照](readme_restoration/chapter_map.md) · [旧成果路径索引](readme_restoration/source_link_index.md) · [运行历史附录](../HISTORY.md) · [本次恢复校验](readme_restoration/validation.json)

最初AD检索和校正用methods/01–11，原件/JCR以方法21及各自清单说明，MG/MT全文筛查保留B001–B010；两条扩展线继续用下列已补充的方法。历史数字注明阶段，不移除主体研究介绍。

## 上轮方法审计成果保持

- [机制详细方法](../oxygen_response_review/methods/METHODS.md) · [机制检索附表](../oxygen_response_review/methods/QUERY_APPENDIX.md)
- [数据详细方法](../omics_dataset_discovery/methods/METHODS.md) · [数据检索附表](../omics_dataset_discovery/methods/QUERY_APPENDIX.md)
- [离线集合审计](audit_summary.json) · [阶段提交快照](stage_history.json) · [上轮校验](validation.json) · [上轮9文档独立读回](remote_readback.json)

上轮明确了Europe PMC旧摘要与后续3次成功正文并存、原17范围与原17推荐不完全同集、原2228论文队列漏排12篇旧22已审计记录。Crossref尾部、未保存的模型输入/选择细节、未核独立支持和文件传输限制继续保留。本次不重写原队列或筛选来掩盖这些问题。

## 离线命令及避免再次覆盖首页

从仓库根目录：

```bash
python results/ad-oxygen-literature-20261006/method_audit/validate.py
python results/ad-oxygen-literature-20261006/method_audit/update_readme_navigation.py
```

validate.py识别当前七阶段布局并转入readme_restoration/validate.py，校验章节、锚点、链接和Git差异范围，不重新读回或核哈希论文。update_readme_navigation.py已改为**只检查、不写README**；旧的整体折叠生成器仅留在9208历史中，不应再执行旧版本。

rebuild_appendices.py仍是只读已有材料/本地Git对象、重建methods附表的离线工具，不会发起新数据库查询；本次恢复没有运行它，也没有重写上轮详细方法/附表。protected_sources.json与上轮validation记录3146个非Markdown结果文件的当时保护验证，不表示本次重新核验了原件。

今后新增工作直接补入相应阶段或新增章节，先明确集合/日期/阅读深度，保留前阶段动机、方法、成果和限制。不要恢复“仅展示最新两条工作线”的首页生成方式。
