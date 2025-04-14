window = global

window._$ = {
    'ajax': function () {
        console.log(arguments)
    },
    'apply': function () {
        console.log(arguments)
    },
    'extend': function () {
        window.url = arguments[2].url
        console.log(arguments)
    },
    'ajaxPrefilter': function () {
        console.log(arguments)
    }
}

function CanvasRenderingContext2D() {
    this.direction = "ltr";
    this.fillStyle = "#000000";
    this.filter = "none";
    this.font = "10px sans-serif";
    this.fontKerning = "auto";
    this.fontStretch = "normal";
    this.fontVariantCaps = "normal";
    this.lobalAlpha = 1;
    this.globalCompositeOperation = "source-over";
    this.imageSmoothingEnabled = true;
    this.imageSmoothingQuality = "low";
    this.letterSpacing = "0px";
    this.lineCap = "butt";
    this.lineDashOffset = 0;
    this.lineJoin = "miter";
    this.lineWidth = 1;
    this.miterLimit = 10;
    this.shadowBlur = 0;
    this.shadowColor = "rgba(0; 0; 0; 0)";
    this.shadowOffsetX = 0;
    this.shadowOffsetY = 0;
    this.strokeStyle = "#000000";
    this.textAlign = "start";
    this.textBaseline = "alphabetic";
    this.textRendering = "auto";
    this.wordSpacing = "0px"
    this.style = {}
    this.fillRect = function () {
        console.log(arguments)
    }
    this.fillText = function () {
        console.log(arguments)
    }
}

canvas2D = new CanvasRenderingContext2D();

screen = {
    availWidth: 1920,
    availHeight: 1055,
}

div = {
    setAttribute: function (ele) {
        console.log('div::setAttribute:', ele)
    }
}

head = {

}

const canvas = {
    getContext: function (ele) {
        if (ele === '2d') {
            return canvas2D;
        }
        console.log('canvas::getContext:', arguments)
    },
    textBaseline: 'alphabetic',
    toDataURL: function () {
        console.log(arguments)
    },
    width: 200,
    height: 200
}

function Plugin() {}
navigator = {
    plugins: [
        new Plugin(),
        new Plugin(),
        new Plugin(),
        new Plugin(),
        new Plugin(),
    ],
    appCodeName: "Mozilla",
    appName: "Netscape",
    appVersion: "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    languages: ['zh-CN', 'zh'],
    webdriver: false,
    platform:"Win32",
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
}

chrome = {}

function History() {}
window.History = History
history = {
    length: 7,
    scrollRestoration: 'auto',
    state: null,
    back() {

    }
}
history.__proto__ = History.prototype

document = {
    createElement: function (ele) {
        console.log('document::createElement:', arguments)
        if (ele === 'canvas') {
            return canvas;
        }

        if (ele === 'div') {
            return div;
        }
    },
    getElementsByTagName: function (ele) {
        console.log('document::getElementsByTagName:', ele)
    },
    head: {},
    attachEvent: function () {
        console.log('document::attachEvent:', arguments)
    },
    addEventListener(type, listener, options) {
        console.log(type, listener, options)
    },
    documentElement: {},
    getElementById: function () {
        console.log('document::getElementById:', arguments)
    },
    cookie: 'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1742952358; HMACCOUNT=F8D55D100B06DC65; s=51b351b351b351b370b0d030d030507090d0f030f0; v=QTJ4b3BBdk1KN3lsLVRQN3UtNXhSbEhrTzBHYkpSTDhFc3NrazhhdGVRMjY5Z0pfN2pYZ1gyTFo5Q0FWMTc0NDM1ODc3MTkzOA==; _nano_fp=XpmYn0EoX5PxX5dxno_SEWXzUnt~HLUABpTu5fic; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1744615136',
    referrer: '',
    visibilityState: 'visible'
}

function Location() {}
window.Location = Location
location = {
    href: 'https://stu.tulingpyton.cn/problem-detail/18/',
    port: '',

}
location.__proto__ = Location.prototype

