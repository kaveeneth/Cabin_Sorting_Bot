import logging
import random
import time
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from config import Config
from database import *
from telethon.sync import TelegramClient, events
from telethon.tl.types import InputPeerChannel
import os
from io import BytesIO
import io
from telethon import Button
import re
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# logger = logging.getLogger(__name__)




# Set new commands

cabins = {
    "Cabin 1": {"Name": "Ares", "ID": -1001792883189, "Image": "https://telegra.ph/file/919ddf9ee3fd3a214f3b5.jpg"},
    "Cabin 2": {"Name": "Artemis", "ID": -1002060612061, "Image": "https://telegra.ph/file/0f76dbed65b9b1382313c.jpg"},
    "Cabin 3": {"Name": "Poseidon", "ID": -1001770822860, "Image": "https://telegra.ph/file/4449301c03532b2994159.jpg"},
    "Cabin 4": {"Name": "Hephaestus", "ID": -1001773388041, "Image": "https://te.legra.ph/file/a276e83109d9bea4f9319.jpg"},
    "Cabin 5": {"Name": "Hades", "ID": -1001785776905, "Image": "https://te.legra.ph/file/5ce59d4aa5e8d74fdc418.jpg"},
    "Cabin 6": {"Name": "Apollo", "ID": -1001657293814, "Image": "https://te.legra.ph/file/bd9b8795890ee81f397f9.jpg"},
    "Cabin 7": {"Name": "Demeter", "ID": -1001602115494, "Image": "https://telegra.ph/file/08c4227dea2120689a786.jpg"},
    "Cabin 8": {"Name": "Dionysus", "ID": -1001613009885, "Image": "https://telegra.ph/file/aeec774d08f44b7de4afd.jpg"},
    "Cabin 9": {"Name": "Zeus", "ID": -1001685383869, "Image": "https://te.legra.ph/file/c14665a99e4dfdc246325.jpg"},
    "Cabin 10": {"Name": "Aphrodite", "ID": -1001747105379, "Image": "https://te.legra.ph/file/961164d84b137741d0a6f.jpg"},
    "Cabin 11": {"Name": "Athena", "ID": -1001560750799, "Image": "https://te.legra.ph/file/e9dc276a8db66c347bd32.jpg"},
    "Cabin 11": {"Name": "Hermies", "ID": -1001720418421, "Image": "https://te.legra.ph/file/a5077e97d84cd7d18eb61.jpg"}

}

async def force_subscribe(c, id):
    try:     
        await c.get_chat_member("CyberLine_Official", id)
        await c.get_chat_member("percy_jackson_fan_Sl_PJFSL", id)
        return True
    except UserNotParticipant:
        c1 = [InlineKeyboardButton("𝙲𝚢𝚋𝚎𝚛𝙻𝚒𝚗𝚎 『🇱🇰』", url="t.me/CyberLine_Official")]  
        c2 = [InlineKeyboardButton("𝗣𝗲𝗿𝗰𝘆 𝗝𝗮𝗰𝗸𝘀𝗼𝗻 𝐅𝐚𝐧𝐬 🇱🇰🇱🇰 ˢᴸ ᵒᶠᶠⁱᶜⁱᵃˡ 【】ℙ𝕁𝔽𝕊𝕃™️°【】", url='t.me/percy_jackson_fan_Sl_PJFSL')]
        await c.send_message(id, "**Please Join These Channels And Try Again /start**", reply_markup=InlineKeyboardMarkup([c1, c2]))
        return False


def get_id_and_image_by_name(cabin_name,cabins=cabins):
    for cc, info in cabins.items():
        if info["Name"] == cabin_name:
            return info["ID"], info["Image"]
    return None, None


papp = Client("pbot",
                   api_id=Config.APP_ID,
                   api_hash=Config.API_HASH,
                   bot_token=Config.BOT_TOKEN)

tapp = TelegramClient("tbot", Config.APP_ID, Config.API_HASH).start(bot_token=Config.BOT_TOKEN)



