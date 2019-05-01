let customerChat = function () {
    let d = document, w = window, l = window.location, p = l.protocol == "file:" ? "http://" : "//";
    if (!w.WS) w.WS = {};
    c = w.WS;
    let m = function (t, o) {
        let e = d.getElementsByTagName("script");
        e = e[e.length - 1];
        let n = d.createElement(t);
        if (t == "script") {
            n.async = true;
        }
        for (k in o) n[k] = o[k];
        e.parentNode.insertBefore(n, e)
    };
    m("script", {
        src: p + "bawkbox.com/widget/customer-chat/5cc1a3ba53918a001063b6cb?page=" + encodeURIComponent(l + ''),
        type: 'text/javascript'
    });
    c.load_net = m;
};
if (window.Squarespace) {
    document.addEventListener('DOMContentLoaded', customerChat);
} else {
    customerChat()
}