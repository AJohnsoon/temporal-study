import httpx
import os
from temporalio import activity
from src.common.config import settings
from dotenv import load_dotenv

load_dotenv()

URL = settings.service_host
API_KEY = settings.service_apikey

@activity.defn(name="fetch_nasa_apod")
async def fetch_nasa_apod() -> dict:
    url = f"{URL}?api_key={API_KEY}"
    async with httpx.AsyncClient(verify=False) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()


@activity.defn(name="fetch_nasa_neows")
async def fetch_nasa_neows(data) -> dict:
        
    start = data.get('inputs').get('start_time')
    end = data.get('inputs').get('end_time')
    
    url = f"{URL}?start_date={start}&end_date={end}&api_key={API_KEY}"
    async with httpx.AsyncClient(verify=False) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()
