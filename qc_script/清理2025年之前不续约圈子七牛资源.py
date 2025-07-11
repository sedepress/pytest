import json
import time

import requests
from qiniu import build_batch_delete, Auth, BucketManager


def main():
    access_key = 'YO6sRouk-x9NhEJZJ7ameodax-zWlObe6EqfHQK9'
    secret_key = 'YR0NMZRcdPsXpNDXYzLDGWUHy0UVWjnqDpQXfLv0'

    q = Auth(access_key, secret_key)

    bucket = BucketManager(q)

    bucket_name = 'youzan-fansquan'

    default_imgs = ['default_flow_limit.jpg', 'fansquan_default_avatar.png', 'default_avatar_3.svg', 'default_auditing_1.jpg', 'default_thread_img.png']

    page = 1
    forumId = 198
    while True:
        response = requests.get(f'https://fansquan.isv.youzan.com/remote/forum/clean/resource?page={page}&forum_id={forumId}')
        data = response.json()

        keys = []
        if len(data['data']) > 0:
            for item in data['data']:
                print(item)
                attachment_list = json.loads(item['attachment_list'])
                if attachment_list and len(attachment_list) > 0:
                    for attachment in attachment_list:
                        if attachment and attachment.get('filename', '') and attachment['filename'] not in default_imgs:
                            keys.append(attachment['filename'])
        else:
            break

        if len(keys) > 0:
            ops = build_batch_delete(bucket_name, keys)
            ret, info = bucket.batch(ops)
            print('[七牛云清理结果]', ret, info)

        page += 1
        time.sleep(1)

if __name__ == '__main__':
    main()