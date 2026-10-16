# novel-to-manhua

把中文小说、章节或剧情大纲改编成手机竖屏漫画的 Codex skill。它负责剧情拆解、角色与画风锁定、分镜、无字出图、后期排字和质检；**skill 是制作说明，不自带出图模型或排字软件**。

## 画风与流程

- **参考图的省笔画法**：头脸、发型、服装主体和环境光影精绘；露出的四肢是火柴人式黑色细线，手是实心黑圆点。角色外观按[人物视觉卡](novel-to-manhua/references/character-cards.md)固定，不把手机截图的状态栏和灰色外框画进漫画。
- **先画图，后配文字**：分镜时确定准确台词与留白位置；先生成无字、无气泡的画面并验收，再单独叠加气泡、旁白、标题、拟声词、页码和中文。改错字只改排字层，不重画整页。
- **按任务停在合适阶段**：只要策划或分镜，就交付文字方案；要完整漫画，才继续无字底图、排字和逐页验收。缺少出图或排字工具时，明确说明已完成到哪一层。

详细规则见 [`novel-to-manhua/SKILL.md`](novel-to-manhua/SKILL.md)；四组样图的选择方法见[视觉语言与样图索引](novel-to-manhua/references/visual-language.md)。

## 安装

在 Codex 中调用 `$skill-installer`，指定仓库 `fengye102/novel-to-manhua-skill` 和仓库内路径 `novel-to-manhua`。也可用安装器脚本：

```powershell
python "$HOME/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py" --repo fengye102/novel-to-manhua-skill --path novel-to-manhua
```

安装器不会覆盖已有的同名 skill；首次安装后在下一轮对话中调用。已安装旧版时，先备份个人修改，再更新本机的 `novel-to-manhua` 目录。

## 调用示例

```text
$novel-to-manhua
把下面的小说片段改成 3 页 3:4 竖屏漫画。先给角色视觉卡和逐格脚本；
确认画面后先生成无字、无气泡底图，再单独排入简体中文台词。

原文：雨夜，阿岚在门前发现一封没有署名的信。她刚拆开信，
屋内那盏十年没亮过的灯忽然亮了。信上只有一句话：“别回头。”
```

如需只做分镜、指定页数、沿用某组参考图或另给画风，直接在请求中说明。不要把仓库的参考图人物和台词直接搬进无关故事。

## 交付结构

新作品先按自身 `Codex.md` 定规则；缺省文件分层如下（只建立实际需要的目录）：

```text
comic-project/
├── Codex.md
├── source/               # 原文与原始素材
├── planning/             # 剧情、角色卡、逐格脚本和准确台词
├── drafts/               # 待修中间稿
├── art/                  # 已验收的无字底图，例如 page-01-art.png
├── pages/                # 已排字的成品，例如 page-01.png
└── qa/report.md          # 逐页验收记录
```

具体字段与验收点见[交付与质检](novel-to-manhua/references/delivery-and-qa.md)。仓库中的 14 张 JPG 位于 [`novel-to-manhua/assets/`](novel-to-manhua/assets/)，用作风格和人物特征证据，不是供输出时复制的现成页面。

## 仓库校验

```powershell
python scripts/validate-skill.py
```

该命令与 GitHub Actions 检查 skill 入口、相对链接、参考图与测试用例，以及“先无字画面、后排字”的顺序；**静态校验不等于漫画出图或中文排字的视觉验收**。

仓库目前未附 `LICENSE` 文件；授权范围由仓库所有者另行确定。
