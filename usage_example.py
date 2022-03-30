import requests

token_raw = requests.post('http://95.163.250.221:8090/token',
    data={
        "username": "igor",
        "password": "secret",
    }
)

token = token_raw.json()["access_token"]
print(f"My token: {token}")

res = requests.post('http://95.163.250.221:8090/send_data',
    json={
        "product_list": ["90019A", "90016B", "90123C"],
        "n": 5
    }, headers={
        "Authorization": f"bearer {token}"
    }
)

print(res.json())
