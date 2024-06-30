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
    session_string="BQHAnfYAUnSXLtwDM0PSLWrLLEVf4vD0qxvJcUpQOTynTXwW3Y5SazJ7ZJR2Ew4yFwF9g8X_mDzL1acd0153rkgbQG_dL2g2YkXQ-U91FtLY5EaQ4sJkDaMhzgohf4syIgYBCmmkQBFzkBieFQk5ItfMhz3Ct3aRyt5Ayx2hL2mkcePUivKi6mHUq9WjoPOeh69ANuQZETCo3oNybeOA3DRQ0arGnH2WDkvbK1hP6-rMY_uPM8bq1lB8iVtKShTg2CYnvmgeeLj2HSjlblTn15jnj4r1x0m59z_z-lKho4H169YEceNEZjG9DDwbcaWhTYj4NLedQfK5YDMqr4kChdu4NtC8-QAAAAGDvCC_AA"
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
from pyrogram.types import Message
import asyncio

@app.on_message(filters.command("e1", prefixes="!"))
async def evaluate_code(app, message: Message):
    code = message.text.split(maxsplit=1)[1]
    try:
        exec_locals = {}
        exec(code, globals(), exec_locals)
        output = str(exec_locals)
        await message.edit_text(output)
    except Exception as e:
        traceback_str = traceback.format_exc()
        await message.edit_text(f"Error: {e}\n\n{traceback_str}")

@app.on_message(filters.command("s1", prefixes="!"))
async def start(app, message: Message):
    await message.edit_text("Send !e1  to evaluate Python code.")
"""

import io
import sys
import asyncio

@app.on_message(filters.command("e2", prefixes="!"))
async def eva_code(app, message):
    code = message.text.split(maxsplit=1)[1]
    try:
        stdout_capture = io.StringIO()
        sys.stdout = stdout_capture

        stderr_capture = io.StringIO()
        sys.stderr = stderr_capture

        exec(
            f"async def __exec_code():\n{code}\n\nresult = await __exec_code()",
            globals(),
            locals(),
        )

        await locals()["result"]
        
        stdout_value = stdout_capture.getvalue()
        stderr_value = stderr_capture.getvalue()
        if stdout_value:
            await message.edit_text(stdout_value)
        elif stderr_value:
            await message.edit_text(stderr_value)
        else:
            await message.edit_text("No output.")
    except Exception as e:
        tb_str = traceback.format_exception(
            type(e), e, e.__traceback__
        )
        tb_formatted = "".join(tb_str)
        await message.edit_text(f"Error: {e}\n\nTraceback:\n{tb_formatted}")
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__



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