function Storage(){}
window.Storage = Storage
localStorage = {
    'getItem': function (ele) {
        console.log('localStorage::getItem:', arguments)
        if (ele === 'WQ_dy1_vk') {
            return '{"5.0":{"b5216":{"e":31536000,"v":"wwrpxwcw3ad9sra1","t":1744484802301}}}'
        }

        if (ele === 'WQ_dy1_tk_algo') {
            return '{"wwrpxwcw3ad9sra1":{"b5216":{"v":"eyJ0ayI6InRrMDN3Yjg4MDFjNDAxOG5qdGRpNnAwY0VIU3V2VWtRcnZtQi1zbnY3NzAtYVdMVVV6UDR2U2FfUlJFRk1mMTFVUGctZ2xUZDJZYVBzQUR6WVpiaG12MzJZSmVRIiwiYWxnbyI6ImZ1bmN0aW9uIHRlc3QodGssZnAsdHMsYWksYWxnbyl7dmFyIHJkPSdsMUluZ3QxR1hvRjEnO3ZhciBzdHI9XCJcIi5jb25jYXQodGspLmNvbmNhdChmcCkuY29uY2F0KHRzKS5jb25jYXQoYWkpLmNvbmNhdChyZCk7cmV0dXJuIGFsZ28uTUQ1KHN0cik7fSJ9","e":86400,"t":1744484802663}}}'
        }

        if (ele === 'WQ_gather_cv1') {
            return '{"v":"6902da3cc3d2c9012ca66b9516e55d6d","t":1744484802375,"e":31536000}'
        }

        if (ele === 'WQ_gather_wgl1') {
            return '{"v":"955d8474cd4b30c3b1ffd5a5492bcbbe","t":1744484802387,"e":31536000}'
        }

        if (ele === 'hexin-v') {
            return 'QTJ4b3BBdk1KN3lsLVRQN3UtNXhSbEhrTzBHYkpSTDhFc3NrazhhdGVRMjY5Z0pfN2pYZ1gyTFo5Q0FWMTc0NDM1ODc3MTkzOA=='
        }

        if (ele === 'isWhitelist') {
            return 'false'
        }

        if (ele === '_nano_fp') {
            return 'XpmYn0EoX5PxX5dxno_SEWXzUnt~HLUABpTu5fic'
        }
    },
    'setItem': function () {
        console.log('localStorage::setItem:', arguments)
    }
}
localStorage.__proto__ = Storage.prototype

window['$'] = window._$
window.outerHeight = 1055
window.outerWidth = 1920
window.DeviceOrientationEvent = function () {}
window.DeviceMotionEvent = function () {}

function HTMLElement() {}
window.HTMLElement = HTMLElement


delete Buffer

console.log_ = console.log

delete global

function ProxyDocumentObjects(proxyObjs) {
    for (let i = 0; i < proxyObjs.length; i++) {
        const documentObj = proxyObjs[i];
        const keys = Object.keys(documentObj)
        keys.forEach(key => {
            const value = documentObj[key];
            if (value && typeof value === 'object') {
                documentObj[key] = new Proxy(value, {
                    get(target, p, receiver) {
                        const propValue = Reflect.get(target, p, receiver);
                        console.log_('方法：', 'get', '对象：', `${key}`, '属性：', p, '属性类型：', `${typeof p}`, '属性值：', propValue, '属性值类型：', `${typeof propValue}`);
                        return propValue;
                    },
                    set(target, p, n, receiver) {
                        console.log_('方法：', 'set', '对象：', `${key}`, '属性：', p, '属性类型：', `${typeof p}`, '属性值：', n, '属性值类型：', `${typeof n}`);
                        return Reflect.set(target, p, n, receiver);
                    },
                })
            }
        })
    }
}

Element = {}
Element.prototype = function () {

}

const proxyObjs = [window, Element]

ProxyDocumentObjects(proxyObjs)

require('/Users/zs/PycharmProjects/pytest/爬虫网/js/actoken.js')

