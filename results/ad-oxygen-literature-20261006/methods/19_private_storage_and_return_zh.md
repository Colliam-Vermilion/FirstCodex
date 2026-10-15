# 全量持久存储、实际读回和Windows回填

本轮已完成不依赖存储选择的审计、解析、队列、工具及私有交付包。**尚未连接外部私有存储**，rclone实际检测到已配置remote数量为0。下面区分已验证Git原件、已准备的本机包和仍需用户操作的远端存储。

## 1. 用实际体积选择方案

|内容|实际数量/大小|本轮放置|
|---|---|---|
|已持久原件|54个、111,258,208字节|原结果分支original_files，维持原位置和全部文件|
|当前原件/来源证据全量|135个不同SHA、302,148,223字节|54 Git对象＋81待私有保存对象；包含107主选核心文件、1另存版本、27 XML/传输证据|
|完整解析|907文件、87,325,715字节|当前解析根；另有46,497,792字节SQLite索引|
|新增Git解析样例|58文件、6,728,952字节|R03161/R06325/R09236，原件全部来自已允许共享的Git文件|
|待私有交付包|约178 MB，精确大小及SHA见下列receipt|已生成并全成员SHA校验；没有上传GitHub或外部云|

[私有包准备回执](../inventory/private_package_preparation.json)记录包SHA/体积及本机路径；该路径不是下载链接。[离线独立还原验证](../inventory/private_package_roundtrip_validation.json)记录实际复制、空目录还原和135个原件读取结果。它验证传输/还原流程，**不等于实际OneDrive/S3或新云任务已经读回**。

普通GitHub每文件硬限100 MiB（[官方说明](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)）。现有54个对象已真实保存，不能退回样例；本轮新加的解析样例约6.73 MB适合普通Git。135个原件单独存虽多数小于100 MiB，但整个私有包超过该限制，后续337篇及SI还会增长，历史累积也会增加；更关键的是机构文件不能无依据放到未知可见性的仓库。

Git LFS可在有适当权限的私有仓库承载大对象，但涉及套餐配额/带宽、LFS对象授权和后续Codex smudge下载；LFS指针不是原件。当前没有将已保存原件迁移成指针，也没有将私有文件推入LFS。当前体量不需要为技术展示引入LFS。

**建议实际采用混合存储**：现有54对象留Git；其余81原件及完整解析/索引放本人/学校授权的私有OneDrive或S3兼容存储。manifest和工具继续在原Git分支。最终逻辑库是一套papers映射，不在仓库里另复制一套原件；私有包中不重复打包54个Git原件。私有位置权限仅限本人和获授权Codex任务，不创建公开链接。

## 2. 当前已经实际准备的东西

`transfer_library.py prepare-private`已生成`ad_oxygen_hybrid_corpus_20261015.zip`及其SHA回执。包包括：

- 81个尚未在Git持久保存的原件/来源对象，按canonical_path放置；
- 全部解析、SQLite及554个metadata；
- 每文件SHA/大小、Git原件固定源提交及storage_map；
- 外部数据/媒体引用说明。测序数据库本身没有打包。

包生成时逐个读原文件校验，生成后重新打开校验全部成员。独立还原只从这个包取私有字节，再从Git读取另外54个原件；不会从原下载目录偷偷补文件。恢复时路径越界、重复成员、缺件、SHA错误和已有不同内容会拒绝，原件不覆写。

完整索引可跨论文正文/表格检索；4篇仅XML文章仍不算已获PDF。未缓存的XML图引用、模型、图片/视频视觉内容另有状态，不声称全库全部内容均已索引。

## 3. 用户现在需要做的具体选择/连接

