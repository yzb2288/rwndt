from PIL import Image, ImageDraw, ImageFont

if __name__ == "__main__":
    font_size=32
    unicode_text ="✨"
    im = Image.open("hud_laptop_gps.png")
    draw = ImageDraw.Draw(im)
    unicode_font = ImageFont.truetype("seguiemj.ttf", font_size)
    draw.text((60,4), unicode_text, font=unicode_font, fill=(255, 255, 255), stroke_width=1.2, stroke_fill=(0, 0, 0), embedded_color=False)
    im.show()
    im.save("hud_laptop_gps_with_emoji.ico", format="ICO", sizes=[im.size])
