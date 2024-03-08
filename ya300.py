from time import sleep
from appconfig import ys_cookie, yandex_session_cookie
import requests

ya300_apikey = ""
#
# endpoint = 'https://300.ya.ru/api/sharing-url'
# r = requests.post(endpoint, json = {'article_url': 'https://habr.com/ru/news/729422/'},
#     headers = {'Authorization': f'OAuth {ya300_apikey}'})
#
gen_url = "https://300.ya.ru/api/generation"

cook = {
    "ys": ys_cookie,
    "Session_id": yandex_session_cookie
}
headers = {'Authorization': f'OAuth {ya300_apikey}'}


def video_summary(youtube_video_id: str):
    video_url = f"https://www.youtube.com/watch?v={youtube_video_id}"

    gen_start = requests.post(gen_url, json={"video_url": video_url},
                              headers=headers,
                              cookies=cook)
    gen_start_json = gen_start.json()
    print(gen_start, gen_start.text)
    if "message" in gen_start_json:
        return

    ya300_session_id = gen_start_json['session_id']
    sleep(gen_start_json['poll_interval_ms'] / 1000)

    gen_data = {}
    first_run = True

    while first_run or gen_data['status_code'] == 1:
        first_run = False

        gen_r = requests.post(gen_url, json={"session_id": ya300_session_id, "video_url": video_url},
                              headers=headers,
                              cookies=cook)
        gen_data = gen_r.json()
        if "status_code" in gen_data:
            biba = gen_data.copy()
            biba.pop("keypoints")
            print(biba)

        else:
            print(gen_r, gen_r.text)

        interval = gen_data['poll_interval_ms']
        print(f"Waiting {interval}ms")
        sleep(interval / 1000)

    keypoints = gen_data['keypoints']
    for keypoint in keypoints:
        for thesis in keypoint['theses']:
            print(f"{keypoint['id']}.{thesis['id']}. {thesis['content']}")


if __name__ == "__main__":
    video_summary("LXA_FovAS-A")
