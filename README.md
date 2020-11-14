# Scrapy-project
This project is an implentation of simple scrapy project, which first crawl over the price comparison website [apomio](https://www.apomio.de) and store the result in a sqlite database.\
**Requirement** : [conda](https://docs.conda.io/en/latest/)
## Structure
- spiders
  - apomio_spider.py: *perfroms web crawl*
- items.py: *define format of the parsed data*
- middlewares.py
- model.py: *specify the schema in the DB*
- pipelines.py: *control the whole process (crawl and store to DB)*
- settings.py
## Usage
1. Clone the project
2. Set up the virtual environment :\
  `conda env create -f environment.yml`
3. Activate the virtual environment :\
  `conda activate scrapyProject`
4. Start crawling the website with the spider :\
  `scrapy crawl apomio`
5. Query the stored data through sqlite :\
  `sqlite3 scrapy_apomio.db`
## Issue
- Blocked by the website: Even though the `USER_AGENT` was set and `DOWNLOAD_DELAY` were set, the spider was still blocked by the website once in a while.
- PZN doesn't match for the `show more` webpage: \
  The show more webpage of **PZN-1587486** doesn't match the original one and it's **14470116** instead. But it is likely to be just an exception.
### Reference
- [Scrapy Tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html)
- [A Minimalist End-to-End Scrapy Tutorial](https://towardsdatascience.com/a-minimalist-end-to-end-scrapy-tutorial-part-i-11e350bcdec0)
