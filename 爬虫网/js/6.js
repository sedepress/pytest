window = this, function (n) {
    function r(n, r) {
        var t = (65535 & n) + (65535 & r);
        return (n >> 16) + (r >> 16) + (t >> 16) << 16 | 65535 & t
    }

    function t(n, t, o, u, e, c) {
        return r(function (n, r) {
            return n << e | n >>> 32 - e
        }(r(r(t, n), r(u, c))), o)
    }

    function o(n, r, o, u, e, c, f) {
        return t(r & o | ~r & u, n, r, e, c, f)
    }

    function u(n, r, o, u, e, c, f) {
        return t(r & u | o & ~u, n, r, e, c, f)
    }

    function e(n, r, o, u, e, c, f) {
        return t(r ^ o ^ u, n, r, e, c, f)
    }

    function c(n, r, o, u, e, c, f) {
        return t(o ^ (r | ~u), n, r, e, c, f)
    }

    function f(n, t) {
        var f, i, a, h, g;
        n[t >> 5] |= 128 << t % 32, n[14 + (t + 64 >>> 9 << 4)] = t;
        var l = 1732584193, d = -271733879, v = -1732584194, C = 271733878;
        for (f = 0; f < n.length; f += 16) d = c(d = c(d = c(d = c(d = e(d = e(d = e(d = e(d = u(d = u(d = u(d = u(d = o(d = o(d = o(d = o(a = d, v = o(h = v, C = o(g = C, l = o(i = l, d, v, C, n[f], 7, -680876936), d, v, n[f + 1], 12, -389564586), l, d, n[f + 2], 17, 606105819), C, l, n[f + 3], 22, -1044525330), v = o(v, C = o(C, l = o(l, d, v, C, n[f + 4], 7, -176418897), d, v, n[f + 5], 12, 1200080426), l, d, n[f + 6], 17, -1473231341), C, l, n[f + 7], 22, -45705983), v = o(v, C = o(C, l = o(l, d, v, C, n[f + 8], 7, 1770035416), d, v, n[f + 9], 12, -1958414417), l, d, n[f + 10], 17, -42063), C, l, n[f + 11], 22, -1990404162), v = o(v, C = o(C, l = o(l, d, v, C, n[f + 12], 7, 1804603682), d, v, n[f + 13], 12, -40341101), l, d, n[f + 14], 17, -1502002290), C, l, n[f + 15], 22, 1236535329), v = u(v, C = u(C, l = u(l, d, v, C, n[f + 1], 5, -165796510), d, v, n[f + 6], 9, -1069501632), l, d, n[f + 11], 14, 643717713), C, l, n[f], 20, -373897302), v = u(v, C = u(C, l = u(l, d, v, C, n[f + 5], 5, -701558691), d, v, n[f + 10], 9, 38016083), l, d, n[f + 15], 14, -660478335), C, l, n[f + 4], 20, -405537848), v = u(v, C = u(C, l = u(l, d, v, C, n[f + 9], 5, 568446438), d, v, n[f + 14], 9, -1019803690), l, d, n[f + 3], 14, -187363961), C, l, n[f + 8], 20, 1163531501), v = u(v, C = u(C, l = u(l, d, v, C, n[f + 13], 5, -1444681467), d, v, n[f + 2], 9, -51403784), l, d, n[f + 7], 14, 1735328473), C, l, n[f + 12], 20, -1926607734), v = e(v, C = e(C, l = e(l, d, v, C, n[f + 5], 4, -378558), d, v, n[f + 8], 11, -2022574463), l, d, n[f + 11], 16, 1839030562), C, l, n[f + 14], 23, -35309556), v = e(v, C = e(C, l = e(l, d, v, C, n[f + 1], 4, -1530992060), d, v, n[f + 4], 11, 1272893353), l, d, n[f + 7], 16, -155497632), C, l, n[f + 10], 23, -1094730640), v = e(v, C = e(C, l = e(l, d, v, C, n[f + 13], 4, 681279174), d, v, n[f], 11, -358537222), l, d, n[f + 3], 16, -722521979), C, l, n[f + 6], 23, 76029189), v = e(v, C = e(C, l = e(l, d, v, C, n[f + 9], 4, -640364487), d, v, n[f + 12], 11, -421815835), l, d, n[f + 15], 16, 530742520), C, l, n[f + 2], 23, -995338651), v = c(v, C = c(C, l = c(l, d, v, C, n[f], 6, -198630844), d, v, n[f + 7], 10, 1126891415), l, d, n[f + 14], 15, -1416354905), C, l, n[f + 5], 21, -57434055), v = c(v, C = c(C, l = c(l, d, v, C, n[f + 12], 6, 1700485571), d, v, n[f + 3], 10, -1894986606), l, d, n[f + 10], 15, -1051523), C, l, n[f + 1], 21, -2054922799), v = c(v, C = c(C, l = c(l, d, v, C, n[f + 8], 6, 1873313359), d, v, n[f + 15], 10, -30611744), l, d, n[f + 6], 15, -1560198380), C, l, n[f + 13], 21, 1309151649), v = c(v, C = c(C, l = c(l, d, v, C, n[f + 4], 6, -145523070), d, v, n[f + 11], 10, -1120210379), l, d, n[f + 2], 15, 718787259), C, l, n[f + 9], 21, -343485551), l = r(l, i), d = r(d, a), v = r(v, h), C = r(C, g);
        return [l, d, v, C]
    }

    function i(n) {
        var r, t = "", o = 32 * n.length;
        for (r = 0; r < o; r += 8) t += String.fromCharCode(n[r >> 5] >>> r % 32 & 255);
        return t
    }

    function a(n) {
        var r, t = [];
        for (t[(n.length >> 2) - 1] = void 0, r = 0; r < t.length; r += 1) t[r] = 0;
        var o = 8 * n.length;
        for (r = 0; r < o; r += 8) t[r >> 5] |= (255 & n.charCodeAt(r / 8)) << r % 32;
        return t
    }

    function h(n) {
        var r, t, o = "0123456789abcdef", u = "";
        for (t = 0; t < n.length; t += 1) r = n.charCodeAt(t), u += o.charAt(r >>> 4 & 15) + o.charAt(15 & r);
        return u
    }

    function g(n) {
        return unescape(encodeURIComponent(n))
    }

    function l(n) {
        return function (n) {
            return i(f(a(n), 8 * n.length))
        }(g(n))
    }

    function d(n, r) {
        return function (n, r) {
            var t, o, u = a(n), e = [], c = [];
            for (e[15] = c[15] = void 0, 16 < u.length && (u = f(u, 8 * n.length)), t = 0; t < 16; t += 1) e[t] = 909522486 ^ u[t], c[t] = 1549556828 ^ u[t];
            return o = f(e.concat(a(r)), 512 + 8 * r.length), i(f(c.concat(o), 640))
        }(g(n), g(r))
    }

    window.xxoo = function (n, r, t) {
        return r ? t ? d(r, n) : function (n, r) {
            return h(d(n, r))
        }(r, n) : t ? l(n) : function (n) {
            return h(l(n))
        }(n)
    }
}();

const CryptoJS = require("crypto-js");
let kkkk = CryptoJS.enc.Utf8.parse("xxxxxxxxoooooooo");
let iiii = CryptoJS.enc.Utf8.parse("0123456789ABCDEF");

function s() {
    window.ttt = new Date().getTime();
    window.token = window.xxoo("sssssbbbbb" + ttt)
    window.hhh = {
        s: window.token,
        tt: window.ttt,
    }

    return window.hhh;
}

function xxxxoooo(encryptedHex) {
    let enccc = CryptoJS.enc.Hex.parse(encryptedHex);
    let deccc = CryptoJS.AES["decr" + "ypt"]({ciphertext: enccc}, kkkk, {
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7,
        iv: iiii,
    });
    return deccc.toString(CryptoJS.enc.Utf8);
}

function loadPage(pageNumber) {
    s()
    const params = {
        page: pageNumber,
    };

    const queryString = new URLSearchParams(params).toString();
    fetch(`/api/problem-detail/${problemId}/data/?${queryString}`, {
        headers: hhh,
    })
        .then(response =>
            response.json()
        )
        .then(data =>
            updatePageContent(
                JSON.parse(xxxxoooo(data.t))
            ))
        .catch(error => console.error('Error fetching problem details:', error));
}