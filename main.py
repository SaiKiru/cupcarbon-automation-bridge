from fastapi import FastAPI, Request
from datetime import datetime
import asyncio
import uvicorn
import re

app = FastAPI()


@app.post("/alerts")
async def default_webhook(request: Request):
    """
    Example webhook. Guide for creating new webhooks and automation scripts 
    """

    received_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = await request.json()

    for alert in data.get('alerts', []):
        status = alert.get('status', '')

        if status != "firing":
            continue

        labels = alert.get('labels', {})

        node_id = int(labels.get('node_id', '0'))
        prop = labels.get('alertname', 'Unknown Property')
        value = alert.get('values', []).get('A')
        value_string = alert.get('valueString', '')

        print(f"[{received_at}] Device: {node_id} | Property: {prop} | Value: {value} || {value_string}")

    return {"status": "sent"}


def get_query_value(raw_value: str):
    """
    Gets the value from the raw_value property returned by Grafana. Use if the value cannot be found in A, and is complex.
    Example usage:
    value_string = alert.get('valueString', '')
    raw_value = get_query_value(value_string)
    handle_latency(id, raw_value)
    """

    blocks = re.findall(r"\[[^]]+]", raw_value)

    processed_val = 0

    for block in blocks:
        if "type='query'" in block:
            value_match = re.search(r"value=([\d.]+)", block)

            if value_match:
                raw_value = value_match.group(1)
                clean_val = raw_value.strip("'\"")

                try:
                    processed_val = float(clean_val)
                except ValueError:
                    processed_val = clean_val

                return processed_val


if __name__ == "__main__":
    print("\nView the documentation at http://localhost:8080/docs\n")
    uvicorn.run(app, host="localhost", port=8080)
