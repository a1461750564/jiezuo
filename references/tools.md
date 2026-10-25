# 工具

本目录自带的程序不需要读源码，命令里的 `<skill>` 换成本 Skill 的安装目录。这里只写什么时候用和最常用的几条命令；全部选项、动作写法和输出文件见各自的 `--help`，写错时报错会给出照抄就能用的写法。

宿主有自己的浏览器工具时，查看页面、走查流程照常用；可运行界面的最终脚本检查按入口步骤 3 执行，宿主截图不能代替 lint/coverage。这里的工具开独立临时浏览器，不碰用户自己浏览器里的数据。本机缺 Node 22+，或者没有 Chrome、Chromium、Edge 时，退回宿主工具，按实际能力取证并说明未覆盖部分，不自动安装运行时。遵循项目的 EnvKit 等运行环境约定；远端宿主先核对命令实际运行位置、脚本路径和本地服务是否可达。任务或项目已经指定了其他截图工具时照用，保留等效检查和未覆盖范围，不为重复取图重放操作。

原生选择菜单先确认实际输入通道能操作，同环境已有校准可复用。macOS 的 headless Chrome 可能取消原生 select 菜单；遇到按键后选值不变，改用已有可见浏览器与原生键盘，读回选值及结果。脚本赋值只证明状态逻辑，URL直达只证明恢复，分别记账；前置输入未完成时，依赖它的检查记未验证，不连报成多个产品缺陷。

## 截图和录屏

### 什么时候截，截多少

截图分两种用途，不要混在一起：

- **看一眼**：改完一批，想看效果。只截当前这一屏，一条命令。把一批改动攒在一起改完再截，不是每改一处截一次；页面没有变，就不重复截。
- **取证**：按当前验收点选择截图、局部或录屏。`--evidence` 是可选组合，包含状态图、2 倍图、动效探测与录屏；不要求每次送审和交付都重跑整套。

每一轮评审只重新取这一轮改动影响到的证据。没有动过的状态和动效，沿用上一轮的文件，交接时注明哪些是沿用的；拿不准有没有被影响到，例如改了共享样式，就重取那一项。

### 常用命令

```text
node <skill>/scripts/shoot.mjs <页面地址、HTML 文件或候选目录> [选项]
```

| 要什么 | 加上 |
| --- | --- |
| 看一眼桌面效果 | `--size desktop`；不写时是手机 390x844；只看整体版式可加 `--thumb`（0.5 倍速截） |
| 一次截完多个页面候选并出并排图 | 传候选目录/manifest（本地 HTML 或本机 URL）或多个 HTML 文件，同一次浏览器会话截图并自动出 `sheet.png` |
| 只看改过的局部组件或区域 | `--selector ".card"`，自动滚入视口并只截该元素区域 |
| 操作几步再截 | `--steps "click .open; wait 300"` |
| 送评审或交付前取证 | `--evidence --states idle,done`（仅用于已有状态入口；带动作的重放限制见下文） |
| 落地页录一段从头滚到底 | `--record --steps "scroll 600; scroll 600; scroll 600"`，按页面长度多写几步 |
| 截图还原：和参考图比对 | `--compare 参考.png --size <参考的逻辑尺寸>` |
| 给用户指出问题：在元素上画框、标编号 | `--mark "1=.page-head .btn; 2=.toggle-row" --full` |
| 看清一段过渡 | 录屏时加 `--frames 8`，另出逐帧标时间的序列图 |
| 把几张图拼成一张对比图，不需要页面 | `--stitch a.png --label 修改前 --stitch b.png --label 修改后` |

`--states` 仅适用于已有 `?state=<名字>` 入口的原型。旧项目用已有路由、测试数据或 mock 进入状态；不要为取证向业务代码注入调试参数。其他选项见 `--help`；`--dry-run` 只解析计划，不启动浏览器，输出 `execution` 中的重复次数与是否阻止执行。

