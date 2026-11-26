from PIL import Image, ImageDraw, ImageFont
BLK="/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
def f(size):
    for i in range(12):
        x=ImageFont.truetype(BLK,size,index=i)
        if "KR" in " ".join(x.getname()): return x
S=1080
img=Image.new("RGB",(S,S),(255,214,10)); d=ImageDraw.Draw(img)
dark=(20,20,24)
ft=f(290)
for t,y in (("요즘",170),("뭐봄",490)):
    w=d.textlength(t,font=ft)
    d.text(((S-w)/2,y),t,font=ft,fill=dark)
# eye-dot motif: small dark pill under text
d.rounded_rectangle((S/2-110,900,S/2+110,916),8,fill=dark)
img.save("/home/claude/cards/profile_yozm.png")
# circle preview
m=Image.new("L",(S,S),0); ImageDraw.Draw(m).ellipse((0,0,S,S),fill=255)
bg=Image.new("RGB",(S,S),(255,255,255)); bg.paste(img,(0,0),m)
bg.resize((400,400)).save("/home/claude/gen/profile_preview.png")
