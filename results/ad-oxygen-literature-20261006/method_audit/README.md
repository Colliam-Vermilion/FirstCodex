# 本次方法审计的范围与复核

本次只将两条工作线的现存证据解释成当前方法说明，不执行新学术/数据平台查询，不重新筛选，不重写原Excel、CSV、JSON或进度。基准为提交0f9eeec20bc23a421165c8cff352137ba68fac48。

- [项目入口](../README.md)
- [机制详细方法](../oxygen_response_review/methods/METHODS.md) · [机制检索附表](../oxygen_response_review/methods/QUERY_APPENDIX.md)
- [数据详细方法](../omics_dataset_discovery/methods/METHODS.md) · [数据检索附表](../omics_dataset_discovery/methods/QUERY_APPENDIX.md)
- [离线集合审计](audit_summary.json) · [关键提交的原摘要快照](stage_history.json) · [本次校验](validation.json)

从仓库根目录可离线执行：

```bash
python results/ad-oxygen-literature-20261006/method_audit/rebuild_appendices.py
python results/ad-oxygen-literature-20261006/method_audit/validate.py
```

第一条只读已有材料/本地Git对象，写两条工作线methods内的查询附表、来源/集合/选择审计及本目录的复核记录。第二条核原结果未变、实际数量及当前本地链接。两者不调用原检索、筛选或导出脚本。update_readme_navigation.py仅整合README导航，原README留在同文件历史折叠区。

protected_sources.json记录3146个已有非Markdown结果/响应/脚本等文件的基准SHA，不包含原论文PDF；没有为了本次方法整理重复下载或核哈希论文原件。Markdown更新限方法、导航及旧阶段报告顶部指引。

本次查清了Europe PMC旧摘要与后续成功响应并存、原17范围与原17推荐不完全同集，以及论文续跑队列残留12篇旧22已审计记录。后者的原2228队列保持不变，问题及可定位ID在数据方法中明确。Crossref尾部、未保存的模型输入片段/选择细节、未核独立支持和被阻断文件传输继续作为真实缺口，不补造理想执行记录。

[GitHub交付文档独立读回](remote_readback.json)：9份当前README、详细方法和查询附表通过官方Git Blobs API重新获取，解码后大小/SHA256及逐字节一致；此操作没有重新请求文献或数据平台。