manifest 中的图片或无效候选会显式列为未覆盖，`--dry-run` 的 `candidateCoverage` 和实际 `report.json` 的 `skipped` 记录保留原因，返回码为 1。混合输入仍为有效页面取证；仅有未覆盖候选时不启动浏览器。图片可查看原图或单独用 `--stitch` 拼图，不冒充页面检查。录屏帧使用本次独占的随机临时目录，清理不复用已有的 `frames` 或 `frames-组名` 目录。

**动作默认不重放。** 所有 `--steps` 都可能产生写入，脚本不凭 click/hover 名称猜安全性。普通截图按目标×尺寸×密度×状态执行每组；`--evidence` 的探测和录屏各执行一次，`--motion` 叠加截图或录屏也执行两次。默认拒绝这些重复组合；带步骤时超时不整次重跑，失败停止后续动作与重建重放。单次提交可用一个目标/状态/尺寸/倍数的截图，或 `--record --steps "click .send; waitfor text=已保存"` 一次录下操作与终态，再读回后台结果。

只有已确认可安全重放的只读操作，或隔离假数据且每次能回到确定起点时，才显式加 `--replay-safe` 使用多状态/密度/探测组合及自动重试。该标志是调用者声明，不会重置数据库，也不会实现服务端去重。缺少 ffmpeg 时录屏只保留真实采集帧，报告会注明视频未生成；不能把帧文件或命令成功当成完整视频验收。结果未知时先核对请求与持久化记录，不能直接照抄重试命令。页面加载本身也可能触发写入，应先检查目标；无步骤的截图不能据此保证只读。

`--zoom 2` 是 DPR 2 的细节图，不是浏览器 200% 缩放。后者需要在实际浏览器设置缩放并记录原始 DPR、缩放值及 CSS 视口。视口减半加 DPR 2 只能标为模拟；脚本在宽度小于 600 时还启用触控仿真。

浏览器启动失败时，输出目录会保留 `browser-startup-failure-attempt-<轮次>.json`，标准错误也保留同一记录：实际耗时、配置时限、进程退出状态、端口文件和最近的浏览器错误。清理临时浏览器前先取证；只有一次单跑通过不能证明先前的偶发失败已修复。

### 检索和下载真实素材

在项目工作目录运行，后续命令也在同一目录，搜索结果的编号才接得上：

```text
node <skill>/scripts/curate-media.mjs search "<关键词>" --kind texture --limit 6 --sheet --dir candidates
node <skill>/scripts/curate-media.mjs search "<一组词> | <另一组词>" --sheet --dir candidates
node <skill>/scripts/curate-media.mjs preview V1,T2 --sheet --dir candidates
node <skill>/scripts/curate-media.mjs fetch C1,T2 --dir assets --sheet
node <skill>/scripts/curate-media.mjs fetch V3 --dir <不上线的参考图目录>
node <skill>/scripts/curate-media.mjs fetch T2 --maps all --resolution 1k --dir assets
```

`--kind` 支持 `all|texture|design|photo|blueprint|map|plate|science|video`。信源包括材质库、欧美与日本的博物馆和图书馆馆藏、NASA，各类别对应哪些信源见 `--help`。`all` 交错取各信源；用 `|` 可一次搜几组词。关键词多用英文，东亚题材可直接用中日文，简体搜不到时换繁体或日文写法。

结果存入 `.curate-cache.json`，编号跨次搜索保留。每项 `use` 说明用途：`page` 可放进页面（CC BY/BY-SA 要署名），`check` 先看来源页，`reference` 不能放进页面；`--use page` 只留第一种。

`search --sheet` 和 `preview` 出带编号、用途和原图尺寸的联系表 PNG，直接读这张图挑选，不要只看标题；同时给每项算 `look`（四边色、是否浅色纸底、哪些区域干净可压字等），并出 HTML 联系表。`fetch --sheet` 出本地联系表并检查真实宽高、完整解码；视频自动截首帧 poster。

