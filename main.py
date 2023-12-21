from fastapi import FastAPI
import wikipedia
from pydantic import BaseModel

app = FastAPI()


class PageByTitleResponse(BaseModel):
    url: str
    title: str
    summary: str
    categories: list[str]


@app.get("/page/{title}", response_model=PageByTitleResponse)
async def page_by_title(title: str):
    page = wikipedia.page(title=title)
    return PageByTitleResponse(url=page.url, summary=page.summary, title=page.title, categories=page.categories)


class SearchResultsResponse(BaseModel):
    results: list[str]


@app.get("/search/{title}", response_model=SearchResultsResponse)
async def search(title: str, results: int = 10):
    return SearchResultsResponse(results=wikipedia.search(title, results=results))


class GeoSearchRequest(BaseModel):
    lat: float
    long: float


class GeoSearchResponse(BaseModel):
    results: list[str]


@app.post("/search/geo", response_model=GeoSearchResponse)
async def categories(req: GeoSearchRequest):
    return GeoSearchResponse(results=wikipedia.geosearch(req.lat, req.long))
