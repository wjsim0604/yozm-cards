from PIL import Image, ImageDraw, ImageFont
import sys, os

OUT = sys.argv[1]
W, H = 1080, 1350
BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
MED = "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc"
BLK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"


def kr_index(path):
    for i in range(12):
        try:
            f = ImageFont.truetype(path, 20, index=i)
            if "KR" in " ".join(f.getname()):
                return i
        except Exception:
            break
    return 0


IDX = {p: kr_index(p) for p in (BOLD, REG, MED, BLK)}


def font(path, size):
    return ImageFont.truetype(path, size, index=IDX[path])


def wrap(draw, text, fnt, maxw):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            # word itself too long -> split by char
            if draw.textlength(word, font=fnt) > maxw:
                piece = ""
                for ch in word:
                    if draw.textlength(piece + ch, font=fnt) <= maxw:
                        piece += ch
                    else:
                        lines.append(piece)
                        piece = ch
                cur = piece
            else:
                cur = word
    if cur:
        lines.append(cur)
    return lines


TOTAL = 9
DATE = "2026.11.26 (목)"

cards = [
    dict(kind="cover"),
    dict(tag="경제 · 무역", bg=(14, 40, 84), accent=(255, 196, 61), n=2,
         title="미국 ‘과잉생산 관세’ 예고,\n한국엔 15% 상한 제시",
         bullets=[
             "미 무역대표부가 한국 등 14개 경제주체에 과잉생산을 이유로 관세 부과를 예고했어요",
             "기존 합의의 15% 상한이 기준이지만, 협의·이행 결과에 따라 25%까지 오를 수 있다고 밝혔어요",
             "한국은행은 기준금리를 0.25%p 올려 3.25%로 정했어요 (만장일치는 아님)",
         ],
         why="수출 기업도, 대출 이자를 내는 우리도 직접 영향"),
    dict(tag="증시 · AI", bg=(20, 28, 48), accent=(86, 220, 190), n=3,
         title="AI·반도체 주가,\n오르락내리락 큰 장",
         bullets=[
             "나스닥은 약세장 문턱에서 반등했고, 일본 닛케이도 AI·반도체주 저가 매수로 올랐어요",
             "미국 수출통제 강화로 엔비디아가 동남아 4개국 서버 출하를 멈췄다는 보도가 나왔어요",
             "코스피는 17일 5,000선이 무너졌다가 18일 되찾는 등 등락이 컸어요",
         ],
         why="AI 투자 열기와 규제 리스크가 동시에 커졌어요"),
    dict(tag="세금 · 부동산", bg=(70, 28, 40), accent=(255, 150, 120), n=4,
         title="종부세 대상 82만 명,\n1년 새 19만 명 늘었다",
         bullets=[
             "종부세 대상은 올해 약 30% 늘었고, 1주택자 세 부담은 두 배 가까이 커졌어요",
             "증가액의 85%는 서울에 몰려 있어요",
             "공시가 현실화율을 묶어도 내년 보유세는 강남3구 주요 단지 기준 30% 안팎 오를 전망이에요",
         ],
         why="고지서가 나오는 연말, 집 가진 사람들의 최대 관심사"),
    dict(tag="쇼핑", bg=(24, 24, 28), accent=(255, 214, 10), n=5,
         title="블랙프라이데이 D-1,\n직구 전 체크리스트",
         bullets=[
             "블랙프라이데이는 11월 27일(금), 사이버먼데이는 11월 30일(월)이에요",
             "직구는 개인통관고유부호가 필요하고, 배송비·세금까지 합친 총비용을 비교하세요",
             "미국발 목록통관 물품은 200달러 이하 면세 기준이 적용돼요",
         ],
         why="연중 최대 할인 시즌, 환율·관세 탓에 ‘진짜 할인’ 따지는 중"),
    dict(tag="생활 이슈", bg=(34, 56, 44), accent=(190, 240, 120), n=6,
         title="파업·휴업 소식\n줄줄이 이어진다",
         bullets=[
             "LH가 창사 첫 총파업을 앞두고 12월 1일 마지막 협상에 나서요",
             "전남광주 학교 비정규직 2,064명이 27일 파업해 451개교 급식 차질이 우려돼요",
             "홈플러스는 27일부터 전 점포 임시 영업을 중단해요",
             "철도노조는 12월 10일 무기한 총파업을 예고했어요",
         ],
         why="당장 내일 출근·급식·장보기에 영향이 있어요"),
    dict(tag="연예 · 콘텐츠", bg=(58, 30, 90), accent=(255, 130, 200), n=7,
         title="OTT·드라마·MAMA,\n연말 콘텐츠 열기",
         bullets=[
             "티빙 11월 첫째 주 집계에서 ‘100일의 거짓말’이 3주 연속 종합·드라마 1위였어요",
             "디즈니+ ‘재혼 황후’는 공개 이후에도 온라인 반응이 이어졌어요",
             "2026 MAMA AWARDS가 오사카에서 열려 팬 페스타 정보도 화제예요",
         ],
         why="※ 최근 주간 집계 기준이라 오늘 순위와는 다를 수 있어요"),
    dict(kind="outro"),
    dict(kind="follow"),
]


