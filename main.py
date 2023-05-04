from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InputFile, InputMedia
from time import time
from datetime import datetime
from random import randint
import os
from math import sqrt
import asyncio

import graphics
#import database
#from database import *
import pygame
from config import *

queries = dict()
'''
{
    query_time,
    border_type,
    border_flag,
    border_width,
    border_padding_width,
    border_padding_color,
    step,
    image
}
'''

# ! CONSTANTS
LOG_SIZE = 3000
LOG_DELAY = 5 * 60
DEV_ID = 983670270
MAX_PHOTO_SIZE = 1024
MIN_PHOTO_SIDE = 64
MAX_PHOTO_SIDE = 2048
QUERY_DELAY = 1 * 60
CLEANER_DELAY = QUERY_DELAY
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)



# ! BUTTONS
BUTTON_ROUND = InlineKeyboardButton('Round ⚪️', callback_data="BUTTON_ROUND")
BUTTON_RECTANGULAR = InlineKeyboardButton('Rectangular ⬜️', callback_data="BUTTON_RECTANGULAR")
KEYBOARD_TYPE = InlineKeyboardMarkup(row_width=2) \
    .row(BUTTON_ROUND, BUTTON_RECTANGULAR)

BUTTON_UKRAINIAN = InlineKeyboardButton('Ukrainian 🟦🟨', callback_data="BUTTON_UKRAINIAN")
BUTTON_BANDERA = InlineKeyboardButton('Ukrainian Insurgent Army 🟥⬛', callback_data="BUTTON_BANDERA")
KEYBOARD_FLAG = InlineKeyboardMarkup(row_width=2) \
    .add(BUTTON_UKRAINIAN).add(BUTTON_BANDERA)

KEYBOARD_WIDTH = InlineKeyboardMarkup(row_width=8)
for p in range(3):
    list = []
    for i in range(8):
        k = p * 8 + i + 5
        list.append(InlineKeyboardButton(f'{k}%', callback_data="BUTTON_WIDTH%s" % k))
    KEYBOARD_WIDTH.row(*list)

KEYBOARD_PADDING_WIDTH = InlineKeyboardMarkup(row_width=8)
for p in range(3):
    list = []
    for i in range(8):
        k = p * 16 + i + i
        list.append(InlineKeyboardButton(f'{k}%', callback_data="BUTTON_PADDING_WIDTH%s" % k))
    KEYBOARD_PADDING_WIDTH.row(*list)

BUTTON_WHITE = InlineKeyboardButton("White 🤍", callback_data="BUTTON_WHITE")
BUTTON_BLACK = InlineKeyboardButton("Black 🖤", callback_data="BUTTON_BLACK")
KEYBOARD_PADDING_COLOR = InlineKeyboardMarkup(row_width=2) \
    .row(BUTTON_WHITE, BUTTON_BLACK)

# ! LOGGING
log_text = ""
log_time = time()


def get_log_start() -> str:
    return "LOG: %s\n" % datetime.utcnow()


async def log(message: str):
    global log_text, log_time
    log_text += get_log_start() + message + "\n"
    print(message)
    if len(log_text) > LOG_SIZE and len(log_text) > 0:
        await bot.send_message(DEV_ID, log_text, parse_mode="Markdown")
        log_text = ""
    elif len(log_text) > 0 and time() - log_time > LOG_DELAY:
        await bot.send_message(DEV_ID, log_text, parse_mode="Markdown")
        log_text = ""
        log_time = time()


def get_mention(user: types.User):
    if user.username is not None:
        return "[@%s](tg://user?id=%s)" % (user.username, user.id)
    else:
        return "[%s](tg://user?id=%s)" % (user.first_name, user.id)


# ! CALLBACKS
@dp.callback_query_handler(lambda c: c.data == 'BUTTON_ROUND')
async def callback_BUTTON_ROUND(cq: types.CallbackQuery):
    if cq.from_user.id not in queries.keys():
        await cq.message.answer("Outdated request, send new photo.")
        return
    data = queries[cq.from_user.id]
    if data["border_type"] is not None or data["step"] != 0:
        return
    data["border_type"] = "round"
    data["step"] += 1
    await cq.message.edit_media(InputMedia(type="photo", media=open("step2.png", "rb")))
    await cq.message.edit_caption("▫️ Border type: round\n\nSelect border flag:")
    await cq.message.edit_reply_markup(KEYBOARD_FLAG)


