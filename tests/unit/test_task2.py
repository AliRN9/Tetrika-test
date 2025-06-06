from pathlib import Path

import httpx

from task2.solution import WikipediaAnimalParser


async def test_parse_page_counts_letters_and_save_to_csv_success(async_client_mock: httpx.AsyncClient, tmp_path: Path,
                                                                 monkeypatch):
    sample_html = """
    <div class="mw-category">
      <div class="mw-category-group">
        <ul>
          <li><a href="/wiki/Антилопа">Антилопа</a></li>
          <li><a href="/wiki/Бобр">Бобр</a></li>
          <li><a href="/wiki/Воробей">Воробей</a></li>
        </ul>
      </div>
    </div>
    <a href="/wiki/Категория:Животные_по_алфавиту/Б">Следующая страница</a>
    """

    filename = tmp_path / "test_output.csv"

    parser = WikipediaAnimalParser(async_client_mock)

    next_url = parser.parse_page(sample_html)

    assert parser.counter["А"] == 1
    assert parser.counter["Б"] == 1
    assert parser.counter["В"] == 1
    assert next_url.endswith("/wiki/Категория:Животные_по_алфавиту/Б")

    await parser.save_to_csv(str(filename))

    assert filename.exists()


async def test_parse_page_terminates__success(async_client_mock: httpx.AsyncClient):
    sample_html = """
    <div class="mw-category">
      <div class="mw-category-group">
        <ul>
          <li><a href="/wiki/Antelope">Antelope</a></li>
          <li><a href="/wiki/Beaver">Beaver</a></li>
          <li><a href="/wiki/Sparrow">Sparrow</a></li>
        </ul>
      </div>
    </div>
    <a href="/wiki/Категория:Животные_по_алфавиту/Б">Следующая страница</a>
    """
    parser = WikipediaAnimalParser(async_client_mock)
    next_url = parser.parse_page(sample_html)
    assert next_url is None

    # print(f"{parser.counter=}")

    assert not parser.counter


async def test_get_html__wrong(async_client_mock: httpx.AsyncClient):
    sample_html = """
    <div class="mw-category">
      <div class="mw-category-group">
        <ul>
          <li><a href="/wiki/Antelope">Antelope</a></li>
          <li><a href="/wiki/Beaver">Beaver</a></li>
          <li><a href="/wiki/Sparrow">Sparrow</a></li>
        </ul>
      </div>
    </div>
    <a href="/wiki/Категория:Животные_по_алфавиту/Б">Следующая страница</a>
    """
    parser = WikipediaAnimalParser(async_client_mock)
    next_url =  parser.parse_page(sample_html)
    assert next_url is None

    # print(f"{parser.counter=}")

    assert not parser.counter
