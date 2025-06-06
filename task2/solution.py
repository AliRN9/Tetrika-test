import asyncio
import csv
import logging
import time
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional

import httpx
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

alphabet = ["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О",
            "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я"]


@dataclass
class WikipediaAnimalParser:
    client: httpx.AsyncClient

    BASE_URL = "https://ru.wikipedia.org"
    CATEGORY_URL = f"{BASE_URL}/wiki/Категория:Животные_по_алфавиту"

    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    counter: Counter = field(default_factory=Counter)

    async def get_html(self, url: str) -> Optional[str]:
        """Получает HTML-страницу по URL"""
        try:
            response = await self.client.get(url, headers=self.HEADERS)
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as e:
            logger.error(f"Ошибка при запросе {url}: {e}")
            return None

    def parse_page(self, html: str) -> Optional[str]:
        """Считаем количество название животных на каждой странцие"""
        soup = BeautifulSoup(html, "html.parser")

        for item in soup.select("div.mw-category div.mw-category-group ul li a"):
            name = item.text.strip()
            if not name:
                continue

            first_letter = name[0].upper()
            if first_letter in alphabet:
                self.counter[first_letter] += 1
            # else: логично сделать такую конструкцию, но английские названия попали в русский алфавит поэтому проверим на начало англ алфавита
            #     return
            if first_letter == "A":  # проверка на начало англ алфавита
                return None

        next_link = soup.select_one("a:-soup-contains('Следующая страница')")
        return self.BASE_URL + next_link['href'] if next_link else None

    async def save_to_csv(self, filename: str = "beasts.csv") -> None:
        loop = asyncio.get_running_loop()

        def write_sync():
            with open(filename, mode='w', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                # 1-ый вариант, но в таком случае первая буква Ё так,как ее Юникод идет раньше А
                # for key, value in sorted(self.counter.items(), key=lambda item: item[0]):
                #     writer.writerow([key, value])

                for letter in list(alphabet):
                    writer.writerow([letter, self.counter.get(letter, 0)])

        await loop.run_in_executor(None, write_sync)
        logger.info(f"Результат сохранён в {filename}")

    async def run(self, ) -> None:
        url = self.CATEGORY_URL
        while url:
            # logger.info(f"Обработка: {url}")
            html = await self.get_html(url)
            if not html:
                break
            url = self.parse_page(html)
        await self.save_to_csv()


if __name__ == "__main__":

    async def runner():
        async with httpx.AsyncClient(timeout=30.0) as client:
            parser = WikipediaAnimalParser(client)
            await parser.run()


    start = time.time()
    asyncio.run(runner())
    print(f"{time.time() - start=}")