@dp.callback_query_handler(lambda c: c.data == 'BUTTON_RECTANGULAR')
async def callback_BUTTON_RECTANGULAR(cq: types.CallbackQuery):
    if cq.from_user.id not in queries.keys():
        await cq.message.answer("Outdated request, send new photo.")
        return
    data = queries[cq.from_user.id]
    if data["border_type"] is not None or data["step"] != 0:
        return
    data["border_type"] = "rectangular"
    data["step"] += 1
    await cq.message.edit_media(InputMedia(type="photo", media=open("step2.png", "rb")))
    await cq.message.edit_caption("▫️ Border type: rectangular\n\nSelect border flag:")
    await cq.message.edit_reply_markup(KEYBOARD_FLAG)


@dp.callback_query_handler(lambda c: c.data == 'BUTTON_UKRAINIAN')
async def callback_BUTTON_UKRAINIAN(cq: types.CallbackQuery):
    if cq.from_user.id not in queries.keys():
        await cq.message.answer("Outdated request, send new photo.")
        return
    data = queries[cq.from_user.id]
    if data["border_flag"] is not None or data["step"] != 1:
        return
    data["border_flag"] = "ukrainian"
    data["step"] += 1
    await cq.message.edit_media(InputMedia(type="photo", media=open("step3.png", "rb")))
    await cq.message.edit_caption("▫️ Border type: %s\n▫️ Border flag: ukrainian\n\nSelect border width:" % \
                                  data["border_type"])
    await cq.message.edit_reply_markup(KEYBOARD_WIDTH)


@dp.callback_query_handler(lambda c: c.data == 'BUTTON_BANDERA')
async def callback_BUTTON_BANDERA(cq: types.CallbackQuery):
    if cq.from_user.id not in queries.keys():
        await cq.message.answer("Outdated request, send new photo.")
        return
    data = queries[cq.from_user.id]
    if data["border_flag"] is not None or data["step"] != 1:
        return
    data["border_flag"] = "UIA"
    data["step"] += 1
    await cq.message.edit_media(InputMedia(type="photo", media=open("step3.png", "rb")))
    await cq.message.edit_caption("▫️ Border type: %s\n▫️ Border flag: UIA\n\nSelect border width:" % \
                                  data["border_type"])
    await cq.message.edit_reply_markup(KEYBOARD_WIDTH)


@dp.callback_query_handler(lambda c: ('BUTTON_WIDTH' in c.data))
async def callback(cq: types.CallbackQuery):
    k = int(cq.data.replace("%", '').replace("BUTTON_WIDTH", ""))
    if cq.from_user.id not in queries.keys():
        await cq.message.answer("Outdated request, send new photo.")
        return
    data = queries[cq.from_user.id]
    if data["border_width"] is not None or data["step"] != 2:
        return
    data["border_width"] = k
    data["step"] += 1
    await cq.message.edit_media(InputMedia(type="photo", media=open("step4.png", "rb")))
    await cq.message.edit_caption(("▫️ Border type: %s\n▫️ Border flag: %s\n" \
                                   "▫️ Border width: %s\n\nSelect border padding width:") % \
                                  (data["border_type"], data["border_flag"], f"{k}%"))
    await cq.message.edit_reply_markup(KEYBOARD_PADDING_WIDTH)


@dp.callback_query_handler(lambda c: ('BUTTON_PADDING_WIDTH' in c.data))
async def callback(cq: types.CallbackQuery):
    k = int(cq.data.replace("%", '').replace("BUTTON_PADDING_WIDTH", ""))
    if cq.from_user.id not in queries.keys():
        await cq.message.answer("Outdated request, send new photo.")
        return
    data = queries[cq.from_user.id]
    if data["border_padding_width"] is not None or data["step"] != 3:
        return
    data["border_padding_width"] = k
    data["step"] += 1
    await cq.message.edit_media(InputMedia(type="photo", media=open("step5.png", "rb")))
    await cq.message.edit_caption(("▫️ Border type: %s\n▫️ Border flag: %s\n" \
                                   "▫️ Border width: %s\n▫️ Border padding width: %s\n\nSelect border padding color:") % \
                                  (data["border_type"], data["border_flag"], f"{data['border_width']}%", f"{k}%"))
    await cq.message.edit_reply_markup(KEYBOARD_PADDING_COLOR)


