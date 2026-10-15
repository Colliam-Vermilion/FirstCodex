# 已保存的可共享原件

此目录保存实际文件字节：40份自身明确CC BY/CC0的正文、9个官方补充附件、5个解包派生Excel，共54对象。作者、题名、DOI、原下载URL、许可链接及SHA见 [ATTRIBUTION_utf8.csv](ATTRIBUTION_utf8.csv) 和 [持久原件清单](../methods/audit/current_original_files_manifest_utf8.csv)。正文按原ID和原文件名组织；不同历史字节的R10086文件加当前日期/SHA，不覆盖旧SHA。

官方SI中ZIP是原始附件；其中Excel解包件标为派生，不重复计附件。原文件未改写、未删除署名或版权页。其余未明确允许再分发的本机正文/SI不在此目录，未宣称已备份。

取回方式：GitHub结果分支打开文件选择Download raw file；或对结果分支选择Code → Download ZIP。`ad_oxygen_literature_final.zip`只是表格/方法/审计包，**不含此目录二进制原件**；GitHub整个分支ZIP才包含已提交文件。

独立克隆或解压结果分支后，从项目目录运行 `python methods/verify_current_original_files.py`，逐个核对54个文件的SHA及大小。远端独立读回证据见 [readback审计](../methods/audit/current_remote_original_readback_20261015.json)。读回验证不依赖本机下载目录，不把清单本身当作PDF备份。