function _0x1983(_0x1de941, _0x2f274e) {
    const _0x7b18c6 = _0x5959();
    return _0x1983 = function(_0x103b7c, _0x3767e2) {
        _0x103b7c = _0x103b7c - 0x1e1;
        let _0x5dacff = _0x7b18c6[_0x103b7c];
        return _0x5dacff;
    }
    ,
    _0x1983(_0x1de941, _0x2f274e);
}
(function(_0xfb990e, _0x58f059) {
    const _0x4bc778 = _0x1983
      , _0x5e70a5 = _0xfb990e();
    while (!![]) {
        try {
            const _0x558e1e = -parseInt(_0x4bc778(0x1fd)) / 0x1 + parseInt(_0x4bc778(0x203)) / 0x2 + parseInt(_0x4bc778(0x206)) / 0x3 * (parseInt(_0x4bc778(0x1e1)) / 0x4) + -parseInt(_0x4bc778(0x1ed)) / 0x5 * (-parseInt(_0x4bc778(0x205)) / 0x6) + -parseInt(_0x4bc778(0x200)) / 0x7 + -parseInt(_0x4bc778(0x1ef)) / 0x8 + -parseInt(_0x4bc778(0x1f0)) / 0x9;
            if (_0x558e1e === _0x58f059)
                break;
            else
                _0x5e70a5['push'](_0x5e70a5['shift']());
        } catch (_0x454bb2) {
            _0x5e70a5['push'](_0x5e70a5['shift']());
        }
    }
}(_0x5959, 0x91840));
const _0x5408bf = (function() {
    let _0x5a6697 = !![];
    return function(_0x4020fb, _0x9db4e7) {
        const _0x5ad05b = _0x5a6697 ? function(){const _0x49e327=_0x1983;if(_0x9db4e7){const _0x5c6dd8=_0x9db4e7[_0x49e327(0x1ee)](_0x4020fb,arguments);return _0x9db4e7=null,_0x5c6dd8}}
        : function() {}
        ;
        return _0x5a6697 = ![],
        _0x5ad05b;
    }
    ;
}())
  , _0x3f4f5e = _0x5408bf(this, function() {
    const _0x5b3de1 = _0x1983;
    return _0x3f4f5e[_0x5b3de1(0x1f6)]()[_0x5b3de1(0x1f9)]('(((.+)+)+)+$')[_0x5b3de1(0x1f6)]()[_0x5b3de1(0x1fb)](_0x3f4f5e)[_0x5b3de1(0x1f9)](_0x5b3de1(0x1e7));
});
_0x3f4f5e();
const _0x3767e2 = (function() {
    let _0x25c379 = !![];
    return function(_0xfaeb92, _0x107892) {
        const _0x3842a8 = _0x25c379 ? function(){const _0x17e84c=_0x1983;if(_0x107892){const _0x4d8237=_0x107892[_0x17e84c(0x1ee)](_0xfaeb92,arguments);return _0x107892=null,_0x4d8237}}
        : function() {}
        ;
        return _0x25c379 = ![],
        _0x3842a8;
    }
    ;
}())
  , _0x103b7c = _0x3767e2(this, function() {
    const _0x9fd465 = _0x1983
      , _0x1e3f1d = function() {
        const _0x3d8502 = _0x1983;
        let _0x4509d3;
        try {
            _0x4509d3 = Function(_0x3d8502(0x1e5) + _0x3d8502(0x202) + ');')();
        } catch (_0xa9f013) {
            _0x4509d3 = window;
        }
        return _0x4509d3;
    }
      , _0x573a24 = _0x1e3f1d()
      , _0x2e51e5 = _0x573a24[_0x9fd465(0x1fe)] = _0x573a24[_0x9fd465(0x1fe)] || {}
      , _0x2a39da = ['log', _0x9fd465(0x1ec), 'info', 'error', _0x9fd465(0x1f3), _0x9fd465(0x1f5), _0x9fd465(0x1f1)];
    for (let _0x10c5bc = 0x0; _0x10c5bc < _0x2a39da[_0x9fd465(0x20b)]; _0x10c5bc++) {
        const _0x1211c3 = _0x3767e2['constructor'][_0x9fd465(0x1eb)][_0x9fd465(0x1e2)](_0x3767e2)
          , _0x124058 = _0x2a39da[_0x10c5bc]
          , _0x1c4c94 = _0x2e51e5[_0x124058] || _0x1211c3;
        _0x1211c3[_0x9fd465(0x1fc)] = _0x3767e2[_0x9fd465(0x1e2)](_0x3767e2),
        _0x1211c3[_0x9fd465(0x1f6)] = _0x1c4c94[_0x9fd465(0x1f6)]['bind'](_0x1c4c94),
        _0x2e51e5[_0x124058] = _0x1211c3;
    }
});
_0x103b7c();
const VM_OPS = {
    0x1: function(_0x36a893) {
        const _0xe99518 = _0x1983;
        return new Date()[_0xe99518(0x1e8)]();
    },
    0x2: function(_0x4deae8) {
        return getCrawlerInfo(_0x4deae8['ts']);
    },
    0x3: function(_0x1c307f) {
        const _0x1ec3f3 = _0x1983;
        return btoa(_0x1c307f[_0x1ec3f3(0x20a)]);
    },
    0x4: function(_0xafc5c1) {
        const _0x21e569 = _0x1983;
        return new URLSearchParams(_0xafc5c1[_0x21e569(0x208)])['toString']();
    },
    0x5: function(_0x4d7705) {
        const _0x12adfa = _0x1983;
        return console['error']['apply'](null, _0x4d7705[_0x12adfa(0x1ff)]);
    }
};
function _0x5959() {
    const _0x156059 = ['params', 'headers', 'input', 'length', '16AEfXGp', 'bind', '/api/problem-detail/', 'json', 'return\x20(function()\x20', 'ajax', '(((.+)+)+)+$', 'getTime', '/data/?', 'messagePack', 'prototype', 'warn', '5171800VRDLYQ', 'apply', '1803200grDZTF', '33183udGVeL', 'trace', 'config', 'exception', 'client-version', 'table', 'toString', 'Error\x20fetching\x20problem\x20details:', 'luoge', 'search', '获取请求参数失败:', 'constructor', '__proto__', '824158cpXewj', 'console', 'args', '3969147byHlBn', 'query', '{}.constructor(\x22return\x20this\x22)(\x20)', '545084lgEUij', '1.0.0', '6jJeLFt', '682047XdVZwu', 'timestamp'];
    _0x5959 = function() {
        return _0x156059;
    }
    ;
    return _0x5959();
}
function vmExecute(_0x4d87c8, _0x32370b) {
    const _0x1bedc8 = _0x1983;
    return VM_OPS[_0x4d87c8][_0x1bedc8(0x1ee)](null, [_0x32370b]);
}
$['ajaxPrefilter'](function(_0x5e86b1, _0x4a363f, _0x259d98) {
    const _0x1f4414 = _0x1983;
    let _0x44e2c2 = 0x0
      , _0x2ef45b = {
        'headers': _0x5e86b1['headers'] || {},
        'ts': 0x0,
        'crawler': ''
    };
    const _0xd39935 = [ () => {
        _0x2ef45b['ts'] = vmExecute(0x1, _0x2ef45b),
        _0x44e2c2 = 0x1;
    }
    , () => {
        _0x2ef45b['crawler'] = vmExecute(0x2, _0x2ef45b),
        _0x44e2c2 = 0x2;
    }
    , () => {
        const _0x38ae12 = _0x1983;
        _0x2ef45b[_0x38ae12(0x209)]['m'] = _0x2ef45b['crawler'] + vmExecute(0x3, {
            'input': _0x38ae12(0x1f8) + _0x2ef45b['ts']
        }),
        _0x2ef45b[_0x38ae12(0x209)][_0x38ae12(0x207)] = _0x2ef45b['ts'],
        _0x2ef45b[_0x38ae12(0x209)][_0x38ae12(0x1f4)] = _0x38ae12(0x204),
        _0x5e86b1[_0x38ae12(0x209)] = _0x2ef45b[_0x38ae12(0x209)],
        _0x44e2c2 = 0x3;
    }
    ];
    try {
        while (_0x44e2c2 < _0xd39935[_0x1f4414(0x20b)]) {
            _0xd39935[_0x44e2c2]();
        }
    } catch (_0x36b474) {
        vmExecute(0x5, {
            'args': [_0x1f4414(0x1fa), _0x36b474]
        });
    }
});