@dp.callback_query_handler(lambda c: c.data == "BUTTON_WHITE")
async def callback(cq: types.CallbackQuery):
    if cq.from_user.id not in queries.keys():
        await cq.message.answer("Outdated request, send new photo.")
        return
    data = queries[cq.from_user.id]
    if data["border_padding_color"] is not None or data["step"] != 4:
        return
    data["border_padding_color"] = "white"
    await cq.message.edit_caption(("▫️ Border type: %s\n▫️ Border flag: %s\n" \
                                   "▫️ Border width: %s\n▫️ Border padding width: %s\n▫️ Border padding color: white\n\nProcessing...") % \
                                  (data["border_type"], data["border_flag"], f"{data['border_width']}%",
                                   f"{data['border_padding_width']}%"))
    file = await process_image(cq.from_user.id)
    await bot.send_photo(cq.from_user.id, InputFile(file), "Made by @UkraineImageBot to support Ukraine")
    await log("processed photo from %s" % get_mention(cq.from_user))

    os.system("rm %s %s" % (data["image"], file))


@dp.callback_query_handler(lambda c: c.data == "BUTTON_BLACK")
async def callback(cq: types.CallbackQuery):
    if cq.from_user.id not in queries.keys():
        await cq.message.answer("Outdated request, send new photo.")
        return
    data = queries[cq.from_user.id]
    if data["border_padding_color"] is not None or data["step"] != 4:
        return
    data["border_padding_color"] = "black"
    await cq.message.edit_caption(("▫️ Border type: %s\n▫️ Border flag: %s\n" \
                                   "▫️ Border width: %s\n▫️ Border padding width: %s\n▫️ Border padding color: black\n\nProcessing...") % \
                                  (data["border_type"], data["border_flag"], f"{data['border_width']}%",
                                   f"{data['border_padding_width']}%"))
    file = await process_image(cq.from_user.id)
    await bot.send_photo(cq.from_user.id, InputFile(file), "Made by @UkraineImageBot to support Ukraine")
    await log("processed photo from %s" % get_mention(cq.from_user))

    os.system("rm %s %s" % (data["image"], file))


# ! MESSAGES
def mread(file: str) -> str:
    with open(file, 'r') as f:
        data = f.read()
    return data


START_MESSAGE = mread("start_message.txt")
HELP_MESSAGE = mread("help_message.txt")
DEV_MESSAGE = mread("dev_message.txt")
DONATE_MESSAGE = mread("donate_message.txt")
DONATORS_MESSAGE = mread("donators_message.txt")
DONATORS = mread("donators.txt")
DONATORS = DONATORS.split("\n")
DONATORS = sorted(DONATORS, key=lambda b: float(b.split()[-1]), reverse=True)
DONATORS5 = "".join(
    ["%s" % ("".join([e + " " for e in line.split()[:-1]]))[:-1] + '\n' for line in DONATORS[:min(len(DONATORS), 5)]])[
            :-1]
DONATORS = "".join(["%s" % ("".join([e + " " for e in line.split()[:-1]]))[:-1] + '\n' for line in DONATORS])[:-1]


# ! COMMANDS
@dp.message_handler(commands=["start", "info", "about"])
async def start_command(message: types.Message):
    #await add_id_to_database(message.from_user.id)
    await log("%s from %s" % (message.text, get_mention(message.from_user)))
    await message.answer(START_MESSAGE)


@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    #await add_id_to_database(message.from_user.id)
    await log("%s from %s" % (message.text, get_mention(message.from_user)))
    await message.answer(HELP_MESSAGE)


