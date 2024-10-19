from pyrogram import Client, filters
import traceback
from datetime import datetime
from pyrogram import enums
import sys
import io

app = Client(
    name="han",
    api_id=29400566,
    api_hash="8fd30dc496aea7c14cf675f59b74ec6f",
    bot_token="7410054834:AAHU5bFbwRHHKkeanZpuAb7R3AXvtMsFd3w"
)

class PSend:
    def __call__(self, message):
        print(message)

    def send(self, message):
        print(message)

async def aexec(code,app, msg,p):
    exec(
        "async def __aexec(app, msg, p): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](app, msg, p)




"""

"""

import subprocess
import code
import sys
from pyrogram.types import ForceReply

from pyrogram import Client, filters
from pyrogram.types import Message
import sqlite3
import random
import string

# Generate a unique invite code
def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# Save the referral in the database
def save_referral(user_id, invite_code):
    # Open a new connection in each thread
    conn = sqlite3.connect('referrals.db', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("INSERT OR REPLACE INTO referrals (user_id, invite_code) VALUES (?, ?)", (user_id, invite_code))
    
    conn.commit()
    conn.close()  # Always close the connection after each operation

# Fetch the inviter's user ID from the invite code
def get_user_id_by_invite_code(invite_code):
    # Open a new connection in each thread
    conn = sqlite3.connect('referrals.db', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM referrals WHERE invite_code = ?", (invite_code,))
    result = cursor.fetchone()

    conn.close()  # Always close the connection after each operation
    return result[0] if result else None

@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    user_id = message.from_user.id  # The new user (invited user)
    user_name = message.from_user.first_name or "Unknown"

    # Check if the user was referred using an invite code
    if len(message.command) > 1:
        start_param = message.command[1]

        # Parse the invite code (e.g., invitedBy_ABC123)
        if start_param.startswith("invitedBy_"):
            invite_code = start_param.split('invitedBy_')[-1]

            # Get inviter's user ID from the invite code
            inviter_id = get_user_id_by_invite_code(invite_code)

            if inviter_id:
                inviter_name = await client.get_users(inviter_id)
                inviter_name = inviter_name.first_name or "Unknown"

                # Send welcome message to the user who joined via invite
                await message.reply(f"Welcome! You were invited by {inviter_name}")

                # Notify the inviter about the successful referral
                await client.send_message(
                    inviter_id, 
                    f"{user_name} joined via your invite link!"
                )

                # Optionally save the referral information
                save_referral(user_id, None)
            else:
                await message.reply("Invalid invite code.")
    else:
        # If no invite code, generate one for the user
        invite_code = generate_invite_code()
        save_referral(user_id, invite_code)

        # Reply with the user's unique invite link
        await message.reply(f"Welcome! Share your invite link: https://telegram.me/SpaceXCode_Bot?start=invitedBy_{invite_code}")


@app.on_message(filters.command("ev") & filters.user([6505111743, 6517565595, 5220416927, 5896960462]))
@app.on_edited_message(filters.command("ev") & filters.user([6505111743, 6517565595, 5220416927, 5896960462]))
async def evalFunc(app:app, message):
    if len(message.text.split()) < 2:
        return await message.reply("**❗️Iɴᴘᴜᴛ ɴᴏᴛ ғᴏᴜɴᴅ...**")

    cmd = message.text.split(maxsplit=1)[1]
    status_message = await message.reply_text("**♻️ Pʀᴏᴄᴇssɪɴɢ...**")
    start = datetime.now()
    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message
    p = PSend()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd,app, message,p)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Sᴜᴄᴄᴇss"
    end = datetime.now()
    ping = (end - start).microseconds / 1000
    final_output = "<b>🔗 Iɴᴘᴜᴛ :</b>\n"
    final_output += f"<pre>{cmd}</pre>\n"
    final_output += "<b>🔰 Oᴜᴛᴘᴜᴛ :</b>\n"
    final_output += f"<pre>{evaluation.strip()}</pre>\n"
    final_output += f"<b>🚀 Cᴏᴍᴘʟᴇᴛᴇ ɪɴ {ping} ᴍs</b>"
    if len(final_output) > 4096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "evFunc.log"
            await reply_to_.reply_document(
                document=out_file,
                caption=cmd,
                disable_notification=True,
                parse_mode=enums.ParseMode.HTML,
            )
    else:
        await status_message.edit_text(final_output, parse_mode=enums.ParseMode.HTML)

app.run()