function aaa(_0x5e86b1, _0x4a363f, _0x259d98) {
    const _0x1f4414 = _0x1983;
    let _0x44e2c2 = 0x0
      , _0x2ef45b = {
        'headers': _0x5e86b1['headers'] || {},
        'ts': 0x0,
        'crawler': ''
    };
    const _0xd39935 = [ () => {
        _0x2ef45b['ts'] = vmExecute(0x1, _0x2ef45b),
        _0x44e2c2 = 0x1;
    }
    , () => {
        _0x2ef45b['crawler'] = vmExecute(0x2, _0x2ef45b),
        _0x44e2c2 = 0x2;
    }
    , () => {
        const _0x38ae12 = _0x1983;
        _0x2ef45b[_0x38ae12(0x209)]['m'] = _0x2ef45b['crawler'] + vmExecute(0x3, {
            'input': _0x38ae12(0x1f8) + _0x2ef45b['ts']
        }),
        _0x2ef45b[_0x38ae12(0x209)][_0x38ae12(0x207)] = _0x2ef45b['ts'],
        _0x2ef45b[_0x38ae12(0x209)][_0x38ae12(0x1f4)] = _0x38ae12(0x204),
        _0x5e86b1[_0x38ae12(0x209)] = _0x2ef45b[_0x38ae12(0x209)],
        _0x44e2c2 = 0x3;
    }
    ];
    try {
        while (_0x44e2c2 < _0xd39935[_0x1f4414(0x20b)]) {
            _0xd39935[_0x44e2c2]();
        }
    } catch (_0x36b474) {
        vmExecute(0x5, {
            'args': [_0x1f4414(0x1fa), _0x36b474]
        });
    }

    return _0x2ef45b
}