1. 指定**本人/学校允许的私有存储服务和目录**，例如OneDrive for Business的`AD-Oxygen`，或一个私有S3 bucket/prefix。不要提供账号密码，也不要把token写在聊天或Git中。
2. 在Windows安装rclone（[官方](https://rclone.org/install/)），执行`rclone config`，用本人浏览器授权，remote建议命名`adprivate`。S3则在本机私有配置/环境变量安全录入限指定bucket/prefix的凭据。先用`rclone lsf adprivate:AD-Oxygen`检查自己的访问。
3. 给Codex运行环境独立配置访问同一目录所需的安全授权/变量。Windows能读不代表Codex能读；只上传文件也不等于Codex有权限。无需分享浏览器学校会话或整个rclone配置到Git。环境网络需允许所选服务实际API和重定向域名；服务尚未选择，当前没有假称这些域名已配置或实测。
4. 连接完成后，由Codex将当前已备好的私有包上传到确定的私有目录，再从全新目录重新下载，按Git回执中的包SHA及每成员SHA核验、还原、执行verify-view和检索；成功后再记持久通过。用户后续Windows回传也走同一路径。若本人先上传Windows新包，Codex仍要独立读回。

机构订阅原件按个人/机构许可限定访问，仅在授权私有位置存放；不因为更换存储工具而创建公开分享。

## 4. 上传/读回的可执行命令

用户选择位置并完成rclone安全配置后，在Codex运行（替换为实际目录；这里不是已执行的外部上传）：

```bash
rclone copyto /workspace/library-files/ad-oxygen-delivery/ad_oxygen_hybrid_corpus_20261015.zip adprivate:AD-Oxygen/corpus/20261015/ad_oxygen_hybrid_corpus_20261015.zip --immutable --transfers 1 --checkers 2 --retries 3
rclone copyto adprivate:AD-Oxygen/corpus/20261015/ad_oxygen_hybrid_corpus_20261015.zip /tmp/ad-oxygen-remote-readback/ad_oxygen_hybrid_corpus_20261015.zip --immutable --transfers 1
python methods/corpus/transfer_library.py verify --package /tmp/ad-oxygen-remote-readback/ad_oxygen_hybrid_corpus_20261015.zip --expected-sha256 <Git回执中的实际SHA>
python methods/corpus/transfer_library.py hydrate --package /tmp/ad-oxygen-remote-readback/ad_oxygen_hybrid_corpus_20261015.zip --root /workspace/ad-oxygen-private-hydrated --expected-sha256 <同一SHA>
python methods/corpus/transfer_library.py verify-view --root /workspace/ad-oxygen-private-hydrated
python methods/corpus/extract_search.py search --root /workspace/ad-oxygen-private-hydrated --query 'methane AND oxygen'
```

请在项目目录执行Python命令，保证Git原件source_repo_path可读；克隆原结果分支/固定提交后也可设置`--project`绝对路径。必须对照已经信任的Git/本机生产者回执，不以“云端同目录也有一份SHA”代替实际字节校验。

上传使用不可变批次路径；已有相同完整包跳过，发生变化用新批次名，不覆盖旧对象。rclone会重试，已完成包通过SHA复用；单个文件的内部字节续传取决于存储后端，不保证所有后端都支持。Windows新下载可按`--ids`分小批导出，成功合并回执`--exclude-ack`排除旧资产，避免重复上传。

## 5. 本地回传如何合并

Windows流程见[README](../windows/README_zh.md)。新原件先登记、解析，再`prepare-return`。上传原件包＋SHA回执；Codex从同一私有位置重新下载并verify/hydrate后：

```bash
python methods/corpus/transfer_library.py merge-return --root /workspace/ad-oxygen-return-batch
python methods/corpus/verify_inventory.py --root /workspace/ad-oxygen-return-batch
python methods/corpus/render_inventory.py
```

merge先核对全部输入ID/范围、文件路径、大小、SHA和明确的人工身份/版本/关联证据，再按asset_id/ID去重。重复同SHA跳过；另一版本保留并列，旧SHA及首选关系不静默覆盖。仅更新inventory/papers，原人工分类和历史表保持快照；最后返回last_return_merge.json给Windows，用于下一批排重。要合并搜索文件，把新批次extracted子树复制到同一解析根（这些是派生文件），然后重建索引；原件仍按manifest引用私有批次/已有Git位置，原件不搬家。

每个新Codex任务先fetch最新原结果分支，读取metadata和storage_map，实际verify_inventory/verify-view；私有访问失败则准确报告缺哪些原件，只复用当前能读回且SHA匹配的文件。不得用环境发布、临时目录、旧成功列或只下载manifest代替原件存储。