@tapp.on(events.NewMessage(pattern="/start"))
async def start_command_handler(event):
    t = await force_subscribe(c=papp, id=event.sender.id)
    if t:
        user = event.sender
        sorted_users = db.get_users()
        try:
            try:
                if str(user.id) in sorted_users:
                    await event.reply(f"You have already been sorted into a Cabin **{sorted_users[str(user.id)]['CabinNm']}**. You cannot do it again.")
                    return
                else:
                    cabin_name = random.choice(list(cabins.keys()))
                    s = await event.get_sender()
                    async with tapp.conversation(event.chat_id) as x:
                        e = await event.get_chat()
                        s = await event.get_sender()
                        await x.send_message("""**__𝑾𝒆𝒍𝒄𝒐𝒎𝒆 𝒕𝒐 𝑷.𝑱.𝑭.𝑺.𝑳. - 𝑵𝒆𝒘 𝑴𝒆𝒎𝒃𝒆𝒓 𝑰𝒏𝒇𝒐𝒓𝒎𝒂𝒕𝒊𝒐𝒏__**

        Hey there, fellow demigod and Percy Jackson fan! 🌟 We're thrilled to welcome you to the Percy Jackson Fan Society, or as we fondly call it, P.J.F.S.L. Your journey into the world of Camp Half-Blood is about to begin, and we're here to help you get to your cabin and meet fellow demigod siblings!

        Rest assured, your information is safe with us. We take our responsibility for your data seriously and ensure it doesn't end up in the hands of any monsters. 😉

        Please take a moment to fill out th!e following information, so we can sort you into your cabin group and connect you with your fellow campers. This way, you'll be all set to embark on your quest for adventure and friendship within our P.J.F.S.L. community.
                        """
                        )
                        await x.send_message("Full Name :\n`[Send Your Full Name]`")
                        name = await x.get_response() 
                        if name:
                            await x.send_message("Your Birthday : \n`[ Send Your Bithdate in this format - yy/mm/dd\nExample : 2004.02.25 ]`")
                            age = await x.get_response() 
                            if age:
                                await x.send_message("Email (Not Essential) :\n`[Send Your Email Address if You Don't Have One Just send N or n ]`")
                                mail = await x.get_response()  
                                if mail:
                                    await x.send_message("Your School : \n`[Send Your School Name]`")
                                    git = await x.get_response()  
                                    if git:
                                        await x.send_message("Nearby City:\n`[Send Your Nearby City Name]`")
                                        bg = await x.get_response()  
                                        if bg:
                                            img = cabins[cabin_name]["Image"]
                                            print(img)
                                            await x.send_file(file=img, caption=f"**Congratulations {name.message}! You have been sorted into {cabin_name}. May the blessings of {cabins[cabin_name]['Name']} be with you! \n\nThank you for providing your information. Please await confirmation from our team regarding your request to join your designated cabin. Your patience is appreciated as we process your application. ❤️\n\nBest regards,\nPJFSL Team\n\nPowered By [𝙲𝚢𝚋𝚎𝚛𝙻𝚒𝚗𝚎 『🇱🇰』](https://t.me/CyberLine_Official)**")
                                            FileName = f'{s.username}_{s.id}.txt'
                                            msg = f'''
        Application From [{s.first_name}][@{s.username}]

        👤 Name : {name.message}
        🌍 Birth Date : {age.message}
        📧 Email : {mail.message}
        🌐 School : {git.message}
        💼 City : {bg.message}
        🚧 Cabin : `{cabins[cabin_name]["Name"]}`
        '''
                                            with io.open(FileName, 'w', encoding='utf-8') as f:
                                                f.write(msg)
                                            approve_button = [InlineKeyboardButton("Approve", callback_data=b'approve')]  
                                            decline_button = [InlineKeyboardButton("Decline", callback_data=b'decline')]  
                                            cbn = [InlineKeyboardButton(" Contact Us 📞", user_id=str(5022571894))]
                                            userbtn = [InlineKeyboardButton("User", user_id=str(event.sender.id))]
                                            reply_markup = InlineKeyboardMarkup([approve_button + decline_button, userbtn, cbn])
                                            if s.username:
                                                un = s.username
                                            else:
                                                un = s.id
                                            db.add_users(s.id, name=name.message, bd=age.message, mail=mail.message, scl=git.message, city=bg.message, uname=un, cabin=cabins[cabin_name]["Name"], cnum=cabin_name)
                                            if len(msg) > 4096:
                                                await papp.send_document(Config.LOG, document=FileName, caption=f'{s.id}\n\nApplication From [{s.first_name}][@{s.username}]', reply_markup=reply_markup)
                                            else:
                                                await papp.send_message(Config.LOG, text=f'{s.id}\n\n{msg}', reply_markup=reply_markup)
                                            os.remove(FileName)
            except TypeError:
                cabin_name = random.choice(list(cabins.keys()))
                s = await event.get_sender()
                async with tapp.conversation(event.chat_id) as x:
                    e = await event.get_chat()
                    s = await event.get_sender()
                    await x.send_message("""**__𝑾𝒆𝒍𝒄𝒐𝒎𝒆 𝒕𝒐 𝑷.𝑱.𝑭.𝑺.𝑳. - 𝑵𝒆𝒘 𝑴𝒆𝒎𝒃𝒆𝒓 𝑰𝒏𝒇𝒐𝒓𝒎𝒂𝒕𝒊𝒐𝒏__**

        Hey there, fellow demigod and Percy Jackson fan! 🌟 We're thrilled to welcome you to the Percy Jackson Fan Society, or as we fondly call it, P.J.F.S.L. Your journey into the world of Camp Half-Blood is about to begin, and we're here to help you get to your cabin and meet fellow demigod siblings!

        Rest assured, your information is safe with us. We take our responsibility for your data seriously and ensure it doesn't end up in the hands of any monsters. 😉

        Please take a moment to fill out th!e following information, so we can sort you into your cabin group and connect you with your fellow campers. This way, you'll be all set to embark on your quest for adventure and friendship within our P.J.F.S.L. community.
                    """
                    )
                    await x.send_message("Full Name: \n`[Send Your Full Name]`")
                    name = await x.get_response() 
                    if name:
                        await x.send_message("Your Birthday: \n`[ Send Your Bithdate in this format - yy/mm/dd\nExample : 2004.02.25 ]`")
                        age = await x.get_response() 
                        if age:
                            await x.send_message("Email(Not Essential): \n`[Send Your Email Address if You Don't Have One Just send N or n]`")
                            mail = await x.get_response()  
                            if mail:
                                await x.send_message("Your School: \n`[Send Ur School Name]`")
                                git = await x.get_response()  
                                if git:
                                    await x.send_message("Nearby City:\n`[Send Your Nearby City Name]`")
                                    bg = await x.get_response()  
                                    if bg:
                                        img = cabins[cabin_name]["Image"]
                                        print(img)
                                        await x.send_file(file=img, caption=f"**Congratulations {name.message}! You have been sorted into {cabin_name}. May the blessings of {cabins[cabin_name]['Name']} be with you! \n\nThank you for providing your information. Please await confirmation from our team regarding your request to join your designated cabin. Your patience is appreciated as we process your application. ❤️\n\nBest regards,\nPJFSL Team\n\nPowered By [𝙲𝚢𝚋𝚎𝚛𝙻𝚒𝚗𝚎 『🇱🇰』](https://t.me/CyberLine_Official)**")
                                        FileName = f'{s.username}_{s.id}.txt'
                                        msg = f'''
        Application From [{s.first_name}][@{s.username}]

        👤 Name: `{name.message}`
        🌍 B Date:`{age.message}`
        📧 Email:`{mail.message}`
        🌐 School:`{git.message}`
        💼 City:`{bg.message}`
        🚧 Cabin: `{cabins[cabin_name]["Name"]}`
        '''
                                        with io.open(FileName, 'w', encoding='utf-8') as f:
                                            f.write(msg)
                                        approve_button = [InlineKeyboardButton("Approve", callback_data=b'approve')]  
                                        decline_button = [InlineKeyboardButton("Decline", callback_data=b'decline')]  
                                        cbn = [InlineKeyboardButton(" Contact Us 📞", user_id=str(5022571894))]
                                        userbtn = [InlineKeyboardButton("User", user_id=str(event.sender.id))]
                                        reply_markup = InlineKeyboardMarkup([approve_button + decline_button, userbtn, cbn])
                                        if s.username:
                                            un = s.username
                                        else:
                                            un = s.id
                                        db.add_users(s.id, name=name.message, bd=age.message, mail=mail.message, scl=git.message, city=bg.message, uname=un, cabin=cabins[cabin_name]["Name"], cnum=cabin_name)
                                        if len(msg) > 4096:
                                            await papp.send_document(Config.LOG, document=FileName, caption=f'{s.id}\n\nApplication From [{s.first_name}][@{s.username}]', reply_markup=reply_markup)
                                        else:
                                            await papp.send_message(Config.LOG, text=f'{s.id}\n\n{msg}', reply_markup=reply_markup)
                                        os.remove(FileName)
        except TimeoutError:
            event.reply("Time Out send /start again and Try Again")
    else:
        return



