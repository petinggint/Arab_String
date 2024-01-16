from asyncio.exceptions import TimeoutError
from Data import Data
from pyrogram import Client, filters
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

ERROR_MESSAGE = "ᴜᴘꜱ!  ᴛᴇʀᴊᴀᴅɪ ᴘᴇɴɢᴇᴄᴜᴀʟɪᴀɴ! \n\n**ᴋᴇꜱᴀʟᴀʜᴀɴ** : {} " \
            "\n\nʜᴀʀᴀᴘ ᴛᴇʀᴜꜱᴋᴀɴ ɪɴɪ ᴋᴇ @Foundermidnight ᴊɪᴋᴀ ᴘᴇꜱᴀɴ ɪɴɪ ᴛɪᴅᴀᴋ ʙᴇʀɪꜱɪ ᴀᴘᴀ ᴘᴜɴ " \
            "ɪɴꜰᴏʀᴍᴀꜱɪ ꜱᴇɴꜱɪᴛɪꜰ ᴅᴀɴ ᴜɴᴛᴜᴋ ɪɴꜰᴏʀᴍᴀꜱɪ ᴀɴᴅᴀ : **ʟᴏɢ ᴋᴇꜱᴀʟᴀʜᴀɴ ꜱᴇᴍᴀᴄᴀᴍ ɪɴɪ ᴛɪᴅᴀᴋ ᴅɪꜱɪᴍᴘᴀɴ ᴅᴀʟᴀᴍ ᴅᴀᴛᴀʙᴀꜱᴇ ᴋᴀᴍɪ!**"


@Client.on_message(filters.private & ~filters.forwarded & filters.command('generate'))
async def main(_, msg):
    await msg.reply(
        "Please choose the python library you want to generate string session for",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("ᴘʏʀᴏɢʀᴀᴍ", callback_data="pyrogram"),
            InlineKeyboardButton("ᴛᴇʟᴇᴛʜᴏɴ", callback_data="telethon")
        ]])
    )


