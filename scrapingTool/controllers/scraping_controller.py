from typing import Optional

from fastapi import APIRouter, Request, HTTPException

import constants
from services.scrape_data_service import ScrapingTool

router = APIRouter()


@router.get("/scrape")
async def scrape_data(request: Request,
        page_limit: Optional[int]=1,
        proxy: Optional[str]=None):
    headers = request.headers
    response = {
        "status": 0,
        "message": constants.SOMETHING_WENT_WRONG
    }
    try:
        if str(headers.get('Authorization', None)) != constants.static_token:
            response["message"] = "Token mismatch."
            return response
        if proxy and not proxy.startswith("http"):
            raise HTTPException(status_code=400, detail="Proxy URL should start with 'http'")
        scraping_tool_obj = ScrapingTool()
        response_scraped_data = scraping_tool_obj.scrape_data(page_limit, proxy)
        scraped_data = response_scraped_data["scrapedData"]
        updated_data = response_scraped_data["updatedData"]
        scraping_tool_obj.save_to_json(scraped_data, 'scraped_data.json')
        scraping_tool_obj.notify_status(len(scraped_data), len(updated_data))
        response["status"] = 1
        response["message"] = constants.WEBSCRAPING_SUCCESS
    except Exception as e:
        print(str(e))
    return response
