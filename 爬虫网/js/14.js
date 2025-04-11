function x(b = '/api/problem-detail/14/data/') {
    ts = (new Date()).getTime()
    dd = b
    N = 'dasdasdarqwdasdasqwdasda' + ts
    p = n(N)
    s = '?m='
    p = p.toString(16)
    return d(p + ts)
}

function d(N) {
    var W = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
    let O = '', L, y, k, H, D, K, S, I = 0;
    for (; z['\x42\x6f\x68\x51\x71'](I, N.length);)
        L = N.charCodeAt(I++),
        y = z['\x5a\x6d\x62\x4f\x61'](I, N.length) ? N.charCodeAt(I++) : 0,
        k = I < N.length ? N.charCodeAt(I++) : 0,
        H = L >> 2,
        D = (3 & L) << 4 | z['\x78\x42\x55\x50\x41'](y, 4),
        K = z['\x73\x69\x64\x59\x79'](z['\x66\x59\x61\x6c\x4d'](15 & y, 2), z['\x58\x6d\x7a\x52\x73'](k, 6)),
        S = 63 & k,
        isNaN(y) ? K = S = 64 : z['\x64\x55\x6c\x74\x4b'](isNaN, k) && (S = 64),
        O = z['\x66\x44\x61\x77\x78'](O, W['\x63\x68\x61\x72\x41\x74'](H)) + W.charAt(D) + W.charAt(K) + W.charAt(S);
    return O;
}

function n(N) {
    let W = 0;
    for (let L = 0; L < N.length; L++) {
        var O = N.charCodeAt(L)
        for (let y = 0; y < 20; y++)
            switch (y % 3) {
                case 0:
                    W = B.apply(null, [W, O, y])
                    break
                case 1:
                    W = J.apply(null, [W, O, y]);
                    break
                case 2:
                    W = Y.apply(null, [W, O]);
            }
    }
    return W;
}

z = {
    '\x47\x79\x67\x58\x59': '\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x2b\x2f',
    '\x6b\x57\x48\x52\x56': function (e, b) {
        return e >> b;
    },
    '\x42\x77\x4e\x63\x4b': function (e, b) {
        return e & b;
    },
    '\x7a\x4e\x75\x58\x4f': function (e, b) {
        return e << b;
    },
    '\x66\x44\x61\x77\x78': function (e, b) {
        return e + b;
    },
    '\x57\x48\x69\x61\x43': function (e, b) {
        return e !== b;
    },
    // '\x67\x49\x57\x51\x5a': X(0x18b),
    // '\x4a\x59\x42\x73\x69': X(__sk_GI.G),
    // '\x6d\x78\x4a\x76\x4d': X(0x189),
    // '\x45\x67\x54\x6c\x42': '\x43\x47\x57\x4d\x54',
    // '\x49\x57\x43\x68\x66': X(0x196),
    '\x45\x70\x71\x77\x4b': function (e, b) {
        return e ^ b;
    },
    '\x42\x6f\x68\x51\x71': function (e, b) {
        return e < b;
    },
    '\x5a\x6d\x62\x4f\x61': function (e, b) {
        return e < b;
    },
    '\x78\x42\x55\x50\x41': function (e, b) {
        return e >> b;
    },
    '\x73\x69\x64\x59\x79': function (e, b) {
        return e | b;
    },
    '\x66\x59\x61\x6c\x4d': function (e, b) {
        return e << b;
    },
    '\x58\x6d\x7a\x52\x73': function (e, b) {
        return e >> b;
    },
    '\x64\x55\x6c\x74\x4b': function (e, b) {
        return e(b);
    },
    '\x74\x48\x57\x55\x51': function (e, b) {
        return e < b;
    },
    '\x47\x51\x4c\x63\x65': function (e, b) {
        return e % b;
    },
    '\x71\x6c\x57\x50\x49': function (e, b) {
        return e === b;
    },
    '\x79\x45\x7a\x65\x4c': '\x64\x61\x73\x64\x61\x73\x64\x61\x72\x71\x77\x64\x61\x73\x64\x61\x73\x71\x77\x64\x61\x73\x64\x61',
    '\x73\x54\x68\x4d\x4d': function (e, b) {
        return e(b);
    },
    '\x49\x5a\x43\x64\x42': function (e, b, f) {
        return e(b, f);
    }
}

function B(b, f, p) {
    return b ^ z['\x7a\x4e\x75\x58\x4f'](f, p % 8);
}

function J(b, f, p) {
    return z['\x49\x57\x43\x68\x66'] === z['\x49\x57\x43\x68\x66'] ? z['\x45\x70\x71\x77\x4b'](b, f >> p % 8) : Q ^ z['\x7a\x4e\x75\x58\x4f'](v, d % 8);
}

function Y(b, f) {
    return (b = b + f - f) ^ f;
}

console.log(x())