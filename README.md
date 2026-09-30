# Akshare API

基于 [AKShare](https://github.com/akfamily/akshare) 的金融数据 API 服务，部署在 Vercel。

## API 接口

| 接口 | 参数 | 说明 |
|------|------|------|
| `GET /` | - | 服务信息 |
| `GET /api/stock/hist` | symbol, period, start_date, end_date, adjust | A股历史行情 |
| `GET /api/stock/spot` | limit | A股实时行情快照 |
| `GET /api/fund/nav` | symbol, limit | 基金净值 |
| `GET /api/macro/cpi` | limit | CPI月度数据 |
| `GET /api/search` | keyword, limit | 接口搜索 |

## 本地运行

```bash
pip install -r requirements.txt
python api/index.py
```

## 示例

```bash
# 获取平安银行历史行情
curl "http://localhost:5000/api/stock/hist?symbol=000001&start_date=20250101&end_date=20250930"

# 获取实时行情
curl "http://localhost:5000/api/stock/spot?limit=10"
```