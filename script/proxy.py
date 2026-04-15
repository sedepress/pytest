from DrissionPage import ChromiumPage

page = ChromiumPage()
page.set.auto_handle_alert()
page.get('https://freecarrierlookup.com')

page.ele('@class=form-control required input-lg pageload-focus').input('7602158888', True)
page.ele('@class=btn btn-success btn-lg').click()
print(page.ele('c:#search-result > div > div:nth-child(8) > p').text, 123)


# page = SessionPage()
#
# data = {
#     'test': '456Tabo',
#     'cc': '1',
#     'phonenum': 7602158888,
#     'sessionlogin': '1'
# }
# response = page.session.post('https://freecarrierlookup.com/getcarrier_free.php', data=data)
#
# print(response.text)