@tapp.on(events.CallbackQuery)
async def button_click_handler(event):
    m = await event.get_message()
    string = m.text
    id = re.findall(r'\d+', string)[0]
    if event.data == b'approve':
        cnum = db.get_users()[str(id)]["CabinNo"]
        link = await papp.create_chat_invite_link(cabins[cnum]["ID"], member_limit=1)
        print(link)
        await papp.send_message(int(id), f"""**Congratulations! {db.get_users()[str(id)]["Name"]} 🥳  Your request to join your designated cabin has been accepted. Welcome officially to the Percy Jackson Fan Club Sri Lanka! 🎉 We're thrilled to have you as part of our community and look forward to the adventures and camaraderie that lie ahead.

You can now access your cabin group by following this link : [{link.invite_link}]

Feel free to reach out if you have any questions or need assistance as you settle in. Once again, welcome aboard!**""", reply_markup = InlineKeyboardMarkup([
                                                                                                                            [InlineKeyboardButton("Join Here", url=link.invite_link)],
                                                                                                                            [InlineKeyboardButton("Contact Us 📞", user_id=str(5022571894))]
                                                                                                                        ]))
    elif event.data == b'decline':
        dt = db.get_users()
        dt.pop(str(id))
        Users.set(dt)
        await papp.send_message(int(id), "**We're sorry to inform you that we have to decline your request at this time. Please ensure that the information provided matches our requirements accurately. ❗️ Please retry by using the correct information. Thank you for your understanding.**")
    await m.delete()


