from bs4 import BeautifulSoup
import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning
import polars as pl




replacement_dict: dict = {
    '₪': '',
    'K': '',
    'k': '',
    '(': '',
    ')': ''
}


def is_english(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    return True


def convert_string_range_to_list(salary: str) -> list:
    try:
        translation_table = str.maketrans(replacement_dict)
        clean_salary = salary.translate(translation_table)
        return [int(clean_salary.split("-")[0]), int(clean_salary.split("-")[1])]
    except Exception:
        return [0, 0]


def convert_job_title_to_english(job_title: str):
    job_title_split = job_title.split()
    english_words = [word for word in job_title_split if is_english(word)]
    title_in_english = ' '.join(english_words)
    if len(title_in_english) == 0:
        return ""
    else:
        return title_in_english


def _scrape(url: str) -> BeautifulSoup | None:
    try:
        warnings.filterwarnings('ignore', category=InsecureRequestWarning)
        page = requests.get(url, verify=False, timeout=2)
        return BeautifulSoup(page.content, "html.parser")
    except Exception:
        return None


def _create_df_schema(columns: list) -> dict:
    data: dict = {"Profession": []}
    for column in columns:
        data.update({column: []})
    return data


def _get_df(columns: list, title_salary: dict) -> pl.DataFrame:
    data: dict = _create_df_schema(columns)

    for job, values in title_salary.items():
        data['Profession'].append(job)
        for i, column in enumerate(columns):
            data[column].append(values[i])

    return pl.DataFrame(data)
