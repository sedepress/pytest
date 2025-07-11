import requests

def main():
    userIds = [1, 2]
    forumId = 1
    signDates = ['2025-05-01', '2025-05-02', '2025-05-03']

    for userId in userIds:
        for signDate in signDates:
            response = requests.get(
                f'https://fansquan.isv.youzan.com/tool/supplement/sign?forum_id={forumId}&user_id={userId}&sign_date={signDate}')
            print(response.json())

if __name__ == '__main__':
    main()