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


@app.route("/")
def index():
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
    """A股历史行情"""
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
    """A股实时行情快照"""
    df = ak.stock_zh_a_spot_em()
    limit = int(request.args.get("limit", 20))
    return json_response(df.head(limit).to_dict(orient="records"))


@app.route("/api/fund/nav")
def fund_nav():
    """基金净值"""
    symbol = request.args.get("symbol", "005827")
    df = ak.fund_open_fund_info_em(symbol=symbol, indicator="单位净值走势")
    limit = int(request.args.get("limit", 30))
    return json_response(df.tail(limit).to_dict(orient="records"))


@app.route("/api/macro/cpi")
def macro_cpi():
    """CPI月度数据"""
    df = ak.macro_china_cpi_monthly()
    limit = int(request.args.get("limit", 30))
    return json_response(df.tail(limit).to_dict(orient="records"))


@app.route("/api/search")
def search():
    """接口搜索"""
    keyword = request.args.get("keyword", "可转债")
    limit = int(request.args.get("limit", 10))
    df = ak.search(keyword, limit=limit)
    return json_response(df.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True)