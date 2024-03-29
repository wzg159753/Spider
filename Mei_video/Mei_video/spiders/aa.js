function decode(a) {
    var b = getHex(a);
    var c = getDex(b.hex);
    var d = substr(b.str, c.pre);
    return atob(substr(d, getPos(d, c.tail)))
}
// return g.atob(this[k](d, this.getPos(d, c.tail)))

function getHex(a) {
    return{
        str:a.substring(4),
        hex:a.substring(0, 4).split("").reverse().join("")
    }
}

function getDex(a) {
    var b = parseInt(a, 16).toString();
    return {
        pre:b.substring(0, 2).split(""),
        tail:b.substring(2).split("")
    }

}

function substr(a, b) {
    var c = a.substring(0, b[0])
        ,d = a.substr(b[0], b[1]);
    return c + a.substring(b[0]).replace(d, "")
}

function getPos(a, b) {
    return b[0] = a.length - b[0] - b[1],
    b
}

var f = function() {
        try {
            document.createElement("$")
        } catch (a) {
            return a
        }
    }();
var e = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";

function atob(a) {
        if (a = a.replace(/=+$/, ""),
        a.length % 4 == 1)
            throw f;
        for (var b, c, d = 0, g = 0, h = ""; c = a.charAt(g++); ~c && (b = d % 4 ? 64 * b + c : c,
        d++ % 4) ? h += String.fromCharCode(255 & b >> (-2 * d & 6)) : 0)
            c = e.indexOf(c);
        return h
    }