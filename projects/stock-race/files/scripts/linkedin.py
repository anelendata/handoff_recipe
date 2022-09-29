# https://ezzeddinabdullah.com/post/linkedin-api-posts/
import json
import os
import requests
import sys


def get_headers():
    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("OAUTH_TOKEN"),
        "LinkedIn-Version": "202209", # {Version in YYYYMM format}"
        "X-Restli-Protocol-Version": "2.0.0",
    }
    return headers


def request_upload(vidoe_file):
    url = "https://api.linkedin.com/rest/videos?action=initializeUpload"
    headers = get_headers()

    file_size = os.path.getsize(video_file)
    payload = {
        "initializeUploadRequest": {
            "owner": "urn:li:person:" + os.getenv("USER_ID"),
            "fileSizeBytes": file_size,
            "uploadCaptions": False,
            "uploadThumbnail": False,
        }
    }
    response = requests.post(
            url=url,
            headers=headers,
            data=json.dumps(payload),
            )
    return response


def upload_video(upload_url, video_file):
    headers = {
            #        "Authorization": "Bearer Redacted",
        "Content-Type": "application/octet-stream",
    }
    res = requests.put(
            url=upload_url,
            headers=headers,
            data=open(video_file, "rb").read())
    return res


def finalize_upload(video_urn, etag):
    url = "https://api.linkedin.com/rest/videos?action=finalizeUpload"
    headers = get_headers()

    payload = {
        "finalizeUploadRequest": {
        "video": video_urn,
        "uploadToken": "",
        "uploadedPartIds": [etag]
        }
    }
    response = requests.post(
            url=url,
            headers=headers,
            data=json.dumps(payload),
            )
    return response

def post(message, video_urn=None, title="Not set"):
    url = "https://api.linkedin.com/rest/posts"
    headers = get_headers()

    payload = {
        "author": "urn:li:person:" + os.getenv("USER_ID"),
        "commentary": message,
        "visibility": "PUBLIC",
        "distribution": {
          "feedDistribution": "MAIN_FEED",
          "targetEntities": [],
          "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    if video_urn:
        content = {
            "media": {
                "title": title,
                "id": video_urn,
            }
        }
        payload["content"] = content

    response = requests.post(
            url=url,
            headers=headers,
            data=json.dumps(payload),
            )
    return response


if __name__ == "__main__":
    video_file = sys.argv[1]
    res = request_upload(video_file)
    print(res.status_code)
    print(res.content)
    print(res.reason)
    if res.status_code != 200:
        print("upload request failed")
        exit()
    upload_url = res.json()["value"]["uploadInstructions"][0]["uploadUrl"]
    video_urn = res.json()["value"]["video"]
    res = upload_video(upload_url, video_file)
    print(res.status_code)
    # print(res.content)
    print(res.reason)
    print(video_urn)
    print(upload_url)
    if res.status_code not in (200, 201):
        print("upload failed")
        exit()
    etag = res.json()["value"]["etag"]
    res = finalize_upload(video_urn, etag)
    print(res.status_code)
    print(res.content)
    print(res.reason)
    res = post(sys.argv[2], video_urn)
    print(res.status_code)
    print(res.content)
    print(res.reason)
