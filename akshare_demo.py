# -*- coding: utf-8 -*-
"""
AKShare 快速示例脚本
运行方式:
  python akshare_demo.py
"""

import akshare as ak

print(f"AKShare 版本: {ak.__version__}\n")


def demo_stock_hist():
    """1. 获取A股个股历史行情"""
    print("=" * 60)
    print("1. A股历史行情 - 平安银行(000001)")
    print("=" * 60)
    df = ak.stock_zh_a_hist(
        symbol="000001", period="daily",
        start_date="20250101", end_date="20250930", adjust="qfq"
    )
    print(df.tail(5).to_string())
    print()


def demo_realtime_spot():
    """2. 获取A股实时行情快照"""
    print("=" * 60)
    print("2. A股实时行情快照（前10只）")
    print("=" * 60)
    df = ak.stock_zh_a_spot_em()
    print(df.head(10).to_string())
    print()


def demo_fund_nav():
    """3. 获取基金净值"""
    print("=" * 60)
    print("3. 基金净值 - 易方达蓝筹精选(005827)")
    print("=" * 60)
    df = ak.fund_open_fund_info_em(symbol="005827", indicator="单位净值走势")
    print(df.tail(5).to_string())
    print()


def demo_macro():
    """4. 获取宏观经济数据 - CPI"""
    print("=" * 60)
    print("4. 宏观经济数据 - CPI月度数据")
    print("=" * 60)
    df = ak.macro_china_cpi_monthly()
    print(df.tail(5).to_string())
    print()


def demo_search():
    """5. 接口搜索功能"""
    print("=" * 60)
    print("5. 接口搜索 - '可转债'")
    print("=" * 60)
    df = ak.search("可转债", limit=5)
    print(df.to_string())
    print()


if __name__ == "__main__":
    demo_stock_hist()
    demo_realtime_spot()
    demo_fund_nav()
    demo_macro()
    demo_search()
    print("所有示例执行完成！")