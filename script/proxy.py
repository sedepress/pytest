import requests

cookies = {
    'PHPSESSID': '78256ebt61le7vudq79d8bm907',
    '_ga': 'GA1.2.613962221.1755675688',
    '_gid': 'GA1.2.308913265.1755675688',
    'cf_clearance': 'UsNXOkAx1.5XAZeYeyJ4tD8kwe3KCEpjGAHzyFMKnu8-1755764967-1.2.1.1-Gt557Zs5aSZjv6m6FveHMcWDxn2hlclmWsyygXdgSPnedXOlbKTh.5yPJz7BbDwTehr80GRdet62NpH_lPpa2uoBOWuDC4VlmsFs.ZDFa2VgkUcofScjnERfjc2qJkSRFnohHBQ5YtcnuT0aD92Vv6t517nXM6SboqnmEV6oLEGa0pu.kuG1odJNnFebsXnTJ2i.cyMezYUbl56Basvfmih1s9uVNnF2VYPgT9OAGVU',
    '_ga_4JSC4GJHB3': 'GS2.2.s1755764968$o4$g0$t1755764968$j60$l0$h0',
    '__gads': 'ID=67ec3cd6a78a0163:T=1755675688:RT=1755764967:S=ALNI_MZm45eCmmymGlxPcxbBC0lkawLRkQ',
    '__gpi': 'UID=000011834b99d1e6:T=1755675688:RT=1755764967:S=ALNI_MZb7MpLEEnHqjbgkgsUUUBibpkcIw',
    '__eoi': 'ID=e0c330f59c61e8dd:T=1755675688:RT=1755764967:S=AA-AfjYbduvrDLcWZFsoxV1GzKvi',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://freecarrierlookup.com',
    'priority': 'u=0, i',
    'referer': 'https://freecarrierlookup.com/',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    # 'cookie': 'PHPSESSID=78256ebt61le7vudq79d8bm907; _ga=GA1.2.613962221.1755675688; _gid=GA1.2.308913265.1755675688; cf_clearance=UsNXOkAx1.5XAZeYeyJ4tD8kwe3KCEpjGAHzyFMKnu8-1755764967-1.2.1.1-Gt557Zs5aSZjv6m6FveHMcWDxn2hlclmWsyygXdgSPnedXOlbKTh.5yPJz7BbDwTehr80GRdet62NpH_lPpa2uoBOWuDC4VlmsFs.ZDFa2VgkUcofScjnERfjc2qJkSRFnohHBQ5YtcnuT0aD92Vv6t517nXM6SboqnmEV6oLEGa0pu.kuG1odJNnFebsXnTJ2i.cyMezYUbl56Basvfmih1s9uVNnF2VYPgT9OAGVU; _ga_4JSC4GJHB3=GS2.2.s1755764968$o4$g0$t1755764968$j60$l0$h0; __gads=ID=67ec3cd6a78a0163:T=1755675688:RT=1755764967:S=ALNI_MZm45eCmmymGlxPcxbBC0lkawLRkQ; __gpi=UID=000011834b99d1e6:T=1755675688:RT=1755764967:S=ALNI_MZb7MpLEEnHqjbgkgsUUUBibpkcIw; __eoi=ID=e0c330f59c61e8dd:T=1755675688:RT=1755764967:S=AA-AfjYbduvrDLcWZFsoxV1GzKvi',
}

data = {
    'test': '456Tabo',
    'cc': '1',
    'phonenum': '7602158888',
    'sessionlogin': '1',
}

response = requests.post('https://freecarrierlookup.com/getcarrier_free.php', cookies=cookies, headers=headers, data=data)
print(response.text)