贴图默认下载 1k Diffuse，`--maps all` 拉取 Diffuse、Roughness、OpenGL Normal JPG 并校验大小与 MD5；使用与许可见 [配图](media.md#真实贴图与科学工程素材)。下载及 poster 自动写入同目录 `SOURCES.md`，兼容 `fetch "<URL>" --out assets/<文件名> --note "来源说明"`。全部选项见 `node <skill>/scripts/curate-media.mjs --help`。

### 看结果

交给评审前先自己看一眼：默认状态是不是已经加载完，遮字版有没有把图形也一起盖掉。证据有错先定位原因；涉及动作时先读回状态，不盲目重放。汇总里提示录屏和截图不一致时，静止的终态以截图为准，在确认可安全重复的场景再单独重录那一段核对过渡。画面是空的 WebGL 截图不能当证据。

每张截图还会查一组能从页面样式里直接判断的问题，命令输出里以“默认做法提示”列出：

- **需要实际核对的可读性线索**：文字对比度不达标、正文小于 13px、多行正文行高过紧、首屏里停在透明状态的内容。
- **改掉或写出理由**：有色底上的灰字、正文行太长，以及模型默认做法：标题上方的眉标和编号标签、彩色单侧边线、渐变文字、卡片里套卡片、表情符号当图标、中文界面里的英文大写标签、标题离上文比离下文还近。保留的项，在交付说明里写出它怎样服务方向。

检查会误报，例如真实的步骤编号、确实需要的标签；误报在交付说明里写一句。它只认得写法，判断不了好不好看：提示清零之后，仍要自己看截图。接口 401、404 可能阻断任务，需要判断与本次改动的关系；在授权范围修复引入的错误，不能绕过登录或吞掉失败。无关环境故障记录影响与未验证范围。

另有标题跳级、控件名称、关联标签、图片替代文本和功能字号提示；局部文字裁切、打开浮层的裁切与当前视口遮挡为启发式线索。`lintCoverage` 记录本次扫描范围、对比度已查/跳过计数与限制；缩略图标为未运行，失败标为失败。不遍历 iframe/shadow DOM，也不代表未打开状态已验。复杂背景与原生控件的对比度须另看。CLI 保持提示型退出约定，验收需读取 `issues`、`lint`、`lintCoverage` 并核对实际画面，不能只看退出0。

## 写可操作的小样

方向探索阶段的首屏不做交互，用不到这一节；选定方向后做完整页面时再用。存量项目照用项目自己的技术栈。

仅对无既有技术栈的独立原型，可以把一个组件或页面写成单文件，用地址参数切换合成状态，避免逐状态复制。颜色、字号、间距、圆角先定成十来个 CSS 变量，后面一律引用变量，不引入需要构建的工具。表单、切换、展开这类状态用 Alpine.js 写在 HTML 属性上：把 `<skill>/assets/vendor/alpine.min.js` 复制到任务目录的 `vendor/` 再引用，状态集中在一个 `x-data` 里，初始状态读地址参数。手势跟手、物理模拟、Canvas 和 WebGL 绘制放进单独的 JS 模块，每帧更新的数据不放进 Alpine 的状态。

`functionalText` 也检查普通可见数据短句；读屏专用的微小裁切标签只从视觉检查排除，数量见 `visuallyHiddenTextSkipped`，语义检查仍保留。不要用sr-only类名遮蔽真实可见问题。


## 按需检索设计与实现资料

已有参考不足以作设计或实现取舍时再查；已有合适依据则直接沿用。`find_reference.py` 用 Python 3.10+ 标准库只读精选目录，不联网、不写缓存、不安装依赖；默认只返回 4 条。不用打开整份 JSON：

```text
python3 <skill>/scripts/find_reference.py "中文阅读 字体" --domain typography
python3 <skill>/scripts/find_reference.py "瀑布图 增减" --domain chart
python3 <skill>/scripts/find_reference.py "状态同步" --stack react --version 18
python3 <skill>/scripts/find_reference.py "缓存 读回" --stack nextjs --version 14 --variant app-router
python3 <skill>/scripts/find_reference.py "弹窗" --stack shadcn --variant base-ui
python3 <skill>/scripts/find_reference.py --list
```

`--domain` 限定 `workflow/style/typography/color/icons/chart/interaction/implementation/stack`；`--list` 列实际范围，`--json` 给结构化结果，`--limit` 可选 1–10。中文/英文关键词由精选条目维护，排序只是文本相关性，不是审美分、置信度或业务判断。没有命中就说明范围并查相关官方资料，不生成默认风格或模板。

每条给出用途、不适用条件、本地参考路径、官方/固定版本来源及适用性。缺版本或 Router/组件底层时标 `needs-context`；只提供文档入口的栈标 `check-project-docs`；`within-curated-scope` 只表示符合目录声明，不证明已运行、API 全部兼容或性能更好。目录日期是维护快照，不代表远端文档一直未变。

只知道大版本、而某条 API 从小版本才可用时，会要求 `version-precision`，不把 `19` 猜成 `19.0.0` 或最新 `19.x`。预发布版本与依赖范围不作数值判断，直接查项目对应文档。

查中后只读当前问题相关内容，沿用实际项目的品牌、tokens、组件、接口与状态。目录是参考卡，不是额外流程或必做检查表。数据与来源集中在 `reference-catalog.json`；维护时核对官方原文与版本，只改相关条目，不自动拉取上游整库。

## 按项目技术栈查实现资料

先看项目配置、锁文件和已复制组件，确认版本属于哪个包；`--version` 必须同时指定 `--stack`，不会把 Next 的版本当成 React 的版本。`--variant` 可区分 `app-router/pages-router`、`radix/base-ui/react-aria` 和 `runes/legacy`；未辨认时不把候选 API 当成可直接采用的实现。

常用 Web 详解覆盖 React 状态/Effect/性能、Next App/Pages 与缓存模型、Vue、Nuxt 4、Svelte runes/legacy、Angular signal、Tailwind 3/4、shadcn 三种底层，以及 token/组件状态分工。版本不符的专属条目被排除；未知版本不猜，旧项目仍按对应文档与本地代码工作，不为查资料换栈、升级或重建组件。

另提供 22 栈官方入口：HTML/Tailwind、React、Next.js、Vue、Nuxt、Nuxt UI、Svelte、Astro、Angular、Laravel、shadcn、Three.js、React Native、Flutter、SwiftUI、Compose、Avalonia、JavaFX、Uno、UWP、WinUI、WPF。后者的入口不等于完整本地规则库；原生 App/桌面资料也不扩大界作现有实机验证范围。只有入口不足时才打开相应版本的官方文档。

选题和检索组织借鉴 UI UX Pro Max，条目与脚本独立实现；不分发其 CSV 库、生成器或附带 Skill。来源、固定版本与 MIT 许可见 [第三方说明](../THIRD_PARTY_NOTICES.md#ui-ux-pro-max)。

## 可选的设计规范比对

`node scripts/shoot.mjs page.html --design /项目/DESIGN.md --out shots` 只报不拦。规范正文不作猜测；显式声明允许值，例如：

```oil-ui-tokens
{"fonts":["PingFang SC","Georgia"],"colors":["#193d32","#ffffff"],"radii":[0,4,8],"fontSizes":[12,14,16,24,40]}
```

数组可按当前改造范围只列一部分；字号与圆角单位为 CSS px，颜色为六位十六进制，字体是计算后首选族名。响应式字号需列实际允许值。读取失败/缺块/部分覆盖写入 `lintCoverage.design`，不据此判通过。字体/字号检查可见文字，颜色检查文字、可见填充与边框，圆角检查四角；渐变、透明合成、变量语义和完整组件规范仍需人工核对。

`lint` 的 `level=hint` 是风格或启发式线索，`warning` 是需核实的质量问题；两者都不改变退出状态。可疑字体、配色、奶油底、网格、动效或中点/箭头如有品牌、语义或用户依据应记录保留理由，不为清零删除信息。中文过紧字距阈值小于 -0.04em（拉丁小于 -0.055em）；行尾按实际字形测量，显式换行也会提示。规则覆盖边界见 `lintCoverage`，不能用零命中代替实际看图、键盘和状态走查。
