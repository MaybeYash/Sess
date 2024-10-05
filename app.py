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
"""

import subprocess
import code
import sys
from pyrogram.types import ForceReply

def run_code(code_str):
    try:
        exec(code_str)
    except Exception as e:
        print("Error:", e)

async def run_shell_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Error:", result.stderr)
    except Exception as e:
        print("Error:", e)

class CustomInterpreter(code.InteractiveConsole):
    def runsource(self, source, filename="<input>", symbol="single"):
        source = source.strip()
        if source:
            run_code(source)

async def start_terminal():
    interpreter = CustomInterpreter()
    interpreter.interact()

@app.on_message(filters.command("start"))
def start_command(client, message):
    message.reply_text(
        "Welcome to the Python Code Runner + Shell + Terminal. "
        "Type /run_code to run Python code, /run_shell to execute shell command, or /start_terminal to start Python terminal."
    )

@app.on_message(filters.command("run_code"))
async def run_code_command(client, message):
    await message.reply_text(
        "Enter Python code:",
        reply_markup=ForceReply()
    )

@app.on_message(filters.reply & filters.text)
async def handle_reply(client, message):
    if message.reply_to_message and isinstance(message.reply_to_message.reply_markup, ForceReply):
        code_str = message.text
        run_code(code_str)

@app.on_message(filters.command("run_shell"))
async def run_shell_commands(app:app, message):
    await message.reply_text(
        "Enter shell command:",
        reply_markup=ForceReply()
    )

@app.on_message(filters.reply & filters.text)
async def handle_shell_reply(app:app, message):
    if message.reply_to_message and isinstance(message.reply_to_message.reply_markup, ForceReply):
        command = message.text
        await run_shell_command(command)

@app.on_message(filters.command("start_terminal"))
async def start_terminal_command(app:app, message):
    await start_terminal()

@app.on_message(filters.command("exit"))
async def exit_command(app:app, message):
    await message.reply_text("Exiting...")
    app.stop()


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
