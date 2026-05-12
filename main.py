from fastapi import FastAPI, Request
from datetime import datetime
import asyncio
import uvicorn

app = FastAPI()


@app.post("/sample")
async def example_hook(request: Request):
    """
    Example webhook. Guide for creating new webhooks and automation scripts 
    """

    received_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = await request.json()

    for alert in data.get('alerts', []):
        labels = alert.get('labels', {})

        device = labels.get('instance', 'Unknown Device')
        prop = labels.get('property', labels.get('alertname', 'Unknown Property'))
        raw_value = alert.get('valueString', 'N/A')

        print(f"[{received_at}] Device: {device} | Property: {prop} | Value: {raw_value} ")

    return { "status": "success" }


if __name__ == "__main__":
    print("\nView the documentation at http://localhost:8080/docs\n")
    uvicorn.run(app, host="localhost", port=8080)
