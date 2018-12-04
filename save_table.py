from PIL import Image, ImageDraw, ImageFont


def save_tables(tables: dict) -> None:
    font = ImageFont.truetype("/usr/share/fonts/TTF/Roboto-Light.ttf", 40)

    images = []

    for name, table in tables.items():
        img = Image.new('RGB', (2970, 2100), color='white')
        images.append(img)
        dr = ImageDraw.Draw(img)

        dr.rectangle([135, 950, (135 + 90 * len(table)), 1150],
                     fill='grey', outline='black',
                     width=2)
        midlle_cord = ((135 + 90 * len(table)) - 135) // 2
        dr.text((midlle_cord, 1000), name, (0, 0, 0), font=font)

        for idx, row in enumerate(table):
            rotated_text = add_text(row[1].name, font)
            img.paste(rotated_text, (180 + (idx * 90), 500), rotated_text)
            rotated_text_pair = add_text(row[0].name, font, cc=True)
            img.paste(rotated_text_pair,
                      (180 + (idx * 90), 1250), rotated_text_pair)

#    rotated_text = add_text("test", font)
#    img.paste(rotated_text, (200, 100), rotated_text)

    pdf_name = 'tables.pdf'
    print(f"Saving tables to {pdf_name}")
    first_table = images[0]
    first_table.save(pdf_name, save_all=True, append_images=images[1:])


def add_text(text: str, font, cc=False) -> Image:
    txt = Image.new('RGBA', (350, 50), (0, 0, 0, 0))
    d = ImageDraw.Draw(txt)
    d.text((0, 0), text, (0, 0, 0), font=font)
    if cc:
        w = txt.rotate(290, expand=1)
    else:
        w = txt.rotate(70, expand=1)
    return w
