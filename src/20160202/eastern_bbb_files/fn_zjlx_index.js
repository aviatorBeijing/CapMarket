var tableCache = '<table cellpadding="0" cellspacing="0" class="t2 ns2"><thead><tr><th>\u4ee3\u7801</th><th>\u540d\u79f0</th><th>\u6700\u65b0\u4ef7</th><th>\u6da8\u8dcc\u989d</th><th>\u6da8\u8dcc\u5e45</th><th>\u632f\u5e45</th><th>\u6210\u4ea4\u91cf(\u624b)</th><th>\u6210\u4ea4\u989d(\u4e07)</th><th>\u6628\u6536</th><th>\u4eca\u5f00</th><th>\u6700\u9ad8</th><th>\u6700\u4f4e</th></tr></thead><tbody><tr><td><a href="http://quote.eastmoney.com/{code}.html" target="_blank">{codes}</a></td><td><a href="http://quote.eastmoney.com/{code}.html" target="_blank">{name}</a></td><td>{price}</td><td>{change}</td><td>{percent}</td><td><span>{zf}</span></td><td><span>{amount}</span></td><td><span>{volume}</span></td><td>{last}</td><td>{open}</td><td>{height}</td><td>{low}</td></tr></tbody></table>';
function ZjlxUpdate() {
    time_stamp = Math.floor((new Date().getTime()) / 60000);
    var b = data_baseurl + "js/" + _dpzs + ".js?rt=" + Math.random();
    tiny.loadJs(b, "utf-8", function () {
        if (!(typeof zjlx_detail == "undefined" || zjlx_detail == null)) {
            var data = zjlx_detail.data.split(",");
            $("updateTime_0").innerHTML = zjlx_detail.update;
            $("updateTime_1").innerHTML = zjlx_detail.update;
            $("data_jlr").innerHTML = data[0];
            $("data_jlr").className = (data[0] > 0) ? "red" : ((data[0] < 0) ? "green" : "");
            $("data_jzb").innerHTML = isNaN(data[1]) ? "0.00%" : data[1] + "%";
            $("data_jzb").className = (data[1] > 0) ? "red" : ((data[1] < 0) ? "green" : "");
            $("data_superjlr").innerHTML = data[2];
            $("data_superjlr").className = (data[2] > 0) ? "red" : ((data[2] < 0) ? "green" : "");
            $("data_superjzb").innerHTML = isNaN(data[3]) ? "0.00%" : data[3] + "%";
            $("data_superjzb").className = (data[3] > 0) ? "red" : ((data[3] < 0) ? "green" : "");
            $("data_ddjlr").innerHTML = data[4];
            $("data_ddjlr").className = (data[4] > 0) ? "red" : ((data[4] < 0) ? "green" : "");
            $("data_ddjzb").innerHTML = isNaN(data[5]) ? "0.00%" : data[5] + "%";
            $("data_ddjzb").className = (data[5] > 0) ? "red" : ((data[5] < 0) ? "green" : "");
            $("data_zdjlr").innerHTML = data[6];
            $("data_zdjlr").className = (data[6] > 0) ? "red" : ((data[6] < 0) ? "green" : "");
            $("data_zdjzb").innerHTML = isNaN(data[7]) ? "0.00%" : data[7] + "%";
            $("data_zdjzb").className = (data[7] > 0) ? "red" : ((data[7] < 0) ? "green" : "");
            $("data_xdjlr").innerHTML = data[8];
            $("data_xdjlr").className = (data[8] > 0) ? "red" : ((data[8] < 0) ? "green" : "");
            $("data_xdjzb").innerHTML = isNaN(data[9]) ? "0.00%" : data[9] + "%";
            $("data_xdjzb").className = (data[9] > 0) ? "red" : ((data[9] < 0) ? "green" : "");
            $("data_superlr").innerHTML = data[12];
            $("data_ddlr").innerHTML = data[14];
            $("data_zdlr").innerHTML = data[16];
            $("data_xdlr").innerHTML = data[18];
            $("data_superlc").innerHTML = data[13];
            $("data_ddlc").innerHTML = data[15];
            $("data_zdlc").innerHTML = data[17];
            $("data_xdlc").innerHTML = data[19] + "";
        }
    }, true)
}
function ZjlxInterval() {
    var e = new Date();
    try {
        e = Eastmoney.Time.now()
    }
    catch (i) {
    }
    var k = parseInt(tiny.dateFormat(e, "HHmm") * 1);
    var g = e.getDay();
    if (!(k <= 914 || (k >= 1145 && k <= 1259) || k >= 1515 || g > 5)) {
        try {
            ZjlxUpdate();
            var j = new Date().getTime();
            var h = new SWFObject(swf_line, "so10", "468", "225", "8", "");
            h.addVariable("path", "/");
            h.addVariable("settings_file", encodeURIComponent("../settings/dpzjlx_line_settings_csv.xml"));
            h.addVariable("data_file", encodeURIComponent(data_baseurl + "allXML/" + _dpzs + ".xml?rt=" + j));
            h.write("flash-cont");
            var f = new SWFObject(swf_pie, "so30", "468", "250", "8", "");
            f.addVariable("path", "/");
            f.addVariable("settings_file", encodeURIComponent("../settings/dpzjlx_pie.xml"));
            f.addVariable("data_file", encodeURIComponent(data_baseurl + "xml/" + _dpzs + ".xml?rt=" + j));
            f.write("flash-cont-1")
        }
        catch (i) {
        }
    }
}
function hqUpdate() {
    if (!$("shhq") || !$("szhq")) {
        zsUpdate();
        return;
    }
    var url = "http://hqdigi2.eastmoney.com/EM_Quote2010NumericApplication/cache.aspx?Type=c1&Reference=flm";
    var spanCache = '<b>{dqzs}</b>{zdqs}<b>{zdzs}</b>{zdqs}<b>{zdf}&nbsp;&nbsp;{cje}</b> ';
    var b = url + "&rt=" + Math.floor((new Date().getTime()) / 30000);
    var c, h, d, type;
    var e = function (g, a) {
        var f;
        if (isNaN(g) || isNaN(a)) {
            return "-"
        }
        if (parseFloat(g) > a) {
            f = "red"
        }
        else {
            if (parseFloat(g) < a) {
                f = "green"
            }
            else {
                f = "" + g + ""
            }
        }
        return f
    };
    tiny.loadJs(b, "utf-8", function () {
        if (!(typeof C1Cache == "undefined" || C1Cache == null)) {
            c = C1Cache.quotation[0].split(",");
            if (c.length < 8) {
                c = ["-", "-", "-", "-", "-", "-", "-"]
            }
            type = e(c[5], 0);
            d = spanCache.replace(/{dqzs}/ig, c[2]);
            d = d.replace(/{zdqs}/ig, type == "green" ? " <span class=\"arr\">¡ý</span>" : " <span class=\"arr\">¡ü</span>");
            d = d.replace(/{zdzs}/ig, c[5]);
            d = d.replace(/{zdf}/ig, c[6]);
            d = d.replace(/{cje}/ig, !isNaN(c[3]) ? (parseFloat(c[3]) / 10000).toFixed(2) : c[3]);
            $("shhq").className = type;
            $("shhq").innerHTML = d;
            $("shz").innerHTML = C1Cache.record[0].split(",")[0];
            $("shp").innerHTML = C1Cache.record[0].split(",")[1];
            $("shd").innerHTML = C1Cache.record[0].split(",")[2];

            c = C1Cache.quotation[1].split(",");
            if (c.length < 8) {
                c = ["-", "-", "-", "-", "-", "-", "-"]
            }
            type = e(c[5], 0);
            d = spanCache.replace(/{dqzs}/ig, c[2]);
            d = d.replace(/{zdqs}/ig, type == "green" ? " <span class=\"arr\">¡ý</span>" : " <span class=\"arr\">¡ü</span>");
            d = d.replace(/{zdzs}/ig, c[5]);
            d = d.replace(/{zdf}/ig, c[6]);
            d = d.replace(/{cje}/ig, !isNaN(c[3]) ? (parseFloat(c[3]) / 10000).toFixed(2) : c[3]);
            $("szhq").className = type;
            $("szhq").innerHTML = d;
            $("szz").innerHTML = C1Cache.record[1].split(",")[0];
            $("szp").innerHTML = C1Cache.record[1].split(",")[1];
            $("szd").innerHTML = C1Cache.record[1].split(",")[2];
        }
    }, true)
}