async def generate_session(bot, msg, telethon=False):
    await msg.reply("ᴍᴇᴍᴜʟᴀɪ {} ᴍᴇɴɢᴀᴍʙɪʟ ꜱᴛʀɪɴɢ...".format("ᴛᴇʟᴇᴛʜᴏɴ" if telethon else "ᴘʏʀᴏɢʀᴀᴍ"))
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, 'ᴋɪʀɪᴍ ᴀᴘɪ_ɪᴅ ʟᴜ ʙᴜʀᴜᴀɴ`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply('ʙᴜᴋᴀɴ ᴀᴘɪ_ɪᴅ ʏᴀɴɢ ᴠᴀʟɪᴅ (ʜᴀʀᴜꜱ ʙɪʟᴀɴɢᴀɴ ʙᴜʟᴀᴛ). ꜱɪʟᴀᴋᴀɴ ᴍᴜʟᴀɪ ᴍᴇᴍʙᴜᴀᴛ ꜱᴇꜱɪ ʟᴀɢɪ.', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    api_hash_msg = await bot.ask(user_id, 'ꜱɪʟᴀʜᴋᴀɴ ᴋɪʀɪᴍᴋᴀɴ `ᴀᴘɪ_ʜᴀꜱʜ`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await bot.ask(user_id, 'ꜱᴇᴋᴀʀᴀɴɢ ᴋɪʀɪᴍᴋᴀɴ ᴘʜᴏɴᴇ_ɴᴜᴍʙᴇʀ ᴀɴᴅᴀ ʙᴇꜱᴇʀᴛᴀ ᴋᴏᴅᴇ ɴᴇɢᴀʀᴀ. \nᴄᴏɴᴛᴏʜ : `+620865739234`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    phone_number = phone_number_msg.text
    await msg.reply("ꜱᴇᴅᴀɴɢ ᴍᴇɴɢɪʀɪᴍ ᴏᴛᴘ...")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    else:
        client = Client(":memory:", api_id, api_hash)
    await client.connect()
    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply('`ᴀᴘɪ_ɪᴅ ᴀɴᴅ ᴀᴘɪ_ʜᴀꜱʜ` ᴋᴏᴍʙɪɴᴀꜱɪ ᴛɪᴅᴀᴋ ᴠᴀʟɪᴅ. ꜱɪʟᴀᴋᴀɴ ᴍᴜʟᴀɪ ᴍᴇᴍʙᴜᴀᴛ ꜱᴇꜱɪ ʟᴀɢɪ.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply('`ᴘʜᴏɴᴇ_ɴᴜᴍʙᴇʀ` ᴛɪᴅᴀᴋ ᴠᴀʟɪᴅ. ꜱɪʟᴀᴋᴀɴ ᴍᴜʟᴀɪ ᴍᴇᴍʙᴜᴀᴛ ꜱᴇꜱɪ ʟᴀɢɪ.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    try:
        phone_code_msg = await bot.ask(user_id, "ꜱɪʟᴀᴋᴀɴ ᴘᴇʀɪᴋꜱᴀ ᴏᴛᴘ ᴅɪ ᴀᴋᴜɴ ᴛᴇʟᴇɢʀᴀᴍ ʀᴇꜱᴍɪ. ᴊɪᴋᴀ ᴀɴᴅᴀ ᴍᴇɴᴅᴀᴘᴀᴛᴋᴀɴɴʏᴀ, ᴋɪʀɪᴍ ᴏᴛᴘ ᴋᴇ ꜱɪɴɪ ꜱᴇᴛᴇʟᴀʜ ᴍᴇᴍʙᴀᴄᴀ ꜰᴏʀᴍᴀᴛ ᴅɪ ʙᴀᴡᴀʜ ɪɴɪ. \nᴊɪᴋᴀ ᴏᴛᴘ ᴅᴀʟᴀᴍ ʙᴇɴᴛᴜᴋ ~ `12345`, **ᴛᴏʟᴏɴɢ ᴋɪʀɪᴍᴋᴀɴ ꜱᴇʙᴀɢᴀɪ** `1 2 3 4 5`.", filters=filters.text, timeout=600)
        if await cancelled(api_id_msg):
            return
    except TimeoutError:
        await msg.reply('ʙᴀᴛᴀꜱ ᴡᴀᴋᴛᴜ ᴍᴇɴᴄᴀᴘᴀɪ 10 ᴍᴇɴɪᴛ. ꜱɪʟᴀᴋᴀɴ ᴍᴜʟᴀɪ ᴍᴇᴍʙᴜᴀᴛ ꜱᴇꜱɪ ʟᴀɢɪ.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, phone_code, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await msg.reply('ᴏᴛᴘ ᴛɪᴅᴀᴋ ᴠᴀʟɪᴅ. ꜱɪʟᴀᴋᴀɴ ᴍᴜʟᴀɪ ᴍᴇᴍʙᴜᴀᴛ ꜱᴇꜱɪ ʟᴀɢɪ.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await msg.reply('ᴏᴛᴘ ᴛᴇʟᴀʜ ᴋᴇᴅᴀʟᴜᴡᴀʀꜱᴀ. ꜱɪʟᴀᴋᴀɴ ᴍᴜʟᴀɪ ᴍᴇᴍʙᴜᴀᴛ ꜱᴇꜱɪ ʟᴀɢɪ.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            two_step_msg = await bot.ask(user_id, 'ᴀᴋᴜɴ ᴀɴᴅᴀ ᴛᴇʟᴀʜ ᴍᴇɴɢᴀᴋᴛɪꜰᴋᴀɴ ᴠᴇʀɪꜰɪᴋᴀꜱɪ ᴅᴜᴀ ʟᴀɴɢᴋᴀʜ. ʙᴇʀɪᴋᴀɴ ᴋᴀᴛᴀ ꜱᴀɴᴅɪ.', filters=filters.text, timeout=300)
        except TimeoutError:
            await msg.reply('ʙᴀᴛᴀꜱ ᴡᴀᴋᴛᴜ ᴍᴇɴᴄᴀᴘᴀɪ 5 ᴍᴇɴɪᴛ. ꜱɪʟᴀᴋᴀɴ ᴍᴜʟᴀɪ ᴍᴇᴍʙᴜᴀᴛ ꜱᴇꜱɪ ʟᴀɢɪ.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
        try:
            password = two_step_msg.text
            if telethon:
                await client.sign_in(password=password)
            else:
                await client.check_password(password=password)
            if await cancelled(api_id_msg):
                return
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await two_step_msg.reply('ᴘᴀꜱꜱᴡᴏʀᴅ ᴠ2ʟ ʟᴜ ꜱᴀʟᴀʜ. ꜱɪʟᴀᴋᴀɴ ᴍᴜʟᴀɪ ᴍᴇᴍʙᴜᴀᴛ ꜱᴇꜱɪ ʟᴀɢɪ.', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = "**{} ~ ꜱᴛʀɪɴɢ ꜱᴇꜱꜱɪᴏɴ** \n\n`{}` \n\n• __ᴊᴀɴɢᴀɴ ᴅɪ ꜱʜᴀʀᴇ ᴀᴛᴀᴜ ʟᴜ ʙᴀɢɪᴋᴀɴ ᴋᴇ ᴏʀᴀɴɢ-ᴏʀᴀɴɢ__\n• __ꜱᴛʀɪɴɢ ꜱᴇꜱꜱɪᴏɴ ʙʏ @Foundermidnight | @Berlinmusic_suport__".format("TELETHON" if telethon else "PYROGRAM", string_session)
    L_PIC = "https://graph.org/file/a0b83a9660f4479d8079a.jpg"
    #await msg.reply({text})
    if telethon:
        await client.send_file("me", L_PIC, caption="**{} - STRING SESSION** \n\n`{}`\n\n• __ᴊᴀɴɢᴀɴ ᴅɪ ꜱʜᴀʀᴇ ᴀᴛᴀᴜ ʟᴜ ʙᴀɢɪᴋᴀɴ ᴋᴇ ᴏʀᴀɴɢ-ᴏʀᴀɴɢ__\n• __Dont Invite Anyone To Heroku__".format("TELETHON" if telethon else "PYROGRAM", string_session))
        try:
            await client(JoinChannelRequest("@Ortresxz"))
            await client(JoinChannelRequest("@Berlinmusic_support"))
            await client(LeaveChannelRequest("@Areamidnight"))
        except BaseException:
            pass
    else:
        await client.send_message("me", text)
        #await client.join_chat("@Berlinmusic_support")
    await client.disconnect()
    await phone_code_msg.reply("ꜱᴇꜱɪ ꜱᴛʀɪɴɢ ʙᴇʀʜᴀꜱɪʟ ᴛᴇʟᴀʜ ᴅɪᴀᴋᴛɪᴘᴋᴀɴ {} \n\nʟᴜ ᴄᴇᴋ ᴀᴊᴀ ᴘᴇꜱᴀɴ ᴛᴇʀꜱɪᴍᴘᴀɴ ʟᴜ ʏᴀ ᴛᴏᴅ!".format("telethon" if telethon else "pyrogram"), reply_markup=InlineKeyboardMarkup(Data.support_button))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("ᴘʀᴏᴄᴄᴇꜱ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("ʀᴇꜱᴛᴀʀᴛɪɴɢ ʙᴏᴛ!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("ᴘʀᴏᴄᴄᴇꜱ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ᴘᴇɴɢᴀᴍʙɪʟᴀɴ ꜱᴛʀɪɴɢ!", quote=True)
        return True
    else:
        return False
