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

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@app.on_message(filters.command("eval"))
async def eval(client, message):
    if len(message.text.split()) < 2:
        return await message.reply_text("`Input Not Found!`")

    cmd = message.text.split(maxsplit=1)[1]
    status_message = await message.reply_text("Processing ...")
    start = datetime.now()
    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
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
        evaluation = "Success"
    end = datetime.now()
    ping = (end - start).microseconds / 1000
    final_output = "<b>📎 Input</b>: "
    final_output += f"<code>{cmd}</code>\n\n"
    final_output += "<b>📒 Output</b>:\n"
    final_output += f"<code>{evaluation.strip()}</code> \n\n"
    final_output += f"<b>✨ Taken Time</b>: {ping}<b>ms</b>"
    if len(final_output) > 4096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await reply_to_.reply_document(
                document=out_file,
                caption=cmd,
                disable_notification=True,
                parse_mode=enums.ParseMode.HTML,
            )
    else:
        await status_message.edit_text(final_output, parse_mode=enums.ParseMode.HTML)

app.run()
