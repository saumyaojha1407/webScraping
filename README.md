Project info

Web Scraping

Tasks to perform:
1. Scrape the product name, price, and image from each page of the catalogue (it’s not necessary to open each product card).
    Different settings can be provided as input, so your tool should be able to recognize them and work accordingly. For the current task, you can implement only two optional settings:
    1. The first one will limit the number of pages from which we need to scrape the information (for example, `5` means that we want to scrape only products from the first 5 pages).
    2. The secod one will provide a proxy string that tool can use for scraping

2. Store the scraped information in a database. For simplicity, you can store it on your PC's local storage as a JSON file in the following format:
    [
        {
        "product_title":"",
        "product_price":0,
        "path_to_image":"", # path to image at your PC
        }
        ]

3. At the end of the scraping cycle, you need to notify designated recipients about the scraping status - send a simple message that will state how many products were scraped and updated in DB during the current session. For simplicity, you can just print this info in the console. However, be aware that there should be an easy way to use another notification strategy.

Keep in mind the following guidelines:

- Ensure type validation and data integrity using appropriate methods. Remember, accurate typing is crucial for data validation and processing efficiency.
- Consider adding a simple retry mechanism for the scraping part. For example, if a page cannot be reached because of a destination site server error, we would like to retry it in N seconds.
- Add simple authentication to the endpoint using a static token.
- Add a scraping results caching mechanism using your favourite in-memory DB. If the scraped product price has not changed, we don’t want to update the data of such a product in the DB.





Implementation:
1. Number of pages check is handled, if input not given then default is one page only
2. Proxy input is handled
3. Retry mechanism is added - here if server error is there then our service will wait for 2 seconds and then retry and this will happen three times.
4. Static auth token check is there so if no "Authorization" header or wrong value is passed in api call then it will throw an error, static auth token is - "SECURE_STATIC_TOKEN"
5. For In memory db task we have defined cache object for now, where we have added a check of no difference in price then db will not be updated.
6. Type Validation is added through out the code
7. Proper oops handling is there
8. Have also made sure that notification and storage strategies can be changed so all that is modular.



curl to hit the api :
curl --location --request GET 'http://localhost:6101/scrape/' \
--header 'Authorization: SECURE_STATIC_TOKEN'

curl --location --request GET 'http://localhost:6101/scrape/?page_limit=5&proxy=http://proxy.example.com:8080' \
--header 'Authorization: SECURE_STATIC_TOKEN'


name of the json file in which response is saved ->scraped_data.json and it is saved in root path

notification message sample - Scraping Status: 120 products scraped, 5 products updated in DB


how to setup the project
python3 -m venv scraping_tool
source scraping_tool_env/bin/activate
**Go to the project directory
pip install -r requirements

how to run the project
python3 main.py
