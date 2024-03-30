from prettytable import PrettyTable
from simple_term_menu import TerminalMenu

from standartization import seniority_to_column_dict, tags_dict, add_tag
from util_functions import _select_multiple, get_df_filtered_by_profession, \
    convert_df_to_pretty_table, _get_all_profession_from_dfs, get_input_from_user, \
    _convert_multiple_dfs_to_single_df, _continue_menu
import polars as pl


def get_salary(dfs: list):
    professions: list = _get_all_profession_from_dfs(dfs)
    while True:
        selected_professions: list = _select_multiple(professions, "The Professions I have info about are")
        transposed_professions_df: pl.DataFrame = _convert_multiple_dfs_to_single_df(dfs)
        filtered_df_by_professions: pl.DataFrame = get_df_filtered_by_profession(transposed_professions_df, selected_professions)
        salary_table: PrettyTable = convert_df_to_pretty_table(filtered_df_by_professions, "Salary ranges")
        print(salary_table)
        continue_selection = _continue_menu()
        if continue_selection == "Main menu":
            from main import start
            start(dfs)




def which_profession_pays_my_bills(dfs: list):
    transposed_profession_df: pl.DataFrame = _convert_multiple_dfs_to_single_df(dfs)
    while True:
        salary: int = get_input_from_user()
        matched_professions: dict = {}

        for i in range(len(transposed_profession_df)):
            row = transposed_profession_df[i]
            matched_professions.update(_find_sal_in_job_seniority(row, salary))

        matched_professions_table = PrettyTable(title=f"Working in these professions can get you {salary} K", align="l")
        matched_professions_table.add_column("Professions", [], align="l")
        matched_professions_table.add_column("Seniority", [], align="l")
        for prof, sen in matched_professions.items():
            matched_professions_table.add_row([prof, sen])

        print(matched_professions_table)
        continue_selection = _continue_menu()
        if continue_selection == "Main menu":
            from main import start
            start(dfs)


def search_profession_by_tags(dfs: list):
    transposed_profession_df: pl.DataFrame = _convert_multiple_dfs_to_single_df(dfs)
    transposed_profession_df = add_tag(transposed_profession_df)
    while True:
        selected_tags: list = _select_multiple(list(tags_dict.keys()), "Available Categories")
        table_title = "Jobs by categoris: " + ", ".join(selected_tags)
        job_by_tag_table: PrettyTable = convert_df_to_pretty_table(
            transposed_profession_df.filter(pl.col("tag").is_in(selected_tags)), table_title)
        print(job_by_tag_table)
        continue_selection = _continue_menu()
        if continue_selection == "Main menu":
            from main import start
            start(dfs)



def _find_sal_in_job_seniority(row: pl.DataFrame, sal: int) -> dict:
    prof_sen_dict: dict = {}
    list_of_seniority = list(seniority_to_column_dict.keys())
    profession: str = row["Profession"][0]
    for seniority in list_of_seniority:
        sal_range: list = row[seniority][0].to_list()
        if sal_range and sal in range(sal_range[0], sal_range[1] + 1):
            if profession not in prof_sen_dict:
                prof_sen_dict[profession] = seniority

    return prof_sen_dict
