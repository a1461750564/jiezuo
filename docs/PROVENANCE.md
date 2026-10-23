# 来源、兼容与维护边界

## 当前公开快照

项目名为「界作 / Jiezuo」，Skill 名为 `jiezuo`。公开源码整理于 2026-10-23，以当时已安装的界作为基础，包含业务理解前置、产品文案与开发对话边界、按实际任务走查的修订。

`metadata.version` 保留 `0.23.8-enhanced.pro.17`，用于与已有交付对应；精确公开内容以本仓库提交为准。它不是官方 Oil UI Pro 的版本号。未访问或分发官方私有 Pro 内容。

上游基点为 [oil-oil/oil-ui@feb1f95e8cec48bb8ba35181cb66f94f23b1b6fc](https://github.com/oil-oil/oil-ui/tree/feb1f95e8cec48bb8ba35181cb66f94f23b1b6fc)。上游更新须在维护任务中手动审阅，不在 Skill 加载或普通设计任务中自动拉取。

## 本次整理范围

- 统一项目介绍、调用名与素材工具的项目 User-Agent。
- 增加公开安装、调用、支持范围及许可索引。
- 保留运行文件和现有脚本测试；安装说明只复制运行文件。
- 将教学案例的私有路径和内部评审过程说明整理为公开来源、改动与限制；保留原始来源文件哈希、图片哈希、固定事实和实现。

没有更改设计规则、评审门槛、检测算法或样例功能。没有为公开整理追加设计评测。旧交付包、历史分数和私有证据继续独立保留，不作为当前案例或所有宿主的质量证明。

## 兼容标识

以下旧名称仍用于既有协议或数据，故不随品牌更名：

- `oil-ui-tokens`：`DESIGN.md` 中供检测器读取的 JSON 块。
- `/*__OIL_UI_DATA__*/`：风格对比页模板的数据注入标记。
- `oil-ui-demo:*`、`oil-ui-enhanced:*`：原型的本地状态键。
- `OIL_DEMO_PORT`、`OIL_SHOOT_TIMEOUT_ATTEMPT`：演示或诊断环境变量。
- `pro8`、`pro11`、`pro12` 等现有 fixture 名：检查来源，不代表当前质量分数。

第三方版权、来源仓库和许可证中的原名保持不变。不得用批量替换破坏署名或兼容字段。

## 分发边界

运行文件包括 `SKILL.md`、`agents/`、`references/`、`scripts/`、`assets/`、`licenses/`、`LICENSE` 和 `THIRD_PARTY_NOTICES.md`。`tests/`、`docs/` 与 README 服务源码维护，不要求安装到 Skill 目录。

新任务的截图、报告、缓存与产物应留在任务目录。个人路径、访问凭据、内部评测材料和旧交付包不纳入公开仓库。各例的具体已知限制以对应 CASE 与 SOURCE 文件为准。
