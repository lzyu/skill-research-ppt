"""Replace three SkillHub pages with two: capabilities + ecosystem portrait."""
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Pt

from redesign_lifecycle import add_rect, add_text, set_run

SRC = "skill-final-v1.pptx"
RED = RGBColor(0xB5, 0x33, 0x3B)
TITLE_RED = RGBColor(0xC7, 0x00, 0x0B)
INK = RGBColor(0x1A, 0x1A, 0x1C)
GRAY = RGBColor(0x5B, 0x61, 0x6B)
LIGHT_GRAY = RGBColor(0x8B, 0x8E, 0x94)
BORDER = RGBColor(0xE2, 0xE4, 0xE7)
TRACK = RGBColor(0xED, 0xEF, 0xF2)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SLATE = RGBColor(0x56, 0x64, 0x72)
R_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def add_list(s, x, y, w, h, items, size=9.5):
    box = s.shapes.add_textbox(int(x), int(y), int(w), int(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    for i, text in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = 1.12
        p.space_after = Pt(4)
        r1 = p.add_run(); r1.text = "· "
        set_run(r1, size, RED, True)
        r2 = p.add_run(); r2.text = text
        set_run(r2, size, INK, False)
    return box


def add_bar(s, x, y, w, h, ratio, color):
    add_rect(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, TRACK, None, radius=0.4)
    fill_w = max(int(w * ratio), int(0.002 * w)) if ratio > 0 else 0
    if fill_w:
        add_rect(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, fill_w, h, color, None, radius=0.4)


def card_header(s, x, y, num, title, sub, W, H):
    add_text(s, x + 0.015 * W, y + 0.013 * H, 0.030 * W, 0.022 * H, num, 9, RED, True)
    add_text(s, x + 0.043 * W, y + 0.011 * H, 0.260 * W, 0.024 * H, title, 11, INK, True)
    add_text(s, x + 0.043 * W, y + 0.043 * H, 0.300 * W, 0.020 * H, sub, 8.5, GRAY, False)


def build_capabilities(s, W, H):
    add_text(s, 0.035 * W, 0.040 * H, 0.93 * W, 0.055 * H,
             "SkillHub 关键能力：20 万供给、多路安装、云端试跑、TRACE 评分",
             24, TITLE_RED, True)

    cards = [
        ("01", "供给与发布", "20 万 Skill，来源三条线",
         ["20.0 万 Skill / 13 类 / 1,999 家企业",
          "ClawHub 同步 + 社区 + 企业；来源可重叠",
          "Web / CLI / GitHub / Agent 发布；版本、可见性、团队审核",
          "来源记录可重叠：community / enterprise / clawhub 不可直接相加"]),
        ("02", "分发与安装", "Web、CLI、API、DSH、ZIP",
         ["skillhub search / install <slug> --dir ./skills",
          "装到宿主目录；Claude Code / Cursor / Codex 等可发现",
          "不自动装 pip/npm 依赖，也不执行包内脚本",
          "默认 ./skills；不指定 --dir 可能不被宿主识别"]),
        ("03", "云端试跑", "从「能装」到「能跑」",
         ["前端已有 sandbox / session / 运行案例",
          "支持创建、恢复、清理会话，保存结果",
          "本次只读核查，未登录实测隔离、成功率、费用",
          "官方文档列沙箱 / 会话 / 文件处理；公开 API 契约未完整"]),
        ("04", "TRACE 评测", "从「能装」到「可评」",
         ["5 维、15 子项；抽样 40 条有效",
          "均分 4.54 / 5；72.5% ≥ 4.5",
          "企业覆盖 100%、社区 74%、ClawHub 0%",
          "评测绑定 versionId；旧版本 / 未评测版本可能为空"]),
    ]
    xs = [0.035, 0.510]
    ys = [0.135, 0.465]
    cw, ch = 0.455, 0.300
    for i, (num, title, sub, items) in enumerate(cards):
        x = xs[i % 2] * W
        y = ys[i // 2] * H
        add_rect(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, cw * W, ch * H, WHITE, BORDER, 0.75, radius=0.035)
        card_header(s, x, y, num, title, sub, W, H)
        add_list(s, x + 0.015 * W, y + 0.078 * H, cw * W - 0.030 * W, 0.200 * H, items, 9.5)
    add_text(s, 0.035 * W, 0.805 * H, 0.93 * W, 0.028 * H,
             "关键差异：不只是 20 万供给，而是把云端试跑和 TRACE 接进分发；但评测覆盖还不均。", 10, INK, False)


def build_ecosystem(s, W, H):
    add_text(s, 0.035 * W, 0.040 * H, 0.93 * W, 0.055 * H,
             "SkillHub 生态画像：全站社区 68.4%、ClawHub 31.6%，企业是交叉标签",
             24, TITLE_RED, True)
    add_text(s, 0.035 * W, 0.108 * H, 0.90 * W, 0.024 * H,
             "全站社区 + ClawHub 覆盖全站，企业 34.9% 叠加；Top5000 里个人下载份额最高，企业单条最强。", 10, GRAY, False)

    # 01 who supplies (full site; enterprise is an overlay)
    add_text(s, 0.035 * W, 0.145 * H, 0.44 * W, 0.024 * H, "谁在供给：社区 13.7 万，ClawHub 6.3 万，企业 7.0 万", 10.5, INK, True)
    add_text(s, 0.035 * W, 0.168 * H, 0.44 * W, 0.020 * H, "全站 200,419 条 · 来源计数（可重叠）", 8.5, LIGHT_GRAY, False)
    src = [("社区", 137017, 68.4, RED), ("ClawHub", 63402, 31.6, SLATE), ("企业（交叉）", 69938, 34.9, RGBColor(0xCF, 0xD4, 0xDA))]
    for i, (name, count, pct, color) in enumerate(src):
        y = 0.200 * H + i * 0.030 * H
        add_text(s, 0.035 * W, y, 0.095 * W, 0.020 * H, name, 9.5, GRAY, False)
        add_bar(s, 0.132 * W, y + 0.004 * H, 0.145 * W, 0.010 * H, pct / 68.4, color)
        add_text(s, 0.288 * W, y, 0.165 * W, 0.020 * H, f"{count:,} / {pct}%", 8.5, INK, False)
    add_text(s, 0.035 * W, 0.295 * H, 0.44 * W, 0.048 * H,
             "社区 + ClawHub = 200,419，正好覆盖全站；\n"
             "企业是叠加在两者上的交叉标签，三者不能相加。", 8.5, LIGHT_GRAY, False, spacing=1.1)

    # 02 category (full site)
    add_text(s, 0.510 * W, 0.145 * H, 0.44 * W, 0.024 * H, "分类：全站商业 / 专业 / AI / 开发居前", 10.5, INK, True)
    add_text(s, 0.510 * W, 0.168 * H, 0.44 * W, 0.020 * H, "全站 200,403 条 · 条数占比", 8.5, LIGHT_GRAY, False)
    cats = [("商业运营", 15.2), ("专业服务", 11.6), ("AI Agent", 11.2),
            ("开发编程", 10.6), ("内容创作", 9.4), ("设计多媒体", 7.4)]
    for i, (name, pct) in enumerate(cats):
        y = 0.198 * H + i * 0.022 * H
        add_text(s, 0.510 * W, y, 0.085 * W, 0.020 * H, name, 9, GRAY, False)
        add_bar(s, 0.600 * W, y + 0.004 * H, 0.110 * W, 0.009 * H, pct / 15.2,
                RED if i == 0 else RGBColor(0xC9, 0x7A, 0x80))
        add_text(s, 0.720 * W, y, 0.060 * W, 0.020 * H, f"{pct}%", 8.5, INK, False)
    add_text(s, 0.510 * W, 0.332 * H, 0.44 * W, 0.035 * H,
             "其余 6 类 34.7%；12 个内容分类覆盖全站；Pay Skill 10.0% 为多标签，另计。", 8.5, LIGHT_GRAY, False, spacing=1.05)

    # 03 consumption (Top5000)
    add_text(s, 0.035 * W, 0.385 * H, 0.44 * W, 0.024 * H, "消费集中度：Top10 24.2%，Top100 48.9%", 10.5, INK, True)
    add_text(s, 0.035 * W, 0.408 * H, 0.44 * W, 0.020 * H, "Top5000 总下载 1.35 亿 · 中位 7,521", 8.5, LIGHT_GRAY, False)
    kpis = [("3.9%", "Top1 占比"), ("24.2%", "Top10 占比"), ("48.9%", "Top100 占比"), ("77.3%", "Top1000 占比")]
    for i, (num, label) in enumerate(kpis):
        x = 0.035 * W + (i % 2) * 0.220 * W
        y = 0.440 * H + (i // 2) * 0.060 * H
        add_text(s, x, y, 0.120 * W, 0.034 * H, num, 16, RED, True)
        add_text(s, x, y + 0.030 * H, 0.150 * W, 0.020 * H, label, 8.5, GRAY, False)
    add_text(s, 0.035 * W, 0.565 * H, 0.44 * W, 0.040 * H,
             "Top5000 中 1,519 条 installs=0；下载含 CLI / 镜像，不等于使用。", 8.5, LIGHT_GRAY, False, spacing=1.05)

    # 04 who gets downloaded (median)
    add_text(s, 0.510 * W, 0.385 * H, 0.44 * W, 0.024 * H, "谁被下载：企业 > 个人 > 镜像", 10.5, INK, True)
    add_text(s, 0.510 * W, 0.408 * H, 0.44 * W, 0.020 * H, "Top5000 · 单条中位下载", 8.5, LIGHT_GRAY, False)
    rows = [("企业", 12725, 633, RED), ("个人 / 社区", 8730, 1245, SLATE),
            ("镜像 ClawHub", 6756, 3122, RGBColor(0xCF, 0xD4, 0xDA))]
    for i, (name, median, count, color) in enumerate(rows):
        y = 0.445 * H + i * 0.055 * H
        add_text(s, 0.510 * W, y, 0.095 * W, 0.020 * H, name, 9.5, GRAY, False)
        add_bar(s, 0.615 * W, y + 0.004 * H, 0.120 * W, 0.011 * H, median / 12725, color)
        add_text(s, 0.745 * W, y, 0.185 * W, 0.020 * H, f"{median:,} / {count} 条", 8.5, INK, False)
    add_text(s, 0.510 * W, 0.590 * H, 0.44 * W, 0.032 * H,
             "Top5000 整体中位 7,521；企业单条最高，个人高于镜像。2,883 个上架方，Top10 占 37.9% 下载。", 8.5, LIGHT_GRAY, False, spacing=1.05)

    # 05 paid + API key (full site)
    add_text(s, 0.035 * W, 0.635 * H, 0.90 * W, 0.024 * H, "付费与 API Key：全站 10.0% / 19.3%，Top5000 付费仅 1.0%", 10.5, INK, True)
    add_text(s, 0.035 * W, 0.658 * H, 0.90 * W, 0.020 * H, "全站 200,403 条；Pay Skill 20,125、API Key 38,646", 8.5, LIGHT_GRAY, False)
    add_text(s, 0.035 * W, 0.682 * H, 0.090 * W, 0.036 * H, "10.0%", 16, RED, True)
    add_text(s, 0.035 * W, 0.716 * H, 0.130 * W, 0.020 * H, "Pay Skill", 8.5, GRAY, False)
    add_text(s, 0.180 * W, 0.682 * H, 0.090 * W, 0.036 * H, "19.3%", 16, RED, True)
    add_text(s, 0.180 * W, 0.716 * H, 0.130 * W, 0.020 * H, "API Key", 8.5, GRAY, False)
    add_text(s, 0.350 * W, 0.682 * H, 0.60 * W, 0.060 * H,
             "付费标签 17,123（8.5%）、支付宝 2,901（1.4%）；Pay Skill 且 API Key 331 条。\n"
             "Top5000：付费 1.0%（50 条）、API Key 28.8%；Pay Skill 分类 0 条。",
             8.5, LIGHT_GRAY, False, spacing=1.1)

    add_text(s, 0.035 * W, 0.845 * H, 0.93 * W, 0.028 * H,
             "读法：全站社区 + ClawHub 覆盖全站，企业 34.9% 是叠加；Top5000 里企业单条最强，付费只有 1%。", 10, INK, False)


def main():
    prs = Presentation(SRC)
    W, H = prs.slide_width, prs.slide_height
    old_ids = [prs.slides[2].slide_id, prs.slides[3].slide_id, prs.slides[4].slide_id]

    s = prs.slides.add_slide(prs.slide_layouts[0])
    for ph in list(s.shapes):
        ph._element.getparent().remove(ph._element)
    build_capabilities(s, W, H)
    a = prs.slides._sldIdLst[-1]
    prs.slides._sldIdLst.remove(a)
    prs.slides._sldIdLst.insert(2, a)

    s = prs.slides.add_slide(prs.slide_layouts[0])
    for ph in list(s.shapes):
        ph._element.getparent().remove(ph._element)
    build_ecosystem(s, W, H)
    b = prs.slides._sldIdLst[-1]
    prs.slides._sldIdLst.remove(b)
    prs.slides._sldIdLst.insert(3, b)

    for oid in old_ids:
        sld = next(x for x in list(prs.slides._sldIdLst) if x.id == oid)
        prs.part.drop_rel(sld.get(R_NS + "id"))
        prs.slides._sldIdLst.remove(sld)

    prs.save(SRC)
    print("saved", SRC, "slides", len(prs.slides))


if __name__ == "__main__":
    main()
