# 🌱 CropCompass — Agricultural Financial Projection

A Streamlit GUI for the CropCompass farming financial tool (Ghana).

## Setup & Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## How It Works

The app is a **3-step wizard**:

1. **Farm Details** — Enter your name, select your region (Northern / Mid / Southern Ghana), pick a crop available for that region, set land size (acres), and confirm if the land is already cleared.
2. **Financial Forecast** — Instantly see your:
   - Projected profit or loss
   - Gross revenue
   - Full cost breakdown (seed, fertilizer, labour, clearing)
   - Crop info (duration, spacing, irrigation type, fertilizer type)
   - Visual expense bar chart
3. **Done** — Thank-you screen with consultancy contact.

## Regional Pricing Logic (from original notebook)
| Region | Cost Adjustment |
|---|---|
| Northern Ghana | Labour × 0.6, Fertilizer × 0.6, Total × 0.6 |
| Mid Ghana | Labour × 0.8, Fertilizer × 0.8, Total × 0.8 |
| Southern Ghana | Standard rates (no adjustment) |

## Crops by Region
- **Northern Ghana**: Cotton, Groundnut, Sorghum, Tomato
- **Mid Ghana**: Pepper, Tomato
- **Southern Ghana**: Cocoa, Pepper, Tomato
