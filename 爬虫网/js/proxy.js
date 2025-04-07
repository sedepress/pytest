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
                        console.log('方法：', 'get', '对象：', `${key}`, '属性：', p, '属性类型：', `${typeof p}`, '属性值：', propValue, '属性值类型：', `${typeof propValue}`);
                        return propValue;
                    },
                    set(target, p, n, receiver) {
                        console.log('方法：', 'set', '对象：', `${key}`, '属性：', p, '属性类型：', `${typeof p}`, '属性值：', n, '属性值类型：', `${typeof n}`);
                        return Reflect.set(target, p, n, receiver);
                    },
                })
            }
        })
    }
}