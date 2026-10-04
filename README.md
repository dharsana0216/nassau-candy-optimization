# Nassau Candy Factory Optimization

## Generated project files
- `nassau_cleaned_working.csv` — cleaned dataset + current factory + proxy lead time
- `factory_scenario_results.csv` — all product × candidate factory scenarios
- `factory_recommendations.csv` — top recommendation per product
- `product_summary.csv` — product-level summary
- `app.py` — ready-to-run Streamlit dashboard

## Data audit
- Rows: 10,194
- Columns: 20
- Missing values: 0
- Duplicate rows: 0
- Products: 15
- Regions: 4
- Ship modes: 4

## Critical limitation
The CSV has no historical factory/origin column. Also, raw Ship Date - Order Date is about 904–1,642 days, which is not credible shipping lead time. The project therefore uses a clearly labeled proxy scenario model rather than pretending the dataset can train a causal factory-reassignment model.

## Run dashboard
```bash
pip install streamlit pandas numpy
streamlit run app.py
```