@dp.message_handler(commands=["dev"])
async def dev_command(message: types.Message):
    #await add_id_to_database(message.from_user.id)
    await log("%s from %s" % (message.text, get_mention(message.from_user)))
    await message.answer(DEV_MESSAGE)


@dp.message_handler(commands=["donate"])
async def donate_command(message: types.Message):
    #await add_id_to_database(message.from_user.id)
    await log("%s from %s" % (message.text, get_mention(message.from_user)))
    await message.answer(DONATE_MESSAGE.replace("#DONATORS", DONATORS5), parse_mode="Markdown")


@dp.message_handler(commands=["donators"])
async def donators_command(message: types.Message):
    #await add_id_to_database(message.from_user.id)
    await log("%s from %s" % (message.text, get_mention(message.from_user)))
    await message.answer(DONATORS_MESSAGE.replace("#DONATORS", DONATORS), parse_mode="Markdown")


@dp.message_handler(commands=["logs"])
async def logs_command(message: types.Message):
    if message.from_user.id != DEV_ID:
        return
    global log_text, log_time
    if (not log_text): return
    await bot.send_message(DEV_ID, log_text, parse_mode="Markdown")
    log_text = ""
    log_time = time()


@dp.message_handler(commands=["users"])
async def logs_command(message: types.Message):
    if message.from_user.id != DEV_ID:
        return
    users = get_users()
    await message.answer(str(users))


@dp.message_handler(commands=["connections"])
async def logs_command(message: types.Message):
    if message.from_user.id != DEV_ID:
        return
    #await message.answer(str(database.CONNECTIONS))


'''@dp.message_handler()
async def global_handler(message: types.Message):
    await add_id_to_database(message.from_user.id)

    if "/broadcast" in message.text:
        if message.from_user.id != DEV_ID:
            return
        text = message.text.replace("/broadcast", "").strip()
        users = get_users()
        ok, error = 0, 0
        for user in users:
            try:
                res = await bot.send_message(user, text)
            except:
                res = None
            if isinstance(res,types.Message):
                ok+=1
            else:
                error+=1
        await log("sent broadcast message. %s ok, %s errors"%(ok,error))
        return

    if "Слава" in message.text and "Україні" in message.text:
        await message.answer("Героям Слава!")
        return

'''


# ! PATH GENERATOR
def randpath(e: str) -> str:
    tm = time()
    rand1 = randint(1, 1e18)
    rand2 = randint(1, 1e18)
    return "%s_%s_%s.%s" % (tm, rand1, rand2, e)


# ! PHOTO HANDLER
@dp.message_handler(content_types=["photo"])
async def photo_message(message: types.Message):
    photo = message.photo[-1]
    photo_size = photo.file_size // (1024)
    photo_width = photo.width
    photo_height = photo.height

    await log("photo %sx%s %skb from %s" % (photo_width, photo_height, photo_size, get_mention(message.from_user)))
    if photo_size > MAX_PHOTO_SIZE:
        await message.answer("Rejected: photo's size is too big: %skb. max %skb." % (photo_size, MAX_PHOTO_SIZE))
        return
    if photo_width < MIN_PHOTO_SIDE or photo_height < MIN_PHOTO_SIDE:
        await message.answer("Rejected: photo's size is too small")
        return
    if photo_width > MAX_PHOTO_SIDE or photo_height > MAX_PHOTO_SIDE:
        await message.answer("Rejected: photo's size is too big")
        return

    user_id = message.from_user.id
    if user_id in queries.keys():
        if time() - queries[user_id]["query_time"] < QUERY_DELAY:
            await message.answer("Please wait %ssec." %
                                 int(QUERY_DELAY - (time() - queries[user_id]["query_time"])))
            return
    photo_path = randpath("png")
    await photo.download(destination_file=photo_path)

    queries[user_id] = {
        "query_time": time(),
        "border_type": None,
        "border_flag": None,
        "border_width": None,
        "border_padding_width": None,
        "border_padding_color": None,
        "step": 0,
        "image": photo_path
    }
    #await add_id_to_database(message.from_user.id)
    await message.answer_photo(photo=InputFile("step1.png"), caption="Select border type:", reply_markup=KEYBOARD_TYPE)


