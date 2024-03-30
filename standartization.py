import polars as pl

seniority_with_prof_to_column_dict: dict = {
    "Profession": 0,
    "Junior Level": 1,
    "Mid Level": 2,
    "Senior Level": 3,
    "Management": 4
}

seniority_to_column_dict: dict = {
    "Junior Level": 1,
    "Mid Level": 2,
    "Senior Level": 3,
    "Management": 4
}

languages: list = ["Java", "Python", "Scala", "TypeScript", "Php", "C++", "C", "C#", ".Net", "Javascript", "Ruby", "Go",
                   "Kotlin"]
developer_addition: list = languages + ["Angular", "React", "Mobile"]

tags_dict: dict = {
    "Language": ["Java Developer", "Python Developer", "Scala Developer", "TypeScript Developer", "Php Developer", "C++ Developer", "C Developer", "C# Developer", ".Net Developer", "JavascriptDeveloper",
                 "Ruby Developer", "Go Developer", "Kotlin Developer", "Node.js Developer"],
    "Data": ["Data Engineer", "Data Scientist", "Data Analyst", "Big Data Developer"],
    "Discipline": ["Full Stack Developer", "Front End Developer", "Back End Developer", "Devops", "QA Engineer", "Ui/Ux", "Mobil Developer"],
    "Framework": ["React Developer", "Angular Developer"]

}

profession_synonym: dict = {
    "C++ Developer": ["C++", "++C", "++C/C", "C/++C", "C++/C", "C/C++"],
    "Node.js Developer": ["Nodejs", "Node Js", "Node.Js", "Nodejs Developer", "Node Js Developer"],
    ".Net Developer": ["Net", ".Net", "Net.", "Net Developer."],
    "Full Stack Developer": ["FullStack", "Fullstack", "Full Stack", "Full stack", "Full Stack Developer",
                             "Fs Developer", "Fs"],
    "Front End Developer": ["FrontEnd", "Frontend", "Front end", "Front End Developer", "Fe Developer", "Fe", "Front End"],
    "Back End Developer": ["BackEnd", "Backend", "Back end" "Back End Developer", "Be Developer", "Be", "Back End"],
    "QA Engineer": ["Qa", "Qa Engineer", "Qa Tester", "QA"],
    "Big Data Developer": ["Big Data", "Big Data Engineer"],
    "Data Engineer": ["Data", "Data Developer"],
    "Data Scientist": ["Data Science"]

}

def replace_profession_name(df: pl.DataFrame):
    new_df: pl.DataFrame = df.clone()
    for official_name, synonyms in profession_synonym.items():
        new_df = new_df.with_columns(
            pl.when(pl.col("Profession").is_in(synonyms))
            .then(pl.lit(official_name))
            .otherwise(pl.col("Profession"))
            .alias("Profession")
        )

    new_df = new_df.with_columns(
        pl.col("Profession")
        .map_elements(
            lambda value: value + " Developer" if value in developer_addition else value)
        .alias("Profession")
    )
    return new_df


def convert_range_to_seniority(dfs: list):
    list_of_dfs: list = []
    seniority_with_prof: list = list(seniority_with_prof_to_column_dict.keys())
    for df in dfs:
        new_df: pl.DataFrame = df.clone()
        new_df.columns = seniority_with_prof
        list_of_dfs.append(new_df)
    return list_of_dfs


def add_tag(df: pl.DataFrame) -> pl.DataFrame:
    df_with_tag: pl.DataFrame = df.with_columns(
        pl.col("Profession")
        .alias("tag")
    )
    null_values = [None] * len(df_with_tag)
    df_with_tag = df_with_tag.with_columns(pl.Series("tag", null_values))
    for tag, professions in tags_dict.items():
        df_with_tag = df_with_tag.with_columns(
            pl.when(pl.col("Profession").is_in(professions)).then(pl.lit(tag)).otherwise(pl.col("tag")).alias("tag")
        )

    return df_with_tag
