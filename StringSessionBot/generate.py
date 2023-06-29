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

ERROR_MESSAGE = "Oops! An exception occurred! \n\n**Error** : {} " \
            "\n\nPlease forward this to @Arabnihnge if this message doesn't contain any " \
            "sensitive information and for your information : **These kinda error logs are not stored in our database!**"


@Client.on_message(filters.private & ~filters.forwarded & filters.command('generate'))
async def main(_, msg):
    await msg.reply(
        "Please choose the python library you want to generate string session for",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Pyrogram", callback_data="pyrogram"),
            InlineKeyboardButton("Telethon", callback_data="telethon")
        ]])
    )


async def generate_session(bot, msg, telethon=False):
    await msg.reply("Starting {} Session Generation...".format("Telethon" if telethon else "Pyrogram"))
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, 'Tolong Kirimkan `API_ID`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply('Bukan API_ID yang valid (harus bilangan bulat). Silakan mulai membuat sesi lagi.', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    api_hash_msg = await bot.ask(user_id, 'Silahkan Kirimkan `API_HASH`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await bot.ask(user_id, 'Sekarang kirimkan `PHONE_NUMBER` Anda beserta kode negara. \nContoh : `+620865739234`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    phone_number = phone_number_msg.text
    await msg.reply("Sedang Mengirim OTP...")
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
        await msg.reply('`API_ID` and `API_HASH` kombinasi tidak valid. Silakan mulai membuat sesi lagi.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply('`PHONE_NUMBER` Tidak valid. Silakan mulai membuat sesi lagi.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    try:
        phone_code_msg = await bot.ask(user_id, "Silakan periksa OTP di akun telegram resmi. Jika Anda mendapatkannya, kirim OTP ke sini setelah membaca format di bawah ini. \nJika OTP dalam bentuk ~ `12345`, **Tolong kirimkan sebagai** `1 2 3 4 5`.", filters=filters.text, timeout=600)
        if await cancelled(api_id_msg):
            return
    except TimeoutError:
        await msg.reply('Batas waktu mencapai 10 menit. Silakan mulai membuat sesi lagi.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, phone_code, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await msg.reply('OTP tidak valid. Silakan mulai membuat sesi lagi.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await msg.reply('OTP telah kedaluwarsa. Silakan mulai membuat sesi lagi.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            two_step_msg = await bot.ask(user_id, 'Akun Anda telah mengaktifkan verifikasi dua langkah. Berikan kata sandi.', filters=filters.text, timeout=300)
        except TimeoutError:
            await msg.reply('Batas waktu mencapai 5 menit. Silakan mulai membuat sesi lagi.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
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
            await two_step_msg.reply('Invalid Password Provided. Please start generating session again.', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = "**{} ~ STRING SESSION** \n\n`{}` \n\n• __Jangan Di Share Atau Lu Bagikan Ke Orang-Orang__\n• __String Session by @Arabnihnge | @SiArabSupport__".format("TELETHON" if telethon else "PYROGRAM", string_session)
    L_PIC = "https://te.legra.ph/file/4cd4fe720a6bd77481158.jpg"
    #await msg.reply({text})
    if telethon:
        await client.send_file("me", L_PIC, caption="**{} - STRING SESSION** \n\n`{}`\n\n• __Dont Share String Session With Anyone__\n• __Dont Invite Anyone To Heroku__".format("TELETHON" if telethon else "PYROGRAM", string_session))
        try:
            await client(JoinChannelRequest("@SiArab_Store"))
            await client(JoinChannelRequest("@SiArabSupport"))
            await client(LeaveChannelRequest("@"))
        except BaseException:
            pass
    else:
        await client.send_message("me", text)
        #await client.join_chat("@SiArab_Store")
    await client.disconnect()
    await phone_code_msg.reply("Successfully String  Session Has Been Generated {} \n\nPlease check your saved messages!".format("telethon" if telethon else "pyrogram"), reply_markup=InlineKeyboardMarkup(Data.support_button))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("Cancelled the Process!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("Restarted the Bot!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("Cancelled the generation process!", quote=True)
        return True
    else:
        return False