function getCrawlerInfo(_0x2926eb) {
    return B(_0x2926eb);
}
var B = function(_0x3f0d72) {
    const _0x8b3db1 = _0x1983;
    return anti(0x4)({
        'serverTime': _0x3f0d72
    })[_0x8b3db1(0x1ea)]();
};
function loadPage(_0x2676ad) {
    const _0x1c6593 = _0x1983;
    let _0x5e4569 = 0x0
      , _0x2e406f = {
        'params': {
            'page': _0x2676ad
        },
        'query': '',
        'config': {}
    };
    const _0x522c3d = [ () => {
        const _0x29f78a = _0x1983;
        _0x2e406f[_0x29f78a(0x201)] = vmExecute(0x4, _0x2e406f),
        _0x5e4569 = 0x1;
    }
    , () => {
        const _0x30cb66 = _0x1983;
        _0x2e406f[_0x30cb66(0x1f2)] = {
            'url': _0x30cb66(0x1e3) + _0x2676ad + _0x30cb66(0x1e9) + _0x2e406f[_0x30cb66(0x201)],
            'method': 'GET',
            'async': !![],
            'dataType': _0x30cb66(0x1e4),
            'beforeSend': function(_0x13dd33) {},
            'success': function(_0x2626c5) {
                updatePageContent(_0x2626c5);
            },
            'error': function(_0x301aec, _0x3b1b41, _0x1dd192) {
                const _0x224d28 = _0x30cb66;
                vmExecute(0x5, {
                    'args': [_0x224d28(0x1f7), _0x3b1b41, _0x1dd192]
                });
            }
        },
        _0x5e4569 = 0x2;
    }
    , () => {
        const _0xbcea5a = _0x1983;
        $[_0xbcea5a(0x1e6)](_0x2e406f['config']),
        _0x5e4569 = 0x3;
    }
    ];
    while (_0x5e4569 < _0x522c3d[_0x1c6593(0x20b)]) {
        _0x522c3d[_0x5e4569]();
    }
}

// console.log_(loadPage(1))
console.log_(aaa({}, {}, {}))