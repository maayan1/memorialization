# import multiprocessing
# import os
# from typing import List
# from pathlib import Path
# from PIL import Image, ImageFont, ImageDraw
#
# from utils.casualty import Casualty, Gender
# from utils.paths import *
#
#
# def get_font(size: int):
#     print(f'in get_font function')
#     """Generated a font object with the required size"""
#     return ImageFont.truetype(
#         "resources/Rubik-Regular.ttf", size, layout_engine=ImageFont.Layout.RAQM
#     )
#
#
# def _get_background(casualty: Casualty):
#     print(f'in _get_background function')
#     """Return a background image, matching the casualty's gender"""
#     backgrounds = {
#         Gender.FEMALE: "resources/female.png",
#         Gender.MALE: "resources/male.png",
#     }
#     if casualty.gender not in backgrounds:
#         raise Exception("Unknown gender")
#     return backgrounds[casualty.gender]
#
#
# def _get_image(casualty: Casualty) -> Image:
#     print('in _get_image function')
#     """Return the casualty's image, opened and resized"""
#     casualty_img = Image.open(
#         casualty.post_main_image
#         if casualty.post_main_image
#         else "resources/no_image_default.jpeg"
#     )
#     width, height = casualty_img.size
#     ratio = height / width
#     wanted_width = 300
#     casualty_img = casualty_img.resize((wanted_width, int(wanted_width * ratio)))
#     return casualty_img
#
#
# def _add_text(
#         text: str,
#         font_size: int,
#         bold: bool,
#         increase_offset: int,
#         draw: ImageDraw.Draw,
#         y_axis_offset: int,
# ):
#     """Add text to the post according to the required parameters"""
#     font = get_font(font_size)
#     left, top, right, bottom = font.getbbox(text)
#     width, height = right - left, top - bottom
#     draw.text(
#         (630 - width, y_axis_offset),
#         text,
#         (255, 255, 255),
#         direction="rtl",
#         align="right",
#         features="rtla",
#         font=font,
#         stroke_width=1 if bold else 0,
#         stroke_fill="white",
#     )
#     y_axis_offset += increase_offset
#     return draw, y_axis_offset
#
#
# def _add_degree(
#         casualty: Casualty, draw: ImageDraw.Draw, y_axis_offset: int
# ) -> ImageDraw.Draw:
#     """Add the casualty's degree to the post"""
#     return _add_text(casualty.degree, 45, False, 50, draw, y_axis_offset)
#
#
# def _add_name(
#         casualty: Casualty, draw: ImageDraw.Draw, y_axis_offset: int
# ) -> ImageDraw.Draw:
#     """Add the casualty's name to the post"""
#     return _add_text(f'{casualty.full_name} ז"ל', 54, True, 65, draw, y_axis_offset)
#
#
# def _add_department(
#         casualty: Casualty, draw: ImageDraw.Draw, y_axis_offset: int
# ) -> ImageDraw.Draw:
#     """Add the casualty's department to the post"""
#     if casualty.department:
#         return _add_text(casualty.department, 45, False, 70, draw, y_axis_offset)
#     else:
#         return draw, y_axis_offset
#
#
# def _add_details(
#         casualty: Casualty, draw: ImageDraw.Draw, y_axis_offset: int
# ) -> ImageDraw.Draw:
#     """Add additional text about the casualty to the post"""
#     text = [
#         f"נפל{'ה' if casualty.gender == Gender.FEMALE else ''} במלחמת חרבות ברזל",
#     ]
#
#     if casualty.date_of_death:
#         text.append(f"בתאריך {casualty.date_of_death_he} {casualty.date_of_death_en}")
#
#     if casualty.age:
#         text.append(
#             f"בת {casualty.age} במותה"
#             if casualty.gender == Gender.FEMALE
#             else f"בן {casualty.age} במותו",
#         )
#
#     if casualty.living_city:
#         text.append(
#             f"התגורר{'ה' if casualty.gender == Gender.FEMALE else ''} ב{casualty.living_city}"
#         )
#
#     # if casualty.grave_city:
#     #     text.append(
#     #         f"מקום מנוחת{'ה' if casualty.gender == Gender.FEMALE else 'ו'} {casualty.grave_city}"
#     #     )
#
#     for i, line in enumerate(text):
#         draw, y_axis_offset = _add_text(line, 32, False, 50, draw, y_axis_offset)
#
#     return draw, y_axis_offset
#
# # with names validation
# def _get_post_path(casualty: Casualty) -> str:
#     """Get the post target path"""
#     post_dir = os.path.join(os.getcwd(), GENERATED_POSTS_DIR)
#     post_dir = (
#         os.path.join(
#             post_dir,
#             str(casualty.date_of_death.year),
#             str(casualty.date_of_death.month),
#             str(casualty.date_of_death.day),
#         )
#         if casualty.date_of_death
#         else os.path.join(post_dir, "unknown")
#     )
#     Path(post_dir).mkdir(parents=True, exist_ok=True)
#     sanitized_name = sanitize_filename(casualty.full_name)
#     post_path = f"{post_dir}/{sanitized_name}.jpg"
#     return post_path
#
# # def _get_post_path(casualty: Casualty) -> str:
# #     """Get the post targer path"""
# #     post_dir = os.path.join(os.getcwd(), GENERATED_POSTS_DIR)
# #     post_dir = (
# #         os.path.join(
# #             post_dir,
# #             str(casualty.date_of_death.year),
# #             str(casualty.date_of_death.month),
# #             str(casualty.date_of_death.day),
# #         )
# #         if casualty.date_of_death
# #         else os.path.join(post_dir, "unknown")
# #     )
# #     Path(post_dir).mkdir(parents=True, exist_ok=True)
# #     post_path = f"{post_dir}/{casualty.full_name}.jpg"
# #     return post_path
#
#     # def _create_casualty_post(casualty_data: dict) -> None: MM i changed this func
# def create_casualty_post_worker(casualty_data: dict) -> dict:
#     """Create the casualty's post and save it"""
#     casualty: Casualty = Casualty.from_dict(casualty_data)
#     try:
#         if not casualty.post_published:
#             background = _get_background(casualty)
#             with Image.open(background) as post:
#                 image = _get_image(casualty)
#                 if image:
#                     post.paste(image, (670, 140))
#                 draw = ImageDraw.Draw(post)
#                 y_axis_offset = 135
#                 draw, y_axis_offset = _add_degree(casualty, draw, y_axis_offset)
#                 draw, y_axis_offset = _add_name(casualty, draw, y_axis_offset)
#                 draw, y_axis_offset = _add_department(casualty, draw, y_axis_offset)
#                 draw, y_axis_offset = _add_details(casualty, draw, y_axis_offset)
#                 casualty.post_path = _get_post_path(casualty)
#                 post.convert("RGB").save(casualty.post_path)
#     except Exception as e:
#         print(f"Failed to generate post for {casualty}: {e}")
#     finally:
#         return casualty.to_dict()
#
#
# def create_casualties_posts(given_casualties_data: List[dict]) -> List[dict]:
#     """Create post for all the casualties and save it"""
#     process_pool = multiprocessing.Pool()
#     # MM also here
#     # updated_casualties_data = process_pool.map(
#     #     _create_casualty_post, given_casualties_data
#     # )
#     updated_casualties_data = process_pool.map(create_casualty_post_worker, given_casualties_data)
#     process_pool.close()
#     return updated_casualties_data
#
#
# # i added
# def sanitize_filename(filename: str) -> str:
#     """Sanitize the filename to keep Hebrew and remove invalid characters"""
#     illegal_characters = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
#     for char in illegal_characters:
#         filename = filename.replace(char, '_')
#     filename = re.sub(r'_+', '_', filename)
#     filename = filename.strip('_')
#     filename = filename[:100] if filename else 'default_name'
#     return filename



