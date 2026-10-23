# TodoMVC 样例的设计与集成边界

基点为 tastejs/todomvc@ff43b02e59dfa604386bb382034b2cd07c2bcd8a 的 javascript-es5。没有既有设计规范文件，因此在样例根目录沉淀本次决定。baseline 与 upstream-src 是未修改的来源；授权改造分别在 tidy、upgrade、reshape、feature，互不覆盖。

整理保持原红色品牌、单列、CRUD 与双击编辑，修长标题、页尾换行和焦点。升级增加明确的 Edit 按钮与可访问名称，仍调用原标签的编辑事件；旧双击路径保留。重塑另获准采用中性纸色、蓝色操作、深绿文字与主任务/说明两区；小屏变为上下排列。功能分支基于升级增加本页标题检索，不改 hash 筛选与数据字段。

数据仍由原 Store/Model/Controller 管理：id/title/completed、#/、#/active、#/completed；Store 实际是页面内存，刷新会重置，未擅自增加持久化。无真实服务器、权限或业务数据库。

原页尾有 display 的内联更新与高特异性的 :active 浮动，改成弹性布局时必须同时处理隐藏态、按下态和装饰伪元素的命中；具体修正只在 changes.css，未改 MVC。检查 Enter、Esc、筛选、删除与全选后再验收。本例不验证真实请求与写入保护。
