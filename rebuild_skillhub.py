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
             "SkillHub 生态画像：Top1000 里，开发类拿走 21.8% 下载，付费标签仅 0.9%",
             24, TITLE_RED, True)
    add_text(s, 0.035 * W, 0.110 * H, 0.40 * W, 0.026 * H, "生态画像：Top1000 下载头部", 12, INK, True)

    # 01 supply sources
    add_text(s, 0.035 * W, 0.150 * H, 0.44 * W, 0.024 * H, "谁在供给：ClawHub 数量最多，社区拿走最多下载", 10.5, INK, True)
    add_text(s, 0.035 * W, 0.174 * H, 0.44 * W, 0.020 * H, "Top1000 条 · 数量占比 / 下载占比", 8.5, LIGHT_GRAY, False)
    src = [("ClawHub", 44.7, "27.0%"), ("社区", 30.5, "44.2%"), ("企业", 24.8, "28.8%")]
    for i, (name, pct, dl) in enumerate(src):
        y = 0.212 * H + i * 0.040 * H
        add_text(s, 0.035 * W, y, 0.085 * W, 0.020 * H, name, 9.5, GRAY, False)
        add_bar(s, 0.125 * W, y + 0.004 * H, 0.170 * W, 0.011 * H, pct / 44.7,
                RED if i == 1 else RGBColor(0x9A, 0xA1, 0xAA))
        add_text(s, 0.310 * W, y, 0.165 * W, 0.020 * H, f"{pct}% / {dl}", 9, INK, False)
    add_text(s, 0.035 * W, 0.340 * H, 0.44 * W, 0.050 * H,
             "社区 = 个人/社区作者；ClawHub = 外部同步；企业 = 认证企业。\n"
             "Top1000 里 ClawHub 条数最多，但下载份额低于社区。", 8.5, LIGHT_GRAY, False, spacing=1.15)

    # 02 category mix
    add_text(s, 0.510 * W, 0.150 * H, 0.44 * W, 0.024 * H, "分类：开发类少而重，AI Agent 多而散", 10.5, INK, True)
    add_text(s, 0.510 * W, 0.174 * H, 0.44 * W, 0.020 * H, "数量占比 / 下载占比", 8.5, LIGHT_GRAY, False)
    cats = [
        ("开发编程", 7.2, 21.8), ("AI Agent", 15.8, 15.4), ("办公效率", 12.7, 10.4),
        ("知识管理", 6.8, 9.5), ("内容创作", 11.8, 9.2), ("设计多媒体", 12.3, 8.1),
    ]
    for i, (name, count_pct, dl_pct) in enumerate(cats):
        y = 0.212 * H + i * 0.030 * H
        add_text(s, 0.510 * W, y, 0.090 * W, 0.020 * H, name, 9, GRAY, False)
        add_bar(s, 0.605 * W, y + 0.004 * H, 0.115 * W, 0.010 * H, count_pct / 15.8,
                RED if i == 0 else RGBColor(0xC9, 0x7A, 0x80))
        add_text(s, 0.730 * W, y, 0.110 * W, 0.020 * H, f"{count_pct}% / {dl_pct}%", 8.5, INK, False)
    add_text(s, 0.510 * W, 0.405 * H, 0.44 * W, 0.022 * H,
             "开发类只占 7.2% 供给，却拿走 21.8% 下载；AI Agent 供给最多，下载占比略低。", 8.5, LIGHT_GRAY, False, spacing=1.05)
    add_text(s, 0.510 * W, 0.432 * H, 0.44 * W, 0.020 * H,
             "其余 6 类合计：33.4% 供给 / 25.6% 下载。", 8.5, LIGHT_GRAY, False)

    # 03 paid + API key
    add_text(s, 0.035 * W, 0.520 * H, 0.44 * W, 0.024 * H, "付费与 API Key：API Key 已三成，付费仍在边缘", 10.5, INK, True)
    add_text(s, 0.035 * W, 0.544 * H, 0.44 * W, 0.020 * H, "Top1000 条 · 条数占比 / 下载占比", 8.5, LIGHT_GRAY, False)
    add_text(s, 0.035 * W, 0.578 * H, 0.115 * W, 0.040 * H, "0.9%", 18, RED, True)
    add_text(s, 0.035 * W, 0.615 * H, 0.150 * W, 0.020 * H, "PaySkill（9 条）", 8.5, GRAY, False)
    add_text(s, 0.240 * W, 0.578 * H, 0.115 * W, 0.040 * H, "30.7%", 18, RED, True)
    add_text(s, 0.240 * W, 0.615 * H, 0.150 * W, 0.020 * H, "API Key（307 条）", 8.5, GRAY, False)
    add_text(s, 0.035 * W, 0.655 * H, 0.44 * W, 0.075 * H,
             "付费下载占比 0.8%；API Key 下载占比 21.6%；付费且 API Key 仅 1 条；\n"
             "Pay Skill 分类在 Top1000 为 0 条。付费标签按 pricing_type=paid/alipay 统计。",
             8.5, LIGHT_GRAY, False, spacing=1.15)

    # 04 concentration
    add_text(s, 0.510 * W, 0.520 * H, 0.44 * W, 0.024 * H, "消费集中度：Top10 拿走 31.3%，Top100 拿走 63.3%", 10.5, INK, True)
    add_text(s, 0.510 * W, 0.544 * H, 0.44 * W, 0.020 * H, "Top1000 总下载约 1.04 亿；中位 32,907", 8.5, LIGHT_GRAY, False)
    kpis = [("31.3%", "Top10 下载占比"), ("63.3%", "Top100 下载占比"), ("443", "installs=0 的条数")]
    for i, (num, label) in enumerate(kpis):
        x = 0.510 * W + i * 0.145 * W
        add_text(s, x, 0.578 * H, 0.130 * W, 0.040 * H, num, 18, RED, True)
        add_text(s, x, 0.615 * H, 0.130 * W, 0.034 * H, label, 8.5, GRAY, False, spacing=1.05)
    add_text(s, 0.510 * W, 0.665 * H, 0.44 * W, 0.060 * H,
             "Top1 占 5.0%，Top3 占 14.7%；下载含 CLI/镜像拉取，不等于安装或使用。", 8.5, LIGHT_GRAY, False, spacing=1.1)

    add_text(s, 0.035 * W, 0.855 * H, 0.93 * W, 0.028 * H,
             "读法：ClawHub 撑数量，社区撑下载，开发类最重；付费仍在边缘，API Key 已是三成供给。", 10, INK, False)


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