# ! IMAGE PROCESSING
async def process_image(id):
    file = randpath("png")
    data = queries[id]
    if data["border_type"] == "round":
        img = pygame.image.load(data["image"])
        round_image = graphics.circle_from_image(img, img.get_width() // 2, img.get_height() // 2,
                                                 min(img.get_width(), img.get_height()) / 2)
        imgW = round_image.get_width()
        k = data["border_width"]
        borderW = int(imgW / (1 - k / 100))
        k = data["border_padding_width"]
        paddingW = int(imgW + (k / 100) * (borderW - imgW))
        clr = (0, 0, 0) if data["border_padding_color"] == "black" else (255, 255, 255)
        padding_image = graphics.circle_from_color(clr, paddingW / 2)
        border_image = pygame.Surface((borderW, borderW), pygame.SRCALPHA)

        if data["border_flag"] == "ukrainian":
            surf = pygame.Surface((borderW, borderW // 2))
            surf.fill((0, 91, 187))
            border_image.blit(surf, (0, 0))
            surf = pygame.Surface((borderW, borderW - borderW // 2))
            surf.fill((255, 213, 0))
            border_image.blit(surf, (0, borderW // 2))
        elif data["border_flag"] == "UIA":
            surf = pygame.Surface((borderW, borderW // 2))
            surf.fill((190, 0, 0))
            border_image.blit(surf, (0, 0))
            surf = pygame.Surface((borderW, borderW - borderW // 2))
            surf.fill((0, 0, 0))
            border_image.blit(surf, (0, borderW // 2))
        if k > 0: border_image.blit(padding_image, ((borderW - paddingW) // 2, (borderW - paddingW) // 2))
        border_image.blit(round_image, ((borderW - imgW) // 2, (borderW - imgW) // 2))
        pygame.image.save(border_image, file)
    elif data["border_type"] == "rectangular":
        img = pygame.image.load(data["image"])
        imgW = img.get_width()
        imgH = img.get_height()
        k = data["border_width"]
        border_px = max(imgW / (1 - k / 100) - imgW, imgH / (1 - k / 100) - imgH)
        border_px = int(border_px)
        borderW = imgW + border_px
        borderH = imgH + border_px
        k = data["border_padding_width"]
        padding_px = int(border_px * (k / 100))
        paddingW = imgW + padding_px
        paddingH = imgH + padding_px
        border_image = pygame.Surface((borderW, borderH), pygame.SRCALPHA)
        if data["border_flag"] == "ukrainian":
            surf = pygame.Surface((borderW, borderH // 2))
            surf.fill((0, 91, 187))
            border_image.blit(surf, (0, 0))
            surf = pygame.Surface((borderW, borderH - borderH // 2))
            surf.fill((255, 213, 0))
            border_image.blit(surf, (0, borderH // 2))
        elif data["border_flag"] == "UIA":
            surf = pygame.Surface((borderW, borderH // 2))
            surf.fill((190, 0, 0))
            border_image.blit(surf, (0, 0))
            surf = pygame.Surface((borderW, borderH - borderH // 2))
            surf.fill((0, 0, 0))
            border_image.blit(surf, (0, borderH // 2))
        padding_image = pygame.Surface((paddingW, paddingH))
        clr = (0, 0, 0) if data["border_padding_color"] == "black" else (255, 255, 255)
        padding_image.fill(clr)
        border_image.blit(padding_image, ((borderW - paddingW) // 2, (borderH - paddingH) // 2))
        border_image.blit(img, ((borderW - imgW) // 2, (borderH - imgH) // 2))
        pygame.image.save(border_image, file)
    return file


# ! CLEANER
async def cleaner():
    global queries
    while True:
        await asyncio.sleep(CLEANER_DELAY)
        new_dict = queries.copy()
        for id in queries.keys():
            if time() - queries[id]["query_time"] > CLEANER_DELAY:
                if os.path.isfile(queries[id]["image"]):
                    os.system("rm %s" % queries[id]["image"])
                new_dict.pop(id, {})
        queries = dict(new_dict)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(cleaner())
    executor.start_polling(dp, skip_updates=True)
