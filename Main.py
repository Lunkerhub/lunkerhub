# meta developer: @Honorpadx9lte

from .. import loader, utils
import asyncio

@loader.tds
class TypeWriterMod(loader.Module):
    """Эффект печати с настройками"""
    strings = {
        "name": "TypeWriter",
        "delay_cfg": "Задержка между символами (сек)",
        "cursor_cfg": "Символ курсора",
        "delete_cfg": "Удалять сообщение после завершения?"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("delay", 0.4, lambda: self.strings["delay_cfg"], validator=loader.validators.Float()),
            loader.ConfigValue("cursor", "|", lambda: self.strings["cursor_cfg"]),
            loader.ConfigValue("auto_delete", False, lambda: self.strings["delete_cfg"], validator=loader.validators.Boolean()),
        )

    async def textcmd(self, message):
        """<текст> - Печатать текст с анимацией"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, "<b>Введите текст</b>")

        display_text = ""
        for char in args:
            display_text += char
            await message.edit(f"{display_text}{self.config['cursor']}")
            await asyncio.sleep(self.config['delay'])
        
        await message.edit(display_text)

        if self.config['auto_delete']:
            await asyncio.sleep(2)
            await message.delete()
