# -*- coding: utf-8 -*-
"""
AKShare API - Vercel Serverless 入口
提供 A股行情、基金净值、宏观数据等金融数据接口
"""

import json
from flask import Flask, request, Response
import akshare as ak

app = Flask(__name__)

# 统一 JSON 响应函数：ensure_ascii=False 确保中文不被转义
def json_response(data, status=200):
    return Response(
        json.dumps(data, ensure_ascii=False, default=str),
        status=status,
        mimetype="application/json; charset=utf-8"
    )


HTML_PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AKShare API - 金融数据接口服务</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background: #0f1923;
    color: #e0e0e0;
    min-height: 100vh;
  }
  .header {
    background: linear-gradient(135deg, #1a2a3a 0%, #0d1117 100%);
    padding: 40px 20px;
    text-align: center;
    border-bottom: 1px solid #1e2d3d;
  }
  .header h1 {
    font-size: 2.4em;
    color: #58a6ff;
    margin-bottom: 8px;
  }
  .header .subtitle {
    color: #8b949e;
    font-size: 1.1em;
  }
  .header .badge {
    display: inline-block;
    background: #1f6feb;
    color: #fff;
    padding: 3px 12px;
    border-radius: 12px;
    font-size: 0.8em;
    margin-top: 10px;
  }
  .container {
    max-width: 960px;
    margin: 0 auto;
    padding: 30px 20px;
  }
  .section-title {
    font-size: 1.3em;
    color: #58a6ff;
    margin: 30px 0 15px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #1e2d3d;
  }
  .api-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 16px;
    transition: border-color 0.2s;
  }
  .api-card:hover { border-color: #388bfd; }
  .api-method {
    display: inline-block;
    background: #1f6feb;
    color: #fff;
    padding: 2px 10px;
    border-radius: 4px;
    font-size: 0.85em;
    font-weight: 600;
    margin-right: 8px;
  }
  .api-path {
    font-family: 'SF Mono', Consolas, monospace;
    color: #e6edf3;
    font-size: 1.05em;
  }
  .api-desc {
    color: #8b949e;
    margin: 8px 0 12px 0;
    font-size: 0.95em;
  }
  .api-params {
    font-family: 'SF Mono', Consolas, monospace;
    font-size: 0.85em;
    color: #f0883e;
  }
  .test-btn {
    background: #238636;
    color: #fff;
    border: none;
    padding: 6px 16px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.85em;
    margin-top: 10px;
    transition: background 0.2s;
  }
  .test-btn:hover { background: #2ea043; }
  .result-box {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 6px;
    padding: 14px;
    margin-top: 10px;
    max-height: 400px;
    overflow: auto;
    display: none;
    font-family: 'SF Mono', Consolas, monospace;
    font-size: 0.82em;
    white-space: pre-wrap;
    word-break: break-all;
  }
  .result-box.show { display: block; }
  .footer {
    text-align: center;
    padding: 30px 20px;
    color: #484f58;
    font-size: 0.85em;
  }
  .footer a { color: #58a6ff; text-decoration: none; }
</style>
</head>
<body>

<div class="header">
  <h1>AKShare API</h1>
  <p class="subtitle">基于 AKShare 的金融数据接口服务</p>
  <span class="badge">v__VERSION__</span>
</div>

<div class="container">

  <div class="section-title">接口列表</div>

  <div class="api-card">
    <span class="api-method">GET</span>
    <span class="api-path">/api/stock/hist</span>
    <p class="api-desc">A股个股历史行情数据（日K/周K/月K）</p>
    <p class="api-params">参数: symbol(股票代码) period(daily/weekly/monthly) start_date end_date adjust(qfq前复权/hfq后复权/空)</p>
    <button class="test-btn" onclick="testAPI('stock/hist')">在线测试</button>
    <div class="result-box" id="result-stock-hist"></div>
  </div>

  <div class="api-card">
    <span class="api-method">GET</span>
    <span class="api-path">/api/stock/spot</span>
    <p class="api-desc">A股实时行情快照</p>
    <p class="api-params">参数: limit(返回条数，默认20)</p>
    <button class="test-btn" onclick="testAPI('stock/spot')">在线测试</button>
    <div class="result-box" id="result-stock-spot"></div>
  </div>

  <div class="api-card">
    <span class="api-method">GET</span>
    <span class="api-path">/api/fund/nav</span>
    <p class="api-desc">基金单位净值历史数据</p>
    <p class="api-params">参数: symbol(基金代码) limit(返回条数)</p>
    <button class="test-btn" onclick="testAPI('fund/nav')">在线测试</button>
    <div class="result-box" id="result-fund-nav"></div>
  </div>

  <div class="api-card">
    <span class="api-method">GET</span>
    <span class="api-path">/api/macro/cpi</span>
    <p class="api-desc">中国CPI月度宏观经济数据</p>
    <p class="api-params">参数: limit(返回条数)</p>
    <button class="test-btn" onclick="testAPI('macro/cpi')">在线测试</button>
    <div class="result-box" id="result-macro-cpi"></div>
  </div>

  <div class="api-card">
    <span class="api-method">GET</span>
    <span class="api-path">/api/search</span>
    <p class="api-desc">搜索 AKShare 可用接口</p>
    <p class="api-params">参数: keyword(搜索关键词) limit(返回条数)</p>
    <button class="test-btn" onclick="testAPI('search')">在线测试</button>
    <div class="result-box" id="result-search"></div>
  </div>

</div>

<div class="footer">
  数据来源: <a href="https://github.com/akfamily/akshare" target="_blank">AKShare</a> |
  <a href="https://github.com/gongyanghsuyun/Akshare" target="_blank">GitHub</a> |
  仅供学术研究使用，不构成投资建议
</div>

<script>
async function testAPI(path) {
  const boxId = 'result-' + path.replace('/', '-');
  const box = document.getElementById(boxId);
  if (box.classList.contains('show')) {
    box.classList.remove('show');
    return;
  }
  box.classList.add('show');
  box.textContent = '加载中...';

  let url = '/api/' + path;
  if (path === 'stock/hist') {
    url += '?symbol=000001&start_date=20250901&end_date=20250930&adjust=qfq';
  } else if (path === 'stock/spot') {
    url += '?limit=5';
  } else if (path === 'fund/nav') {
    url += '?symbol=005827&limit=5';
  } else if (path === 'macro/cpi') {
    url += '?limit=5';
  } else if (path === 'search') {
    url += '?keyword=可转债&limit=5';
  }

  try {
    const resp = await fetch(url);
    const data = await resp.json();
    box.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    box.textContent = '请求失败: ' + e.message;
  }
}
</script>

</body>
</html>"""


@app.route("/")
def index():
    html = HTML_PAGE.replace("__VERSION__", ak.__version__)
    return Response(html, mimetype="text/html; charset=utf-8")


@app.route("/api/info")
def api_info():
    return json_response({
        "service": "AKShare API",
        "version": ak.__version__,
        "endpoints": {
            "/api/stock/hist": "A股历史行情 (symbol, period, start_date, end_date, adjust)",
            "/api/stock/spot": "A股实时行情快照",
            "/api/fund/nav": "基金净值 (symbol)",
            "/api/macro/cpi": "CPI月度数据",
            "/api/search": "接口搜索 (keyword, limit)",
        }
    })


@app.route("/api/stock/hist")
def stock_hist():
    symbol = request.args.get("symbol", "000001")
    period = request.args.get("period", "daily")
    start_date = request.args.get("start_date", "20250101")
    end_date = request.args.get("end_date", "20250930")
    adjust = request.args.get("adjust", "qfq")
    df = ak.stock_zh_a_hist(
        symbol=symbol, period=period,
        start_date=start_date, end_date=end_date, adjust=adjust
    )
    return json_response(df.to_dict(orient="records"))


@app.route("/api/stock/spot")
def stock_spot():
    df = ak.stock_zh_a_spot_em()
    limit = int(request.args.get("limit", 20))
    return json_response(df.head(limit).to_dict(orient="records"))


@app.route("/api/fund/nav")
def fund_nav():
    symbol = request.args.get("symbol", "005827")
    df = ak.fund_open_fund_info_em(symbol=symbol, indicator="单净值走势")
    limit = int(request.args.get("limit", 30))
    return json_response(df.tail(limit).to_dict(orient="records"))


@app.route("/api/macro/cpi")
def macro_cpi():
    df = ak.macro_china_cpi_monthly()
    limit = int(request.args.get("limit", 30))
    return json_response(df.tail(limit).to_dict(orient="records"))


@app.route("/api/search")
def search():
    keyword = request.args.get("keyword", "可转债")
    limit = int(request.args.get("limit", 10))
    df = ak.search(keyword, limit=limit)
    return json_response(df.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True)