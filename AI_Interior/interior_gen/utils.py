import requests
import os

API_URL = os.getenv("API_URL")

HEADERS = {
    'Accept': os.getenv("API_ACCEPT", "*/*"),
    'Content-Type': os.getenv("API_CONTENT_TYPE", "application/json"),
    'Origin': os.getenv("API_ORIGIN"),
    'Referer': os.getenv("API_REFERER"),
    'User-Agent': os.getenv("API_USER_AGENT", "Mozilla/5.0")
}

def build_payload(image_url, prompt):
    return {
        'image':    image_url,
        'version':  'black-forest-labs/flux-1.1-pro',
        'prompt':   prompt,
        'guidance': 25,
        'steps':    28,
    }

def post_interior(payload):
    resp = requests.post(API_URL, headers=HEADERS, json=payload)
    resp.raise_for_status()
    return resp.json()

def get_interior_status(task_id):
    resp = requests.get(API_URL, headers=HEADERS, params={'id': task_id})
    resp.raise_for_status()
    return resp.json()
