import textwrap
from PIL import Image, ImageDraw, ImageFont


def generate_image_macro(image_path,
                         top_text,
                         bottom_text,
                         font_path='./fonts/impact.ttf',
                         font_size=9,
                         stroke_width=5):
    
    # load image
    im = Image.open(image_path)
    draw = ImageDraw.Draw(im)
    image_width, image_height = im.size

    # load font
    font = ImageFont.truetype(font=font_path,
                              size=int(image_height * font_size) // 100)

    # convert text to uppercase
    top_text = top_text.upper()
    bottom_text = bottom_text.upper()

    # função auxiliar para pegar largura e altura do texto
    def get_text_size(text, font):
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return width, height

    # text wrapping
    char_width, char_height = get_text_size('A', font)
    chars_per_line = image_width // char_width
    top_lines = textwrap.wrap(top_text, width=chars_per_line)
    bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line)

    # draw top lines
    y = 10
    for line in top_lines:
        line_width, line_height = get_text_size(line, font)
        x = (image_width - line_width) / 2
        draw.text((x, y),
                  line,
                  fill='white',
                  font=font,
                  stroke_width=stroke_width,
                  stroke_fill='black')
        y += line_height

    # draw bottom lines
    y = image_height - char_height * len(bottom_lines) - 0.20 * char_height * (
        len(bottom_lines) - 1) - 15
    for line in bottom_lines:
        line_width, line_height = get_text_size(line, font)
        x = (image_width - line_width) / 2
        draw.text((x, y),
                  line,
                  fill='white',
                  font=font,
                  stroke_width=stroke_width,
                  stroke_fill='black')
        y += line_height
    
    return im
