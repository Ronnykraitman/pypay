# -*- coding: utf-8 -*-
import polars as pl

from scrape.scraping_utils import convert_job_title_to_english, convert_string_range_to_list, _scrape, _get_df


def scrape_speedigital(url: str):
    columns = ["0-1 years", "1-2 years", "3-5 years", "Management"]
    title_salary: dict = {}

    soup = _scrape(url)
    if not soup:
        return pl.DataFrame()

    tables = soup.find_all("tbody")

    for table in tables:
        job_row = table.find_all("tr")
        for job in job_row:
            salaries_as_list = []
            job_cell = job.find_all("td")
            job_title = job_cell[0].text
            title_in_english = convert_job_title_to_english(job_title)
            if title_in_english != "" and len(job_cell) == 5:
                for i in range(1, len(job_cell)):
                    salaries_as_list.append(convert_string_range_to_list(job_cell[i].text.strip()))

                title_salary.update({title_in_english.title(): salaries_as_list})

    return _get_df(columns, title_salary)


def scrape_dialog(url: str):
    columns = ["0-2 years", "2-5 years", "5-10 years", "Management"]
    title_salary: dict = {}

    soup = _scrape(url)
    if not soup:
        return pl.DataFrame()

    jobs = soup.find_all("div", class_="table-row")

    for job in jobs:
        salaries_as_list = []
        job_row = job.find_all("div", class_="table-cell")
        job_title = job_row[0].text
        title_in_english = convert_job_title_to_english(job_title)

        if title_in_english != "":
            for i in range(1, len(job_row)):
                salaries_as_list.append(convert_string_range_to_list(job_row[i].text.strip()))

            title_salary.update({title_in_english.title(): salaries_as_list})

    return _get_df(columns, title_salary)


def scrape_sqlink(url: str):
    columns = ["0-1 years", "1-2 years", "3-5 years", "Management"]
    title_salary: dict = {}

    soup = _scrape(url)
    if not soup:
        return pl.DataFrame()

    jobs = soup.find_all("div", class_="listRow")
    for job in jobs:
        salaries_as_list = []
        job_title = job.find("div", class_="professionName").text
        title_in_english = convert_job_title_to_english(job_title)
        if title_in_english != "":
            job_salary_range = job.find("div", class_="professionSalary")
            salaries = job_salary_range.find_all("div", class_="price")
            for sal in salaries:
                salaries_as_list.append(convert_string_range_to_list(sal.text.strip()))

            title_salary.update({title_in_english.title(): salaries_as_list})
    return _get_df(columns, title_salary)


def scrape_got_friends(url: str):
    columns = ["0-2", "3-5", "6-10", "Management"]
    title_salary: dict = {}

    soup = _scrape(url)
    if not soup:
        return pl.DataFrame()
    jobs = soup.find_all("div", class_="listRow")

    for job in jobs:
        salaries_as_list = []
        job_title = job.find("div", class_="professionName").text
        title_in_english = convert_job_title_to_english(job_title)
        if title_in_english != "":
            job_salary_range = job.find("div", class_="professionSalary")
            salaries = job_salary_range.find_all("span", class_="link")
            for sal in salaries:
                salaries_as_list.append(convert_string_range_to_list(sal.text.strip()))
            title_salary.update({title_in_english.title(): salaries_as_list})

    return _get_df(columns, title_salary)


########## NOT SUPPORTED YET #############
def scrape_jobinfo():
    url = "https://www.jobinfo.co.il/%D7%98%D7%91%D7%9C%D7%90%D7%95%D7%AA-%D7%A9%D7%9B%D7%A8"
    columns = ["0-2 years", "2-3 years", "3-5 years", "5-10 years", "Management"]

    soup = _scrape(url)

    if not soup:
        return pl.DataFrame()
    jobs = soup.find_all("td", class_="position")

    title_salary: dict = {}
    for job in jobs:
        salaries_as_list = []
        job_title = job.find("target", class_="_blank").text
        title_in_english = convert_job_title_to_english(job_title)
        if title_in_english != "":
            job_salary_range = job.find("div", class_="professionSalary")
            salaries = job_salary_range.find_all("div", class_="range")
            for sal in salaries:
                salaries_as_list.append(convert_string_range_to_list(sal.text.strip()))

            title_salary.update({title_in_english.title(): salaries_as_list})

    return _get_df(columns, title_salary)
