# meta developer: @Honorpadx9lte

from .. import loader, utils
import asyncio

@loader.tds
class TypeWriterMod(loader.Module):
    """Эффект печати для Hikka"""
    strings = {"name": "TypeWriter"}

    async def textcmd(self, message):
        """<текст> - Печатать текст с задержкой 0.4с"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, "<b>Введите текст</b>")

        display_text = ""
        for char in args:
            display_text += char
            await message.edit(f"{display_text}|")
            await asyncio.sleep(0.4)
        
        await message.edit(display_text)
