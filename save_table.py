from PIL import Image, ImageDraw, ImageFont
from person import Person


def save_tables(tables: dict, allergies=False) -> None:
    font = ImageFont.truetype("/usr/share/fonts/TTF/Roboto-Light.ttf", 40)

    images = []

    for name, table in tables.items():
        img = Image.new('RGB', (2970, 2100), color='white')
        images.append(img)
        dr = ImageDraw.Draw(img)

        dr.rectangle([135, 950, (135 + 90 * len(table)), 1150],
                     fill=(211, 211, 211), outline='black',
                     width=2)
        midlle_cord = ((135 + 90 * len(table)) - 135) // 2
        dr.text((midlle_cord, 1020), name.upper(), (0, 0, 0), font=font)
        allergy_table = {}

        for idx, row in enumerate(table):
            color = add_allergy(row[1],
                                allergy_table) if allergies else (0, 0, 0)
            rotated_text = add_text(row[1], font, color)
            img.paste(rotated_text, (180 + (idx * 90), 500), rotated_text)
            color = add_allergy(row[0],
                                allergy_table) if allergies else (0, 0, 0)
            rotated_text_pair = add_text(row[0], font, color, cc=True)
            img.paste(rotated_text_pair,
                      (180 + (idx * 90), 1250), rotated_text_pair)

        other_allergies = allergy_table.pop('other', None)
        if other_allergies is not None:
            other_allergies = ", ".join(other_allergies)
            allergy_table[other_allergies] = (255, 69, 0)
        x_cord = 10
        for allerg, color in allergy_table.items():
            dr.text((20, x_cord), allerg, color, font=font)
            x_cord += 50
    pdf_name = 'tables.pdf'
    print(f"Saving tables to {pdf_name}")
    first_table = images[0]
    first_table.save(pdf_name, save_all=True, append_images=images[1:])


def add_text(person: Person, font, color, cc=False) -> Image:
    txt = Image.new('RGBA', (350, 50), (0, 0, 0, 0))
    d = ImageDraw.Draw(txt)
    d.text((0, 0), person.name, color, font=font)
    if cc:
        w = txt.rotate(290, expand=1)
    else:
        w = txt.rotate(70, expand=1)
    return w


def add_allergy(person: Person, allergy_table: dict) -> tuple:
    if person.allergies is not None:
        allerg = person.allergies.lower()
        if len(allerg.split(" ")) > 2:
            allergy_table['multiple'] = (128, 0, 0)
            return (128, 0, 0)
        if 'glut' in allerg:
            allergy_table['glutenfree'] = (204, 204, 0)
            return (204, 204, 0)
        elif 'lakt' in allerg:
            allergy_table['lactosefree'] = (30, 144, 255)
            return (30, 144, 255)
        elif 'mjölk' in allerg:
            allergy_table['milkfree'] = (0, 0, 139)
            return (0, 0, 139)
        elif 'vege' in allerg:
            allergy_table['vegetarian'] = (50, 205, 50)
            return (50, 205, 50)
        elif 'vegan' in allerg:
            allergy_table['vegan'] = (0, 100, 0)
            return (0, 100, 0)
        else:
            if 'other' not in allergy_table:
                allergy_table['other'] = {allerg}
            else:
                allergy_table['other'].add(allerg)
            return (255, 69, 0)
    else:
        return (0, 0, 0)
