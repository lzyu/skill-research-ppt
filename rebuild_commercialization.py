"""Replace the final two pages with a styled commercialization summary + implications."""
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

from redesign_lifecycle import add_rect, add_text, set_run

SRC = "skill-final-v1.pptx"
RED = RGBColor(0xB5, 0x33, 0x3B)
TITLE_RED = RGBColor(0xC7, 0x00, 0x0B)
INK = RGBColor(0x1A, 0x1A, 0x1C)
GRAY = RGBColor(0x5B, 0x61, 0x6B)
LIGHT_GRAY = RGBColor(0x8B, 0x8E, 0x94)
BORDER = RGBColor(0xE2, 0xE4, 0xE7)
BAND = RGBColor(0xF7, 0xF8, 0xFA)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
R_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def remove_last_two(prs):
    for sld in list(prs.slides)[-2:]:
        slide_id = sld.slide_id
        sld_id = next(x for x in list(prs.slides._sldIdLst) if x.id == slide_id)
        prs.part.drop_rel(sld_id.get(R_NS + "id"))
        prs.slides._sldIdLst.remove(sld_id)


def set_cell_border(cell, color="000000", width=6350):
    tc_pr = cell._tc.get_or_add_tcPr()
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        ln = tc_pr.find(qn(tag))
        if ln is None:
            ln = tc_pr.makeelement(qn(tag), {})
            tc_pr.append(ln)
        ln.set("w", str(width))
        ln.set("cap", "flat")
        ln.set("cmpd", "sng")
        ln.set("algn", "ctr")
        for child in list(ln):
            ln.remove(child)
        solid = ln.makeelement(qn("a:solidFill"), {})
        clr = solid.makeelement(qn("a:srgbClr"), {"val": color})
        solid.append(clr)
        ln.append(solid)
        dash = ln.makeelement(qn("a:prstDash"), {"val": "solid"})
        ln.append(dash)


def add_table(slide, W, H, x, y, w, h, data, col_widths):
    rows, cols = len(data), len(data[0])
    shape = slide.shapes.add_table(rows, cols, int(x), int(y), int(w), int(h))
    table = shape.table
    table.first_row = True
    table.horz_banding = False
    for i, cw in enumerate(col_widths):
        table.columns[i].width = int(cw)
    table.rows[0].height = int(0.055 * H)
    for r in range(1, rows):
        table.rows[r].height = int((h - 0.055 * H) / (rows - 1))
    for r, row in enumerate(data):
        for c, value in enumerate(row):
            cell = table.cell(r, c)
            cell.margin_left = Inches(0.04)
            cell.margin_right = Inches(0.04)
            cell.margin_top = Inches(0.02)
            cell.margin_bottom = Inches(0.02)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = RED if r == 0 else WHITE
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            p.line_spacing = 1.0
            run = p.add_run()
            run.text = value
            set_run(run, 9 if r == 0 else 8.5, WHITE if r == 0 else INK, r == 0)
            set_cell_border(cell)
    return table


def build_summary(prs, W, H):
    s = prs.slides.add_slide(prs.slide_layouts[0])
    for ph in list(s.shapes):
        ph._element.getparent().remove(ph._element)

    add_text(s, 0.04 * W, 0.045 * H, 0.92 * W, 0.06 * H,
             "两个平台的商业化：阿里卖商品权益，腾讯连付费服务",
             24, TITLE_RED, True)

    data = [
        ["维度", "阿里：SkillPay + MachinePay", "腾讯：SkillHub SkillPay"],
        ["卖什么", "Skill 商品/权益：买断源码、订阅云端；MachinePay 按次 API / MCP 资源",
         "Skill 包负责发现与调用；远程服务按次收费，如 WorkRally 0.36 元/次"],
        ["平台角色", "商品化、试用/版本/权益、402 支付、云端保护、退款",
         "企业认证、商户绑定、开发者签名、定价审核、分发"],
        ["交易与履约", "402 报价 → 付款凭证 → 验付 → 履约回执；商户做幂等与业务核对",
         "微信订单 → AI 支付码 → payment_code → payment_id；商户验付后交付"],
        ["收入", "开发者定价、资金直达；平台费率未公开",
         "平台技术服务费暂免；服务商从远程服务变现"],
        ["值得借鉴", "先定义购买权益与交付形态，再做试用、续购与持续更新",
         "保留低门槛安装入口，把收费放在持续服务端"],
    ]
    add_table(s, W, H, 0.04 * W, 0.135 * H, 0.92 * W, 0.435 * H, data,
              [0.14 * W, 0.43 * W, 0.43 * W])

    cards = [
        ("阿里：商品经营", "买断 / 订阅 / 试用 / 退款 + 402 验付；强在权益与交付；平台费率未公开。"),
        ("腾讯：服务入口", "免费包 + 远程按次 + 微信支付；强在分发与商户连接；平台技术服务费暂免。"),
        ("共同待解", "费率、结算、退款、质量；公开信息不足，需按协议核实；不要把示例当全量。"),
    ]
    cw = 0.29 * W
    for i, (head, body) in enumerate(cards):
        x = 0.04 * W + i * 0.31 * W
        add_rect(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 0.615 * H, cw, 0.175 * H, WHITE, BORDER, 0.75, radius=0.05)
        add_text(s, x + 0.012 * W, 0.627 * H, cw - 0.024 * W, 0.026 * H, head, 12, INK, True)
        add_text(s, x + 0.012 * W, 0.660 * H, cw - 0.024 * W, 0.115 * H, body, 10, GRAY, False, spacing=1.2)

    add_text(s, 0.04 * W, 0.815 * H, 0.92 * W, 0.035 * H,
             "一句话：阿里把 Skill 变成商品，腾讯把 Skill 变成付费服务的入口。",
             12, INK, True)
    add_text(s, 0.04 * W, 0.865 * H, 0.045 * W, 0.022 * H, "判断", 9.5, RED, True)
    add_text(s, 0.088 * W, 0.865 * H, 0.87 * W, 0.024 * H,
             "阿里证明 Skill 可以商品化，腾讯证明 Skill 可以服务化；智果园要选一条能对账的路径。",
             10, GRAY, False)


