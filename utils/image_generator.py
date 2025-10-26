from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from datetime import datetime
from core.config import SUMMARY_IMAGE_PATH

def generate_summary_image(countries):
    top_countries = sorted(
        [c for c in countries if c["estimated_gdp"]],
        key=lambda x: x["estimated_gdp"],
        reverse=True
    )[:5]

    width, height = 1000, 600
    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arial.ttf", 36)
        text_font = ImageFont.truetype("arial.ttf", 24)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    padding = 20
    y = padding

    draw.text((padding, y), "Countries Summary", fill="black", font=title_font)
    y += 60

    draw.text((padding, y), f"Total countries: {len(countries)}", fill="black", font=text_font)
    y += 40

    flag_size = (50, 30)
    for c in top_countries:
        try:
            response = requests.get(c["flag_url"], timeout=5)
            flag = Image.open(BytesIO(response.content)).convert("RGB")
            flag.thumbnail(flag_size)
            img.paste(flag, (padding, y))
        except:
            pass

        draw.text((padding + flag_size[0] + 5, y), "Top five countries by GDP: ")
        draw.text((padding + flag_size[0] + 15, y), f"{c['name']} - GDP: {c['estimated_gdp']:.2f}", fill="black", font=text_font)
        y += max(flag_size[1], 30) + 10

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw.text((padding, height - 40), f"Last refreshed: {timestamp}", fill="black", font=text_font)

    return img.save(SUMMARY_IMAGE_PATH)