import multiprocessing
import os
import re  # Added for sanitize_filename
from typing import List
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw

from utils.casualty import Casualty, Gender
from utils.paths import *

def get_font(size: int):
    print(f'in get_font function')
    """Generated a font object with the required size"""
    return ImageFont.truetype(
        "resources/Rubik-Regular.ttf", size, layout_engine=ImageFont.Layout.RAQM
    )

def _get_background(casualty: Casualty):
    print(f'in _get_background function')
    """Return a background image, matching the casualty's gender"""
    backgrounds = {
        Gender.FEMALE: "resources/female.png",
        Gender.MALE: "resources/male.png",
    }
    if casualty.gender not in backgrounds:
        raise Exception("Unknown gender")
    return backgrounds[casualty.gender]

# def _get_image(casualty: Casualty) -> Image:
#     print('in _get_image function')
#     """Return the casualty's image, opened and resized"""
#     # Sanitize the post_main_image file name
#     image_path = casualty.post_main_image if casualty.post_main_image else "resources/no_image_default.jpeg"
#     if image_path != "resources/no_image_default.jpeg":
#         image_filename = os.path.basename(image_path)
#         sanitized_filename = sanitize_filename(image_filename)
#         image_path = os.path.join(os.path.dirname(image_path), sanitized_filename)
#     casualty_img = Image.open(image_path)
#     width, height = casualty_img.size
#     ratio = height / width
#     wanted_width = 300
#     casualty_img = casualty_img.resize((wanted_width, int(wanted_width * ratio)))
#     return casualty_img
def _get_image(casualty: Casualty) -> Image:
    print('in _get_image function')
    """Return the casualty's image, opened and resized"""
    image_path = casualty.post_main_image if casualty.post_main_image else "resources/no_image_default.jpeg"
    if image_path != "resources/no_image_default.jpeg":
        image_filename = os.path.basename(image_path)
        sanitized_filename = sanitize_filename(image_filename)
        sanitized_path = os.path.join(os.path.dirname(image_path), sanitized_filename)
        # Try sanitized path first
        if os.path.exists(sanitized_path):
            image_path = sanitized_path
        # If sanitized path doesn't exist, try original path
        elif not os.path.exists(image_path):
            image_path = "resources/no_image_default.jpeg"
    try:
        casualty_img = Image.open(image_path)
    except FileNotFoundError:
        print(f"Image not found: {image_path}, using default")
        casualty_img = Image.open("resources/no_image_default.jpeg")
    width, height = casualty_img.size
    ratio = height / width
    wanted_width = 300
    casualty_img = casualty_img.resize((wanted_width, int(wanted_width * ratio)))
    return casualty_img

