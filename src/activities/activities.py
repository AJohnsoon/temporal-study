import httpx
import os
from temporalio import activity
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv('URL')
API_KEY = os.getenv('APIKEY')

@activity.defn(name="fetch_nasa_apod")
async def fetch_nasa_apod() -> dict:
    url = f"{URL}?api_key={API_KEY}"
    async with httpx.AsyncClient(verify=False) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()