function zsUpdate() {
    var url = "http://hqdigi2.eastmoney.com/EM_Quote2010NumericApplication/Index.aspx?Type=F&jsName=zjlx_hq&id=" + _dpzs.replace("zs", "") + (_dpzs.substr(0, 5) == "zs399" ? "2" : "1");
    var b = url + "&rt=" + Math.floor((new Date().getTime()) / 30000); var c, d;
    var e = function (f, g, a) { if (isNaN(g) || isNaN(a)) { return "<span>" + f + "</span>" } if (parseFloat(g) > a) { f = '<span class="red">' + f + "</span>" } else { if (parseFloat(g) < a) { f = '<span class="green">' + f + "</span>" } else { f = "<span>" + f + "</span>" } } return f };
    tiny.loadJs(b, "utf-8", function () {
        if (!(typeof zjlx_hq == "undefined" || zjlx_hq == null)) {
            c = zjlx_hq.quotation[0].split(",");
            if (c.length < 24) { c = [_stockCode, _stockCode, _stockName, "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", ] }
            d = tableCache.replace(/{code}/ig, _dpzs);
            d = d.replace(/{codes}/ig, _dpzs.replace("zs","")); d = d.replace(/{name}/ig, c[2]); d = d.replace(/{price}/ig, e(c[5], c[10], 0)); d = d.replace(/{change}/ig, e(c[10], c[10], 0)); d = d.replace(/{percent}/ig, e(c[11], c[10], 0)); d = d.replace(/{zf}/ig, c[13]); d = d.replace(/{amount}/ig, c[9]); d = d.replace(/{volume}/ig, c[8]); d = d.replace(/{last}/ig, e(c[3])); d = d.replace(/{open}/ig, e(c[4], c[4], c[3])); d = d.replace(/{height}/ig, e(c[6], c[6], c[3])); d = d.replace(/{low}/ig, e(c[7], c[7], c[3])); d = d.replace(/{hsl}/ig, c[23]); d = d.replace(/{lb}/ig, c[22]); d = d.replace(/{syl}/ig, (c[24] < 0 ? "--" : c[24]));
            $("zjlx_zshqcont").innerHTML = d;
        }
    }, true);
}
function hqInterval() {
    var e = new Date();
    try {
        e = Eastmoney.Time.now()
    }
    catch (g) {
    }
    var h = parseInt(tiny.dateFormat(e, "HHmm") * 1);
    var f = e.getDay();
    if (!(h <= 914 || (h >= 1145 && h <= 1259) || h >= 1515 || f > 5)) {
        try {
            hqUpdate();
        }
        catch (g) {
        }
    }
}