from scrape.scrapers import scrape_speedigital, scrape_dialog, scrape_sqlink, scrape_got_friends

websites_dict: dict = {
    "speedigital": {
        "url": "https://speedigital.co.il/news/salarycompound/",
        "scraper": scrape_speedigital
    },
    "dialog": {
        "url": "https://www.dialog.co.il/salary-potential/salary-tables",
        "scraper": scrape_dialog
    },
    "sqlink": {
        "url": "https://www.sqlink.com/salary/",
        "scraper": scrape_sqlink
    },
    "got_friends": {
        "url": "https://www.gotfriends.co.il/%d7%91%d7%9c%d7%95%d7%92%d7%99%d7%9d/%d7%9b%d7%9e%d7%94-%d7%90%d7%a0%d7%99-%d7%a9%d7%95%d7%95%d7%94-%d7%98%d7%91%d7%9c%d7%aa-%d7%a9%d7%9b%d7%a8-%d7%91%d7%94%d7%99%d7%99%d7%98%d7%a7-2024/",
        "scraper": scrape_got_friends
    }

}
