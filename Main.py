from .. import loader, utils
import asyncio

@loader.tds
class SpeedControlMod(loader.Module):
    """Пример модуля с настройкой скорости"""
    strings = {"name": "SpeedControl"}

    def __init__(self):
        # Создаем настройку в конфиге (параметры: имя, дефолт, описание)
        self.config = loader.ModuleConfig(
            "delay", 0.5, "Скорость анимации (от 0.1 до 1.0)"
        )

    @loader.command()
    async def fastcmd(self, message):
        """Команда для теста скорости"""
        # Проверяем, чтобы значение было в рамках разумного
        delay = max(0.1, min(1.0, float(self.config["delay"])))
        
        text = "Это тест скорости..."
        output = ""
        for char in text:
            output += char
            await message.edit(output)
            await asyncio.sleep(delay)
