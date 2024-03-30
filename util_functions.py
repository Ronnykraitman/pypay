import polars as pl
from prettytable import PrettyTable
from simple_term_menu import TerminalMenu

from scrape.websites import websites_dict
from standartization import seniority_with_prof_to_column_dict, seniority_to_column_dict, replace_profession_name, \
    convert_range_to_seniority, add_tag


def convert_df_to_pretty_table(df: pl.DataFrame, table_title: str) -> PrettyTable:
    professions_table = PrettyTable(title=table_title, align="l")
    prof_name: list = df.select(pl.col("Profession")).to_series().to_list()

    for index, key in enumerate(seniority_with_prof_to_column_dict.keys()):
        if index == 0:
            professions_table.add_column(key, prof_name)
        else:
            salary_as_list: list = df.select(pl.col(key)).to_series().to_list()
            salary_as_str: list = list(map(lambda x: str(x[0]) + " - " + str(x[1]) + " K", salary_as_list))
            professions_table.add_column(key, salary_as_str, align="l")

    return professions_table

def transform_combined_dfs_to_single_df(df: pl.DataFrame):
    list_of_columns_to_agg: list = list(seniority_to_column_dict.keys())
    df_agg: pl.DataFrame = df.group_by("Profession").agg(pl.col(list_of_columns_to_agg))
    df_new: pl.DataFrame = df_agg.clone()
    for i in range(1, len(seniority_to_column_dict) + 1):
        col_name: str = df.columns[i]
        df_new: pl.DataFrame = df_new.with_columns(
            pl.col(col_name)
            .map_elements(lambda sal_range: find_min_max_salary(sal_range))
            .alias(col_name)
        )
    return df_new


def find_min_max_salary(sal_range: list):
    filtered_values: list = [[x for x in values if x != 0] for values in zip(*sal_range)]
    if not filtered_values[0] or not filtered_values[1]:
        return []

    min_range = min(filtered_values[0])
    max_range = max(filtered_values[1])
    return [min_range, max_range]


def combine_dfs(dfs: list) -> pl.DataFrame:
    df_new: pl.DataFrame = pl.DataFrame()
    for df in dfs:
        df_new = df_new.vstack(df)
    return df_new

def get_df_filtered_by_profession(df: pl.DataFrame, professions: list) -> pl.DataFrame:
    return df.filter(pl.col("Profession").is_in(professions))


def _select_multiple(professions: list, title: str):
    professions.sort()
    terminal_menu = TerminalMenu(
        professions,
        title=f"{title}:",
        multi_select=True,
        show_multi_select_hint=True,
    )
    terminal_menu.show()
    return list(terminal_menu.chosen_menu_entries)

def _continue_menu():
    options: list = ["Search again", "Main menu"]
    terminal_menu = TerminalMenu(
        options,
        title="Want to search again?",
        show_multi_select_hint=True,
    )
    menu_entry_index = terminal_menu.show()
    options[menu_entry_index]
    return options[menu_entry_index]


def get_input_from_user():
    is_valid = False
    user_input = input("Which salary you wish to get? (in K, like 44, 32 etc.): ")
    while not is_valid:
        try:
            salary: int = int(user_input)
            is_valid = True
            return salary
        except Exception:
            user_input = input("That's not a valid salary. come on.. try again: ")


def _get_all_jobs_as_dfs() -> list:
    list_of_dfs: list = []
    for website in websites_dict.values():
        url = website.get("url")
        scraper = website.get("scraper")
        scraped_df: pl.DataFrame = scraper(url)
        if not scraped_df.is_empty():
            sd_df: pl.DataFrame = scraped_df.pipe(replace_profession_name)
            list_of_dfs.append(sd_df)

    return list_of_dfs


def _get_all_profession_from_dfs(dfs: list):
    list_of_profession: list = []
    for df in dfs:
        list_of_profession += df["Profession"].unique().to_list()

    return list(set(list_of_profession))

def _convert_multiple_dfs_to_single_df(dfs: list) -> pl.DataFrame:
    seniority_standardized_dfs: list = convert_range_to_seniority(dfs)
    multiple_dfs_combined: pl.DataFrame = combine_dfs(seniority_standardized_dfs)
    transposed_profession_df: pl.DataFrame = transform_combined_dfs_to_single_df(multiple_dfs_combined)

    return transposed_profession_df

def show_tags(dfs: list):
    seniority_standardized_dfs: list = convert_range_to_seniority(dfs)
    multiple_dfs_combined: pl.DataFrame = combine_dfs(seniority_standardized_dfs)
    transposed_profession_df: pl.DataFrame = transform_combined_dfs_to_single_df(multiple_dfs_combined)
    add_tag(transposed_profession_df)