def base(bg):
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    return img, d


def footer(d, n, fg):
    d.text((70, 1262), "@yozm.mwobom", font=font(BOLD, 32), fill=fg)
    t = f"{n} / {TOTAL}"
    d.text((W - 70 - d.textlength(t, font=font(BOLD, 30)), 1262), t, font=font(BOLD, 30), fill=fg)


def draw_card(c, i):
    kind = c.get("kind")
    if kind == "cover":
        img, d = base((255, 214, 10))
        dark = (20, 20, 24)
        d.text((70, 90), DATE, font=font(BOLD, 44), fill=dark)
        d.text((70, 300), "오늘의", font=font(BLK, 170), fill=dark)
        d.text((70, 490), "관심사", font=font(BLK, 170), fill=dark)
        d.rounded_rectangle((70, 760, 70 + 560, 760 + 12), 6, fill=dark)
        sub = wrap(d, "관세·증시·세금부터 블프·파업·연예까지,\n사람들이 오늘 가장 많이 보는 6가지".replace("\n", " "), font(MED, 46), 900)
        y = 810
        for ln in sub:
            d.text((70, y), ln, font=font(MED, 46), fill=dark)
            y += 70
        d.text((70, 1180), "옆으로 넘겨보세요  →", font=font(BOLD, 40), fill=dark)
        footer(d, 1, dark)
        return img
    if kind == "follow":
        img, d = base((255, 214, 10)); dark = (20, 20, 24)
        d.text((70, 90), "마지막 한 장", font=font(BOLD, 40), fill=dark)
        y = 250
        for ln in ("팔로우하면", "소식을 빠르게", "볼 수 있어요"):
            d.text((70, y), ln, font=font(BLK, 118), fill=dark); y += 160
        y += 50
        d.rounded_rectangle((70, y, 630, y + 12), 6, fill=dark); y += 60
        for ln in wrap(d, "매일 아침, 오늘 사람들이 많이 보는 주제를 카드로 정리해 드려요.", font(MED, 44), 900):
            d.text((70, y), ln, font=font(MED, 44), fill=dark); y += 66
        # follow pill
        hf = font(BOLD, 52); handle = "@yozm.mwobom"
        hw = d.textlength(handle, font=hf)
        d.rounded_rectangle((70, 1030, 70 + hw + 90, 1130), 50, fill=dark)
        d.text((115, 1043), handle, font=hf, fill=(255, 214, 10))
        d.text((70, 1170), "저장해 두고, 친구에게도 공유해 보세요", font=font(BOLD, 36), fill=dark)
        footer(d, TOTAL, dark); return img
    if kind == "outro":
        img, d = base((20, 20, 24))
        fg = (255, 255, 255)
        acc = (255, 214, 10)
        d.text((70, 90), "마무리", font=font(BOLD, 40), fill=acc)
        d.text((70, 170), "오늘의 한 줄", font=font(BLK, 84), fill=fg)
        lines = wrap(d, "관세·금리·세금 같은 ‘내 지갑’ 이슈와 블프·파업 같은 ‘당장 내일’ 이슈가 오늘의 중심이에요.", font(MED, 44), 940)
        y = 320
        for ln in lines:
            d.text((70, y), ln, font=font(MED, 44), fill=fg)
            y += 68
        y += 50
        d.rounded_rectangle((70, y, W - 70, y + 4), 2, fill=(70, 70, 76))
        y += 40
        d.text((70, y), "출처", font=font(BOLD, 38), fill=acc)
        y += 70
        srcs = [
            "뉴스핌 · 데일리티 · 네이트뉴스 (11/26 주요 뉴스)",
            "뉴스스콰크 유럽장 개장 데일리 뉴스 (11/26)",
            "KB Think · 이노 블랙프라이데이 일정 안내",
            "KB증권 장마감 코멘트 (11/17·11/18)",
            "CJ ENM 티빙 TOP5 · 톱스타뉴스 (11월)",
        ]
        for s in srcs:
            for ln in wrap(d, "· " + s, font(REG, 33), 940):
                d.text((70, y), ln, font=font(REG, 33), fill=(200, 200, 206))
                y += 50
        y += 20
        for ln in wrap(d, "실시간 검색 순위가 아닌 보도·집계 기반 정리이며, 내용은 직접 요약했어요.", font(REG, 30), 940):
            d.text((70, y), ln, font=font(REG, 30), fill=(150, 150, 158))
            y += 46
        footer(d, 8, (150, 150, 158))
        return img

    bg, acc = c["bg"], c["accent"]
    img, d = base(bg)
    fg = (255, 255, 255)
    # tag pill
    tf = font(BOLD, 38)
    tw = d.textlength(c["tag"], font=tf)
    d.rounded_rectangle((70, 80, 70 + tw + 60, 80 + 74), 37, fill=acc)
    d.text((100, 92), c["tag"], font=tf, fill=bg)
    # title
    y = 210
    tfont = font(BLK, 72)
    for part in c["title"].split("\n"):
        for ln in wrap(d, part, tfont, 940):
            d.text((70, y), ln, font=tfont, fill=fg)
            y += 100
    y += 20
    d.rounded_rectangle((70, y, 70 + 140, y + 10), 5, fill=acc)
    y += 50
    # bullets
    bf = font(MED, 40)
    for k, b in enumerate(c["bullets"], 1):
        r = 24
        d.ellipse((70, y + 6, 70 + 2 * r, y + 6 + 2 * r), fill=acc)
        nf = font(BOLD, 30)
        nt = str(k)
        d.text((70 + r - d.textlength(nt, font=nf) / 2, y + 6 + r - 21), nt, font=nf, fill=bg)
        lines = wrap(d, b, bf, 840)
        ly = y
        for ln in lines:
            d.text((140, ly), ln, font=bf, fill=fg)
            ly += 58
        y = ly + 28
    # why box
    bh = 150
    by = 1130 - bh + 10
    d.rounded_rectangle((70, by, W - 70, by + bh), 28, fill=tuple(min(255, v + 28) for v in bg))
    d.text((105, by + 22), "왜 지금?", font=font(BOLD, 30), fill=acc)
    wl = wrap(d, c["why"], font(MED, 36), 870)
    wy = by + 68
    for ln in wl:
        d.text((105, wy), ln, font=font(MED, 36), fill=fg)
        wy += 50
    footer(d, c["n"], (230, 230, 235))
    return img, y


for i, c in enumerate(cards, 1):
    res = draw_card(c, i)
    if isinstance(res, tuple):
        img, endy = res
        print(i, "content ends at y=", endy)
    else:
        img = res
    img.save(os.path.join(OUT, f"card_{i:02d}.png"))
print("done")