def build_implications(prs, W, H):
    s = prs.slides.add_slide(prs.slide_layouts[0])
    for ph in list(s.shapes):
        ph._element.getparent().remove(ph._element)

    add_text(s, 0.04 * W, 0.045 * H, 0.92 * W, 0.06 * H,
             "对智果园的启示：补商业编排，而不是再堆资产",
             24, TITLE_RED, True)

    cards = [
        ("01", "先定义卖什么",
         "买断、订阅、按次三种形态并存；商品是权益，不是文件；先定 SKU、价格、许可与版本；试用、续购、更新要连成经营。先做一个可售 SKU 试点，再扩品类。"),
        ("02", "把交易接进任务",
         "402/支付凭证/验付/履约，或微信支付码/回调；支付成功 ≠ 交付成功；重试不重复扣费；已付未交付可恢复。把支付、权益、履约写成状态机。"),
        ("03", "平台做可信中介",
         "企业认证、开发者签名、版本/许可、退款/争议；上架补质量与收费测试；订单、收益、退款要能对账。把作者收益、退款、申诉产品化。"),
        ("04", "智果园的差异化",
         "复用 AI 资产广场供给 + CodeArts Agent 宿主；先做行业标杆，不追规模；首期免费入口 + 付费远程能力。先用 3–5 个行业标杆验证。"),
    ]
    cw, ch = 0.45 * W, 0.21 * H
    for i, (num, head, body) in enumerate(cards):
        x = 0.035 * W + (i % 2) * 0.48 * W
        y = 0.14 * H + (i // 2) * 0.235 * H
        add_rect(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, cw, ch, WHITE, BORDER, 0.75, radius=0.05)
        add_text(s, x + 0.014 * W, y + 0.012 * H, 0.028 * W, 0.026 * H, num, 12, RED, True)
        add_text(s, x + 0.044 * W, y + 0.012 * H, cw - 0.060 * W, 0.030 * H, head, 12, INK, True)
        add_text(s, x + 0.014 * W, y + 0.055 * H, cw - 0.028 * W, 0.135 * H, body, 10, GRAY, False, spacing=1.25)

    # First-phase path
    strip_y, strip_h = 0.635 * H, 0.135 * H
    add_rect(s, MSO_SHAPE.ROUNDED_RECTANGLE, 0.035 * W, strip_y, 0.93 * W, strip_h, BAND, BORDER, 0.75, radius=0.04)
    add_text(s, 0.050 * W, strip_y + 0.012 * H, 0.16 * W, 0.024 * H, "首期路径", 9, RED, True)
    steps = [
        ("发现 / 安装", "免费 Skill 入口"),
        ("绑定", "资产 / 版本"),
        ("试用 / 购买", "商品 / 订单 / 买家"),
        ("服务端验权", "限额 / 有效期"),
        ("执行 / 计量", "同一任务一次消费"),
        ("交付 / 对账", "恢复 / 补偿 / 售后"),
    ]
    sw = 0.135 * W
    for i, (label, body) in enumerate(steps):
        x = 0.050 * W + i * 0.148 * W
        add_text(s, x, strip_y + 0.040 * H, sw, 0.020 * H, label, 9.5, INK, True)
        add_text(s, x, strip_y + 0.064 * H, sw, 0.050 * H, body, 9, GRAY, False, spacing=1.0)
        if i < len(steps) - 1:
            add_rect(s, MSO_SHAPE.RIGHT_ARROW, x + sw + 0.002 * W, strip_y + 0.060 * H,
                     0.010 * W, 0.010 * H, RED, None, radius=0.3)

    add_text(s, 0.04 * W, 0.805 * H, 0.92 * W, 0.050 * H,
             "首期建议：免费 Skill 入口 + 付费远程能力，先跑通一条可对账的交易闭环。",
             12, INK, True)
    add_text(s, 0.04 * W, 0.860 * H, 0.92 * W, 0.040 * H,
             "验收以付费任务履约为准：重复请求不重复扣费，已付未交付可恢复，退款与权益、账单一致。",
             10, GRAY, False)


def main():
    prs = Presentation(SRC)
    W, H = prs.slide_width, prs.slide_height
    remove_last_two(prs)
    build_summary(prs, W, H)
    build_implications(prs, W, H)
    prs.save(SRC)
    print("saved", SRC, "slides", len(prs.slides))


if __name__ == "__main__":
    main()
