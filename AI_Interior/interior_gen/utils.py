import requests

API_URL = 'https://www.decoratly.com/api/interior'
HEADERS = {
    'Accept': '*/*',
    'Content-Type': 'application/json',
    'Origin': 'https://www.decoratly.com',
    'Referer': 'https://www.decoratly.com/photos/rGHu9RVxBBXiCMQBCKYA',
    'User-Agent': 'Mozilla/5.0'
}

def build_payload(image_url, prompt):
    return {
        'image':    image_url,
        'version':  'black-forest-labs/flux-canny-pro',
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