def _add_text(
        text: str,
        font_size: int,
        bold: bool,
        increase_offset: int,
        draw: ImageDraw.Draw,
        y_axis_offset: int,
):
    """Add text to the post according to the required parameters"""
    font = get_font(font_size)
    left, top, right, bottom = font.getbbox(text)
    width, height = right - left, top - bottom
    draw.text(
        (630 - width, y_axis_offset),
        text,
        (255, 255, 255),
        direction="rtl",
        align="right",
        features="rtla",
        font=font,
        stroke_width=1 if bold else 0,
        stroke_fill="white",
    )
    y_axis_offset += increase_offset
    return draw, y_axis_offset

def _add_degree(
        casualty: Casualty, draw: ImageDraw.Draw, y_axis_offset: int
) -> ImageDraw.Draw:
    """Add the casualty's degree to the post"""
    return _add_text(casualty.degree, 45, False, 50, draw, y_axis_offset)

def _add_name(
        casualty: Casualty, draw: ImageDraw.Draw, y_axis_offset: int
) -> ImageDraw.Draw:
    """Add the casualty's name to the post"""
    return _add_text(f'{casualty.full_name} ז"ל', 54, True, 65, draw, y_axis_offset)

def _add_department(
        casualty: Casualty, draw: ImageDraw.Draw, y_axis_offset: int
) -> ImageDraw.Draw:
    """Add the casualty's department to the post"""
    if casualty.department:
        return _add_text(casualty.department, 45, False, 70, draw, y_axis_offset)
    else:
        return draw, y_axis_offset

def _add_details(
        casualty: Casualty, draw: ImageDraw.Draw, y_axis_offset: int
) -> ImageDraw.Draw:
    """Add additional text about the casualty to the post"""
    text = [
        f"נפל{'ה' if casualty.gender == Gender.FEMALE else ''} במלחמת חרבות ברזל",
    ]

    if casualty.date_of_death:
        text.append(f"בתאריך {casualty.date_of_death_he} {casualty.date_of_death_en}")

    if casualty.age:
        text.append(
            f"בת {casualty.age} במותה"
            if casualty.gender == Gender.FEMALE
            else f"בן {casualty.age} במותו",
        )

    if casualty.living_city:
        text.append(
            f"התגורר{'ה' if casualty.gender == Gender.FEMALE else ''} ב{casualty.living_city}"
        )

    for i, line in enumerate(text):
        draw, y_axis_offset = _add_text(line, 32, False, 50, draw, y_axis_offset)

    return draw, y_axis_offset

def _get_post_path(casualty: Casualty) -> str:
    """Get the post target path"""
    post_dir = os.path.join(os.getcwd(), GENERATED_POSTS_DIR)
    post_dir = (
        os.path.join(
            post_dir,
            str(casualty.date_of_death.year),
            str(casualty.date_of_death.month),
            str(casualty.date_of_death.day),
        )
        if casualty.date_of_death
        else os.path.join(post_dir, "unknown")
    )
    Path(post_dir).mkdir(parents=True, exist_ok=True)
    sanitized_name = sanitize_filename(casualty.full_name)
    post_path = f"{post_dir}/{sanitized_name}.jpg"
    return post_path

def create_casualty_post_worker(casualty_data: dict) -> dict:
    """Create the casualty's post and save it"""
    casualty: Casualty = Casualty.from_dict(casualty_data)
    try:
        if not casualty.post_published:
            background = _get_background(casualty)
            with Image.open(background) as post:
                image = _get_image(casualty)
                if image:
                    post.paste(image, (670, 140))
                draw = ImageDraw.Draw(post)
                y_axis_offset = 135
                draw, y_axis_offset = _add_degree(casualty, draw, y_axis_offset)
                draw, y_axis_offset = _add_name(casualty, draw, y_axis_offset)
                draw, y_axis_offset = _add_department(casualty, draw, y_axis_offset)
                draw, y_axis_offset = _add_details(casualty, draw, y_axis_offset)
                casualty.post_path = _get_post_path(casualty)
                post.convert("RGB").save(casualty.post_path)
    except Exception as e:
        print(f"Failed to generate post for {casualty}: {e}")
    finally:
        return casualty.to_dict()

def create_casualties_posts(given_casualties_data: List[dict]) -> List[dict]:
    """Create post for all the casualties and save it"""
    process_pool = multiprocessing.Pool()
    updated_casualties_data = process_pool.map(create_casualty_post_worker, given_casualties_data)
    process_pool.close()
    return updated_casualties_data

def sanitize_filename(filename: str) -> str:
    """Sanitize the filename to keep Hebrew and remove invalid characters"""
    illegal_characters = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in illegal_characters:
        filename = filename.replace(char, '_')
    filename = re.sub(r'_+', '_', filename)
    filename = filename.strip('_')
    filename = filename[:100] if filename else 'default_name'
    return filename