# @papp.on_message(filters.command("start"))
# async def start(_, message: Message):
#     user = message.from_user
#     sorted_users = db.get_users()
#     try:
#         if str(user.id) in sorted_users:
#             cname = get_cabin_number(list(sorted_users[str(user.id)].values())[0])
#             await message.reply_text(f"You have already been sorted into a Cabin **{list(sorted_users[str(user.id)].values())[0]}**`[{cname}]`. You cannot do it again.")
#             return
#         else:
#             m = message.reply_text("Analyzing... Please wait...")
#             time.sleep(5)
#             cabin_name = random.choice(list(cabins.keys()))
#             db.add_users(user.id,message.from_user.first_name, cabins[cabin_name])
#             m.edit(f"Congratulations {user.first_name}! You have been sorted into **{cabin_name}**. "
#                             f"May the blessings of **{cabins[cabin_name]}** be with you! "
#                             f"\n\nThis bot is developed and actively monitored by [Kaveesha Nethmal](https://t.me/jason_spqr_roman_kr). If there is any problem, please feel free to contact Kaveesha.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join This Group", url="https://t.me/+qn4Sr_FqDc1hNTc1")]]), disable_web_page_preview=True)
#             log_message = f"**New user sorted:**\n\n **ID** - `{user.id}`\n **Username** - `{user.username}`\n**Name** - {user.mention}\n**Cabin** - `{cabins[cabin_name]}`"
#             await papp.send_message(Config.LOG, log_message, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("User", user_id=str(message.from_user.id))]]))
#     except TypeError:
#         m = message.reply_text("Analyzing... Please wait...")
#         time.sleep(5)
#         cabin_name = random.choice(list(cabins.keys()))
#         db.add_users(user.id, message.from_user.first_name, cabins[cabin_name])
#         m.edit(f"Congratulations {user.first_name}! You have been sorted into **{cabin_name}**. "
#                         f"May the blessings of **{cabins[cabin_name]}** be with you! "
#                         f"\n\nThis bot is developed and actively monitored by [Kaveesha Nethmal](https://t.me/jason_spqr_roman_kr). If there is any problem, please feel free to contact Kaveesha.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join This Group", url="https://t.me/+qn4Sr_FqDc1hNTc1")]]), disable_web_page_preview=True)
#         log_message = f"**New user sorted:**\n\n **ID** - `{user.id}`\n **Username** - `{user.username}`\n**Name** - {user.mention}\n**Cabin** - `{cabins[cabin_name]}`"
#         await papp.send_message(Config.LOG, log_message, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("User", user_id=str(message.from_user.id))]]))

@papp.on_message(filters.command("info") & filters.chat(Config.LOG))
async def start(_, message: Message):
    id = message.text.split()
    id = str(int(id[1].replace(" ","")))
    s = db.get_users()[id]

    await message.reply_text(f"""
**User Details In Database**
                             
Name - {s["Name"]}
Birth Date - {s["Birthdate"]}
Username - {s["Username"]}
Cabin - {s["CabinNm"]}
City - {s["City"]}
Email - {s["Email"]}
School - {s["School"]}
    """, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("User", user_id=str(message.from_user.id))]]))
 
@papp.on_message(filters.command("devs"))
async def unknown(_, message: Message):
    await message.reply_text("**@GishanKrishka** & **@jason_spqr_roman_Kr**")




@papp.on_message(filters.incoming & ~filters.command(["start", "info", "devs"] & ~filters.text))
def unknown(_, message: Message):
    message.reply_text("Sorry, I didn't understand that command.")

papp.run()

tapp.run_until_disconnected()
