import requests


def parse_cookie(string):
    cookies = {}
    data = string.split(";")
    for pair in data:
        key, value = pair.split("=")
        cookies[key] = value

    return cookies


payload = {'time_spent': '5'}
url = 'https://go.teachbase.ru/mobile/v3/course_sessions/700142/materials/2679822/track'
cookies_string = "tmr_lvid=64d3d0baccf38eff5bb96cfa6e58330f; tmr_lvidTS=1699310078932; carrotquest_device_guid=80998816-2b04-4f9e-91c1-b885078187fd; carrotquest_uid=1570364928273940671; carrotquest_auth_token=user.1570364928273940671.52074-6cb252e075595a7e9ef75bea39.2f5a3f06462a89fb9286980d1a20d24f78f32a102525c588; _lfa=LF1.1.a5631b4bf99088ca.1699310079481; _ga=GA1.2.14150470.1699310081; _ym_uid=1699310081980449626; _ym_d=1699310081; go__tb2_session=4a324362c26462fd6260279c1ca77898; account_id=eyJfcmFpbHMiOnsibWVzc2FnZSI6Ik5URXpNVEk9IiwiZXhwIjoiMjAyMy0xMi0zMFQxMTozMDowMC4xNDZaIiwicHVyIjpudWxsfX0%3D--fa7fbd7abd6d6152949f5ef8be322bb9ddf459a2; member_session_uid=eyJfcmFpbHMiOnsibWVzc2FnZSI6IkltTmpaV1V4TmpFMkxUZG1ORGN0TkRBNE5pMWhPRFpsTFdObVpEZzBNRGs0T1Rsa05TST0iLCJleHAiOiIyMDQzLTExLTMwVDExOjMwOjAwLjcxMFoiLCJwdXIiOm51bGx9fQ%3D%3D--f1b331c1c047ce557fc2e627a327a8cf1b73e679; remember_me_token=eyJfcmFpbHMiOnsibWVzc2FnZSI6IkluZzBVV0Z3YVdGRlEyZGthbEZ0YjNCemVFZDRJZz09IiwiZXhwIjoiMjAyNC0wMi0yOFQxMTozMDoxMS4xNjdaIiwicHVyIjpudWxsfX0%3D--5cb3020c6417ca04dffba45ef41bf46c3e3e3ed4; _fbp=fb.1.1702122347516.597454672; carrotquest_realtime_services_transport=wss; carrotquest_jwt_access=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE3MDI2NDQzMjgsImlhdCI6MTcwMjY0MDcyOCwianRpIjoiZTZhMWFjZWE2Yzc0NGNmNjllYjBjMzZlZjYyZWVhZTYiLCJhY3QiOiJ3ZWJfdXNlciIsImN0cyI6MTcwMjY0MDcyOCwicm9sZXMiOlsidXNlci4kYXBwX2lkOjUyMDc0LiR1c2VyX2lkOjE1NzAzNjQ5MjgyNzM5NDA2NzEiXSwiYXBwX2lkIjo1MjA3NCwidXNlcl9pZCI6MTU3MDM2NDkyODI3Mzk0MDY3MX0.3M_R1_MZLM_EbJLp7pHLpreC9mv1mnzA17fQ5QRb5PQ; _gid=GA1.2.1306722505.1702640704; _ym_isad=2; _ym_visorc=w; _ga=GA1.3.14150470.1699310081; _gid=GA1.3.1306722505.1702640704; tz=10; carrotquest_session=wfe2dcd1gzua61rpr0vvpumrgfm1fxee; carrotquest_session_started=1; amplitude_id_093db16a199b50f7d346d90f10146f81teachbase.ru=eyJkZXZpY2VJZCI6ImU1NzI0MWQ4LTVjOTAtNDMzOC04ZmI5LTcxMWY4MTUyZWQ5YVIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTcwMjY0MDcxMTE4OSwibGFzdEV2ZW50VGltZSI6MTcwMjY0MjQzMTg1MSwiZXZlbnRJZCI6MCwiaWRlbnRpZnlJZCI6MCwic2VxdWVuY2VOdW1iZXIiOjB9; _ga_84JMK3MLJS=GS1.2.1702640705.5.1.1702642432.60.0.0; X-CSRF-TOKEN=ejR%2Fk8W9jR1OX99bKYm3X1ci2O68HB4NMfdkTJ0hmHhPchQkaR%2B1S2T8CMoOpjG%2BQGKrxQUvZQNr%2FB7tjCwszg%3D%3D"
cookies = parse_cookie(cookies_string)

response = requests.post(url=url, cookies=cookies, data=payload)
print(response.status_code)
