const CryptoJS = require("crypto-js");

function get_url_param() {
    var f = (new Date).getTime();

    var m = CryptoJS.HmacSHA1('9527' + f, 'xxxooo').toString();

    return {
        "tt": btoa(f),
        "m": m
    }
}