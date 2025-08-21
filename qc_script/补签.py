import requests

def main():
    userIds = [2604968]
    forumId = 10276
    signDates = ['2025-08-14']

    for userId in userIds:
        for signDate in signDates:
            response = requests.get(
                f'https://fansquan.isv.youzan.com/tool/supplement/sign?forum_id={forumId}&user_id={userId}&sign_date={signDate}')
            print(response.json())

if __name__ == '__main__':
    main()