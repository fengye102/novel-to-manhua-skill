# novel-to-manhua

[![Validate skill](https://github.com/fengye102/novel-to-manhua-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/fengye102/novel-to-manhua-skill/actions/workflows/validate.yml)

把中文小说、章节或剧情大纲改编成手机竖屏漫画的 Codex skill。它负责剧情拆解、角色与画风锁定、分镜、无字出图、后期排字和质检；**skill 是制作说明，不自带出图模型或排字软件**。

## 画风与流程

- **明确的 Q 版与省笔画法**：全身人物默认约 2～3 头身，大圆头、小躯干、短肢与夸张清楚的表情；头脸、发型、服装主体和必要环境光影精绘，四肢却是火柴人式黑色细线，手是实心黑圆点。普通页保持背景清爽，不画成普通动漫或写实比例。角色外观按[人物视觉卡](novel-to-manhua/references/character-cards.md)固定，不把手机截图的状态栏和灰色外框画进漫画。
- **先画图，后配文字**：分镜时确定准确台词与留白位置；先生成无字、无气泡的画面并验收，再单独叠加气泡、旁白、标题、拟声词、页码和中文。改错字只改排字层，不重画整页。
- **整套制作、成品交付分开**：未指定页数的完整漫改或完整逐页剧本，默认至少拆分 30 页正文（封面另计）；情节不足时补有推进作用的细节，不重复剧情凑页。先做本次范围的全套逐页脚本，再按需出图、排字、归档和质检；给作者的成品版本只含已排字页面，无字底图留作内部返工。只要策划或分镜，就停在文字方案；缺少出图或排字工具时，明确说明已完成到哪一层。

交付链路与 Q 版提示词的可执行约束参考 [novel-comic-promo](https://github.com/CYU1102/novel-comic-promo)，但不沿用其人物设计、固定张数和尺寸。详细规则见 [`novel-to-manhua/SKILL.md`](novel-to-manhua/SKILL.md)；四组样图的选择方法见[视觉语言与样图索引](novel-to-manhua/references/visual-language.md)。

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

## 制作工程与作者交付

新作品先按自身 `Codex.md` 定规则；缺省文件分层如下（只建立实际需要的目录）：

```text
comic-project/
├── Codex.md
├── source/               # 内部：原文与原始素材
├── planning/             # 内部：全套剧情、角色卡、逐格脚本和准确台词
├── drafts/               # 内部：待修中间稿
├── art/                  # 内部：无字底图，供排字与返工使用
├── qa/report.md          # 内部：逐页对应关系和验收记录
└── pages/                # 作者交付：仅已排字成品，例如 page-01.png
```

完整漫画交付时只分享 `pages/` 或由它生成的成品压缩包；若作者另要脚本、无字底图或提示词，再单独提供。具体字段与验收点见[交付与质检](novel-to-manhua/references/delivery-and-qa.md)。仓库中的 14 张 JPG 位于 [`novel-to-manhua/assets/`](novel-to-manhua/assets/)，用作风格和人物特征证据，不是供输出时复制的现成页面。

## 仓库校验

```powershell
python scripts/validate-skill.py
```

该命令与 GitHub Actions 检查 skill 入口、相对链接、参考图与测试用例，以及“先无字画面、后排字”的顺序；**静态校验不等于漫画出图或中文排字的视觉验收**。

仓库目前未附 `LICENSE` 文件；授权范围由仓库所有者另行确定。
