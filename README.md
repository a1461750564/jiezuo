<div align="center">

# 界作 · Jiezuo

面向 AI 编程助手的前端设计与交互完善 Skill

先理解任务，再组织界面；用实际运行结果检验设计。

</div>

界作帮助模型设计、改进和评审网站、App、后台与组件。它把用户任务、业务对象、状态变化和操作依据放在视觉结构之前，再将选定概念延续到整页与后续主流程。

基于 [Oil UI 开源版](https://github.com/oil-oil/oil-ui) 独立维护，不代表官方 Oil UI Pro。当前公开快照保留 `0.23.8-enhanced.pro.17` 版本标识，调用名为 **`$jiezuo`**。

## 能做什么

| 场景 | 工作方式 |
| --- | --- |
| 新页面与较大改版 | 拆解具体参考、选择素材和结构，必要时生成方向对比页 |
| 整页视觉与精修 | 统一字体、色彩、层级、间距和视觉主角，优先处理最大视觉差距 |
| 交互与表单 | 串起主要任务，检查状态同步、校验、失败恢复、键盘及窄屏操作 |
| 后台与工具 | 按业务对象选择队列、主从、表格、画布等工作区结构 |
| 老项目 | 在现有组件、数据和流程上整理、升级或重塑，保护未授权改变的业务行为 |
| 评审与取证 | 实际截图、布局与文案提示、任务走查；宿主支持时派独立评审并在预算内修正 |

小改动按指定范围处理，已有品牌和获批方向直接沿用；不会要求每次重新做三套方案。设计与任务可用性分别验收，产品文案基于真实事实和状态，不把开发对话直接搬进界面。

## 安装到 Codex

先获取源码：

```sh
git clone https://github.com/a1461750564/jiezuo.git
cd jiezuo
```

在仓库根目录执行以下 macOS / Linux 命令。只复制运行文件；已有同名 Skill 会先移入备份目录。命令不安装 Node、浏览器或其他依赖。

```sh
(
  set -eu
  codex_root="${CODEX_HOME:-$HOME/.codex}"
  install_dir="$codex_root/skills/jiezuo"
  mkdir -p "$codex_root/skills" "$codex_root/skill-backups"
  if [ -e "$install_dir" ] || [ -L "$install_dir" ]; then
    backup_dir="$(mktemp -d "$codex_root/skill-backups/jiezuo.XXXXXX")"
    mv "$install_dir" "$backup_dir/jiezuo"
    printf '旧版本备份：%s\n' "$backup_dir/jiezuo"
  fi
  mkdir -p "$install_dir"
  cp -R SKILL.md agents references scripts assets licenses \
    LICENSE THIRD_PARTY_NOTICES.md "$install_dir/"
  printf '已安装：%s\n' "$install_dir"
)
```

`README.md`、`docs/` 和 `tests/` 是仓库资料，不需要装入 Skill 目录。回退时保留当前目录，再将打印出的备份移回原安装位置。

## 开始使用

在 Codex 后续对话中使用 `$jiezuo`，给出项目位置、主要任务和已有约束。例如：

```text
$jiezuo

改进当前项目的工单列表和详情。
用户需要快速找到待处理工单，依据最近一次观察判断下一步，
处理后返回原来的筛选和位置。
先读取项目规范、实际数据结构和现有操作流程，保留接口和权限。
沿用已有品牌，完成桌面、手机和键盘操作，并说明未验证的部分。
```

对新页面，可以补充质量参考：

```text
先查看与本任务同品类的具体优秀作品，说明可迁移的构图、
字体、素材和交互关系，以及不适用的部分。
让选定概念贯穿首屏以下与后续主流程，不靠重复装饰维持风格。
沿用 Skill 的评审和停止条件，先修硬缺陷，再处理最大视觉差距。
达到任务门槛或预算用完即停止，如实保留剩余问题。
```

完整入口见 [SKILL.md](SKILL.md)。正常完整设计任务以 9 分为目标、最多 3 轮；用户指定的范围、轮次和预算优先。目标不等于质量保证，不能看图或无法独立派审时须说明能力限制。

## 工具与环境

文字流程不依赖指定模型或其他 Skill。以下工具按需使用，不会在加载 Skill 时自动安装或联网更新。

| 工具 | 要求与用途 |
| --- | --- |
| `scripts/shoot.mjs` | Node 22+，现有 Chrome / Chromium / Edge；截图、交互步骤、布局与可读性提示 |
| `scripts/build_explorer.py` | Python 3.10+ 标准库；将候选页面或图片组装为风格对比页 |
| `scripts/curate-media.mjs` | Node 22+、网络访问；检索素材、保留来源及权利说明 |
| `scripts/find_reference.py` | Python 3.10+ 标准库；离线检索精选设计/实现参考，带版本及分支适用性，不联网或安装依赖 |
| 可选视频与素材处理 | `ffmpeg` / `ffprobe`；缺失时相应输出受限，不视为完整验证 |

例如从仓库根目录检查一个已经运行的本地页面，证据写到任务自己的目录：

```sh
node scripts/shoot.mjs http://127.0.0.1:3000 \
  --size desktop,phone --out /path/to/task/evidence
```

带提交操作前先判断写入与重放风险；`--evidence` 等组合可能执行步骤多次。详见 [工具说明](references/tools.md) 和脚本 `--help`。高像素密度截图不等于真实浏览器 200% 缩放。

参考不够时可以按问题查资料，例如 `python3 scripts/find_reference.py "状态同步" --stack react --version 18`。目录有 69 条精选卡、22 栈官方入口，具体覆盖见 [按需检索](references/tools.md#按需检索设计与实现资料)。它不生成设计系统、不代替业务理解或实际验证；其他平台的入口不代表已完成平台验收。

## 从示范学习

示范采用合成数据，重点是可迁移的选择过程，不能替换项目的真实业务和接口。

| 示例 | 学习重点 |
| --- | --- |
| [潮间](assets/cases/worked-examples/chaojian/CASE.md) | 从首屏概念延续到核心内容、选票和确认，而非重复图案 |
| [渡衡展运](assets/cases/worked-examples/persuasion/CASE.md) | 对象、依据与未决状态如何组织为说服页和相关内页 |
| [榆岚巡检](assets/cases/worked-examples/queue/CASE.md) | 观察优先、定位、详情与返回关系 |
| [青岫器材](assets/cases/worked-examples/recovery/CASE.md) | 混合结果、草稿状态、查单与安全补交 |
| [TodoMVC 改造](assets/cases/todomvc/DESIGN.md) | 同一现有业务中的整理、升级、重塑和功能增补 |

还附有 [组件原型](references/component-polish.md) 与 [工作区原型](references/workspaces.md)。按当前问题读取，不把展示网格或示范外壳直接套进产品。

## 支持范围与限制

- 主要验证环境是 macOS 上的 Codex、本机 Chrome 与 Node 26.2.0。文本协议可迁移，但其他模型、宿主和操作系统的完整链路未据此保证。
- 独立评审需要隔离上下文和看图能力；交互验收需要实际可操作环境。自检、截图保存和 lint 通过不能替代这些能力。
- lint 是提示，不是审美裁决或可访问性认证。它需要结合实际画面判断，也可能漏报或误报。
- 自带页面是教学原型，部分使用内存假后端；不接真实支付，也不承诺生产权限、持久化或事务安全。具体边界见各例的 `CASE.md` / `SOURCE.json`。
- 素材接口可能变动，权利状态需逐项核对；获取到文件不等于拥有任意用途的许可。
- 不承诺每次达到 9 分、获奖水准或优于其他工具。历史评测只适用于对应任务，私有报告和旧交付包不随仓库发布。

## 维护与检查

仓库保留现有脚本测试与检测 fixture，可在准备好所需运行环境后执行：

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
```

这是脚本检查命令，不是设计质量评分。本次公开整理没有重跑设计评测；来源、兼容标识和整理范围见 [维护说明](docs/PROVENANCE.md)。

## 来源与许可

保留 [Oil UI](https://github.com/oil-oil/oil-ui) 的 MIT 许可与原作者署名，独立维护的改动沿用 MIT。字体、Alpine.js 及其他第三方内容遵循各自许可，详见 [LICENSE](LICENSE) 和 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
