import streamlit as st
from abc import ABC, abstractmethod

# Page configuration
st.set_page_config(
    page_title="CropCompass",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Streamlit page styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
  --earth:    #3B2A1A;
  --soil:     #5C3D2E;
  --bark:     #7A5C44;
  --straw:    #C8A96E;
  --gold:     #E6C97A;
  --leaf:     #4A7C59;
  --sprout:   #6DAA7A;
  --sky:      #D4EAD0;
  --cream:    #FAF5EB;
  --paper:    #F2EAD3;
  --ink:      #1A1208;
  --muted:    #8C7B6B;
  --red:      #C0392B;
  --shadow:   rgba(30,15,5,0.18);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
  background: var(--cream);
  font-family: 'DM Sans', sans-serif;
  color: var(--ink);
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { display: none; }

.hero {
  background: linear-gradient(160deg, var(--earth) 0%, var(--leaf) 100%);
  border-radius: 20px;
  padding: 3.5rem 3rem 2.8rem;
  margin-bottom: 2.5rem;
  position: relative;
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute; inset: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.04'%3E%3Ccircle cx='30' cy='30' r='12'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  pointer-events: none;
}
.hero-badge {
  display: inline-block;
  background: rgba(255,255,255,0.15);
  border: 1px solid rgba(255,255,255,0.25);
  border-radius: 30px;
  padding: 4px 14px;
  font-size: 0.72rem;
  color: var(--sky);
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 1rem;
  font-weight: 600;
}
.hero h1 {
  font-family: 'Playfair Display', serif;
  font-size: 3.2rem;
  font-weight: 900;
  color: var(--gold);
  line-height: 1.1;
  margin-bottom: 0.7rem;
}
.hero p {
  color: rgba(255,255,255,0.75);
  font-size: 1.05rem;
  font-weight: 300;
  max-width: 520px;
}

.step-bar {
  display: flex;
  align-items: center;
  gap: 0;
  margin-bottom: 2.5rem;
  background: var(--paper);
  border-radius: 50px;
  padding: 6px;
  border: 1px solid rgba(90,60,40,0.12);
}
.step-item {
  flex: 1;
  text-align: center;
  padding: 10px 6px;
  border-radius: 40px;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--muted);
  cursor: default;
}
.step-item.active {
  background: var(--leaf);
  color: #fff;
  box-shadow: 0 2px 12px rgba(74,124,89,0.35);
}
.step-item.done {
  background: var(--sky);
  color: var(--leaf);
}

.card {
  background: #fff;
  border-radius: 16px;
  padding: 1.8rem 2rem;
  border: 1px solid rgba(90,60,40,0.1);
  box-shadow: 0 2px 16px var(--shadow);
  margin-bottom: 1.4rem;
}
.card-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--earth);
  margin-bottom: 1.1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}
.card-title span.icon {
  background: var(--sky);
  width: 32px; height: 32px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1rem;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.4rem;
}
.kpi {
  background: var(--paper);
  border-radius: 14px;
  padding: 1.2rem 1.4rem;
  border: 1px solid rgba(90,60,40,0.1);
  position: relative;
  overflow: hidden;
}
.kpi::after {
  content: '';
  position: absolute;
  top: -20px; right: -20px;
  width: 80px; height: 80px;
  border-radius: 50%;
  background: rgba(74,124,89,0.07);
}
.kpi .label {
  font-size: 0.72rem;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--muted);
  font-weight: 600;
  margin-bottom: 6px;
}
.kpi .amount { font-family: 'Playfair Display', serif; font-size: 1.7rem; font-weight: 700; color: var(--earth); }
.kpi .amount.profit  { color: var(--leaf); }
.kpi .amount.expense { color: var(--red);  }
.kpi .amount.gross   { color: var(--bark); }

.info-table { width: 100%; border-collapse: collapse; }
.info-table tr { border-bottom: 1px solid rgba(90,60,40,0.07); }
.info-table tr:last-child { border-bottom: none; }
.info-table td { padding: 9px 4px; font-size: 0.9rem; }
.info-table td:first-child { color: var(--muted); font-weight: 500; width: 52%; }
.info-table td:last-child  { color: var(--ink); font-weight: 600; text-align: right; }

.region-pill {
  display: inline-block;
  padding: 6px 18px;
  border-radius: 30px;
  font-size: 0.82rem;
  font-weight: 600;
  background: var(--sky);
  color: var(--leaf);
  border: 1.5px solid var(--sprout);
}

.veg-divider {
  text-align: center;
  color: var(--straw);
  letter-spacing: 4px;
  font-size: 1.1rem;
  margin: 1.2rem 0;
}

.forecast-header {
  background: linear-gradient(135deg, var(--earth), var(--soil));
  border-radius: 14px;
  padding: 1.4rem 1.8rem;
  color: var(--gold);
  font-family: 'Playfair Display', serif;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.4rem;
  display: flex;
  align-items: center;
  gap: 12px;
}

.profit-strip {
  border-radius: 14px;
  padding: 1.4rem 1.8rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.profit-strip.positive { background: linear-gradient(135deg, #e8f5e9, #c8e6c9); border: 1.5px solid var(--sprout); }
.profit-strip.negative { background: linear-gradient(135deg, #fce4ec, #ffcdd2); border: 1.5px solid #e57373; }

.stButton > button {
  background: var(--leaf) !important;
  color: #fff !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.95rem !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 0.65rem 1.6rem !important;
  width: 100%;
  transition: all 0.2s !important;
}
.stButton > button:hover { background: var(--earth) !important; transform: translateY(-1px); }

.stSelectbox label, .stNumberInput label, .stTextInput label {
  color: var(--muted) !important;
  font-size: 0.82rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.5px !important;
  text-transform: uppercase !important;
}
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
  background: var(--paper) !important;
  border: 1.5px solid rgba(90,60,40,0.18) !important;
  border-radius: 10px !important;
  color: var(--ink) !important;
  font-family: 'DM Sans', sans-serif !important;
}
.stRadio label { color: var(--ink) !important; font-weight: 500 !important; }
.stRadio > div { gap: 12px !important; }

.thankyou {
  background: linear-gradient(135deg, var(--earth) 0%, var(--leaf) 100%);
  border-radius: 20px;
  padding: 3rem;
  text-align: center;
  color: #fff;
  margin-top: 2rem;
}
.thankyou h2 { font-family: 'Playfair Display', serif; font-size: 2rem; color: var(--gold); margin-bottom: 0.6rem; }
.thankyou p  { opacity: 0.8; font-size: 0.95rem; }
</style>
""", unsafe_allow_html=True)

# Business Logic — ported from updated notebook

class FarmResource:
    """
    Calculates farm resources: labour, fertilizer, and overall expenses.
    """

    clearing_constant            = 1002   # GH₵ per acre, industry standard
    farm_labour_constant         = 1008   # GH₵ per acre, industry standard
    clearing_decrement_multiplier = 0.8   # Cost reduction for Mid/North clearing
    labour_decrement_multiplier   = 0.6   # Cost reduction for North labour

    def __init__(self, fertilizer_cost, is_cleared, acre):
        self.is_cleared      = is_cleared   # int: 1 = cleared (North/Mid), 2 = cleared (South)
        self.__acre          = acre
        self.fertilizer_cost = fertilizer_cost

    @property
    def acre(self):
        return self.__acre

    @acre.setter
    def acre(self, value):
        if value <= 0:
            raise ValueError("Farm size must be greater than 0 acres.")
        self.__acre = value

    def determine_if_cleared(self):
        # Southern Ghana: is_cleared == 2 triggers clearing cost
        if self.is_cleared == 2:
            return FarmResource.clearing_constant * self.acre
        return 0

    def labour_cost(self):
        return FarmResource.farm_labour_constant * self.acre

    def total_fertilizer_cost(self):
        return self.fertilizer_cost * self.acre

    def overall_farm_expenses(self):
        return self.determine_if_cleared() + self.labour_cost() + self.total_fertilizer_cost()


class North(FarmResource):
    """Northern Ghana — reduced labour & fertilizer costs (×0.6)."""

    def determine_if_cleared(self):
        # North/Mid: is_cleared == 1 triggers clearing cost
        if self.is_cleared == 1:
            return (FarmResource.clearing_constant * self.acre) * \
                FarmResource.clearing_decrement_multiplier
        return 0

    def labour_cost(self):
        return (FarmResource.farm_labour_constant * self.acre) * \
            FarmResource.labour_decrement_multiplier

    def total_fertilizer_cost(self):
        return (self.fertilizer_cost * self.acre) * \
            FarmResource.labour_decrement_multiplier

    def overall_farm_expenses(self):
        return (self.determine_if_cleared() + self.labour_cost() + self.total_fertilizer_cost()) * \
            FarmResource.labour_decrement_multiplier


class Mid(FarmResource):
    """Mid Ghana — moderately reduced costs (×0.8)."""

    def determine_if_cleared(self):
        if self.is_cleared == 1:
            return (FarmResource.clearing_constant * self.acre) * \
                FarmResource.clearing_decrement_multiplier
        return 0

    def labour_cost(self):
        return (FarmResource.farm_labour_constant * self.acre) * \
            FarmResource.clearing_decrement_multiplier

    def total_fertilizer_cost(self):
        return (self.fertilizer_cost * self.acre) * \
            FarmResource.clearing_decrement_multiplier

    def overall_farm_expenses(self):
        return (self.determine_if_cleared() + self.labour_cost() + self.total_fertilizer_cost()) * \
            FarmResource.clearing_decrement_multiplier


class Information:
    """Stores researched crop data for all supported crops."""

    crop_duration = {
        "Sorghum": 3, "Cotton": 5, "Tomato": 4,
        "Pepper": 4, "Cocoa": 60, "Groundnut": 4,
    }
    seed_cost = {
        "Sorghum": 80, "Cotton": 132, "Tomato": 120,
        "Pepper": 160, "Cocoa": 1350, "Groundnut": 40,
    }
    seed_spacing = {
        "Sorghum": "60 cm by 75 cm", "Cotton": "90 cm by 30 cm",
        "Tomato": "60 cm by 75 cm", "Pepper": "60 cm by 75 cm",
        "Cocoa": "300 cm by 300 cm", "Groundnut": "30 cm by 10 cm",
    }
    yield_per_acre = {
        "Sorghum": 1000, "Cotton": 250, "Tomato": 8000,
        "Pepper": 5000, "Cocoa": 200, "Groundnut": 2000,
    }
    num_of_crops_per_acre = {
        "Sorghum": 21000, "Cotton": 30000, "Tomato": 3000,
        "Pepper": 3000, "Cocoa": 444, "Groundnut": 4000,
    }
    irrigation_types = {
        "Drip":     ["Tomato", "Pepper", "Cotton"],
        "Rainfall": ["Sorghum", "Cocoa", "Groundnut"],
    }
    fertilizer_cost_per_acre = {
        "Sorghum": 700, "Cotton": 1162, "Tomato": 1600,
        "Pepper": 1004, "Cocoa": 1004, "Groundnut": 200,
    }
    crop_fertilizer = {
        "NPK":  ["Sorghum", "Groundnut", "Cocoa", "Pepper"],
        "Urea": ["Tomato", "Cotton"],
    }
    price_per_kg = {
        "Sorghum": 20, "Cotton": 365, "Tomato": 10,
        "Pepper": 10, "Cocoa": 40, "Groundnut": 50,
    }

    def __init__(self, crop):
        self.crop = crop

    def all_info(self):
        irrigation = next((k for k, v in self.irrigation_types.items() if self.crop in v), None)
        fertilizer = next((k for k, v in self.crop_fertilizer.items() if self.crop in v), None)
        return (
            self.crop_duration[self.crop],
            self.num_of_crops_per_acre[self.crop],
            self.seed_spacing[self.crop],
            self.price_per_kg[self.crop],
            irrigation,
            fertilizer,
        )

    def get_seed_info(self):
        return self.seed_cost[self.crop], self.yield_per_acre[self.crop], self.price_per_kg[self.crop]

    def get_fertilizer_cost(self):
        return self.fertilizer_cost_per_acre[self.crop]


class CropFunctionality(ABC):
    @abstractmethod
    def total_seed_cost(self): pass
    @abstractmethod
    def calculate_yield(self): pass
    @abstractmethod
    def calculate_revenue(self): pass


class Crop(CropFunctionality):
    """Calculates seed cost, expected yield, and revenue."""

    def __init__(self, seed_cost_per_acre, yield_per_acre, price_per_kg, farm_expenses, farm_acre):
        self.seed_cost_per_acre = seed_cost_per_acre
        self.__farm_acre        = farm_acre
        self.yield_per_acre     = yield_per_acre
        self.price_per_kg       = price_per_kg
        self.farm_expenses      = farm_expenses

    def total_seed_cost(self):
        return self.seed_cost_per_acre * self.__farm_acre

    def calculate_yield(self):
        return self.yield_per_acre * self.__farm_acre

    def calculate_revenue(self):
        total_of_seed = self.total_seed_cost()
        total_yield   = self.calculate_yield()
        all_expenses  = total_of_seed + self.farm_expenses          # seed cost + farm overhead
        gross_revenue = total_yield * self.price_per_kg             # kg × GH₵/kg
        net_revenue   = gross_revenue - all_expenses
        return net_revenue, gross_revenue, all_expenses, total_of_seed, total_yield


# Helper variables

REGION_CROPS = {
    "Northern Ghana": ["Cotton", "Groundnut", "Sorghum", "Tomato"],
    "Mid Ghana":      ["Pepper", "Tomato"],
    "Southern Ghana": ["Cocoa", "Pepper", "Tomato"],
}

CROP_EMOJI   = {"Cotton":"🌿","Groundnut":"🥜","Sorghum":"🌾","Tomato":"🍅","Pepper":"🌶️","Cocoa":"🍫"}
REGION_EMOJI = {"Northern Ghana":"☀️","Mid Ghana":"🌤️","Southern Ghana":"🌧️"}

REGION_NOTES = {
    "Northern Ghana": "☀️ Labour & fertilizer costs reduced by 40% (×0.6). Total expenses further reduced by 40%.",
    "Mid Ghana":      "🌤️ Clearing, labour & fertilizer costs reduced by 20% (×0.8). Total expenses further reduced by 20%.",
    "Southern Ghana": "🌧️ Standard industry rates applied — no regional adjustment.",
}

COMPANY_NUMBER = "0244454647"

# Computing forecast

def compute_forecast(region: str, crop: str, acres: int, is_cleared: bool) -> dict:
    """
    Run the full financial projection and return a results dict.

    is_cleared integer mapping:
      North / Mid  → cleared=1, uncleared=0  (checked with == 1)
      Southern     → cleared=2, uncleared=0  (checked with == 2)
    """
    info = Information(crop)
    seed_cpa, yield_pa, price_pkg = info.get_seed_info()
    fert_cost = info.get_fertilizer_cost()

    # Map boolean cleared to the integer each class expects
    if region == "Northern Ghana":
        cleared_int = 1 if is_cleared else 0
        farm = North(fert_cost, cleared_int, acres)
    elif region == "Mid Ghana":
        cleared_int = 1 if is_cleared else 0
        farm = Mid(fert_cost, cleared_int, acres)
    else:
        cleared_int = 2 if is_cleared else 0
        farm = FarmResource(fert_cost, cleared_int, acres)

    clearing_cost   = farm.determine_if_cleared()
    labour          = farm.labour_cost()
    fert_cost_total = farm.total_fertilizer_cost()
    all_expenses    = farm.overall_farm_expenses()

    crop_obj = Crop(seed_cpa, yield_pa, price_pkg, all_expenses, acres)
    net, gross, expenses, seed_total, total_yield = crop_obj.calculate_revenue()
    dur, n_crops, spacing, price, irr, fert = info.all_info()

    return {
        "net": net, "gross": gross, "expenses": expenses,
        "seed_total": seed_total, "total_yield": total_yield,
        "fert_cost_total": fert_cost_total,
        "labour": labour, "clearing_cost": clearing_cost,
        "all_expenses": all_expenses,
        "dur": dur, "n_crops": n_crops, "spacing": spacing,
        "price": price, "irr": irr, "fert": fert,
    }


# Session state for Streamlit 

for k, v in {"step":1,"name":"","region":None,"crop":None,"acres":1,"cleared":True,"forecast":None}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Hero section for Streamlit

st.markdown("""
<div class="hero">
  <div class="hero-badge">🌱 Agricultural Finance Tool · Ghana</div>
  <h1>CropCompass</h1>
  <p>Your financial guide to a successful farming venture. Project costs, yields, and profits before breaking ground.</p>
</div>
""", unsafe_allow_html=True)


# Step bar

step = st.session_state["step"]
steps = ["📋 Farm Details", "📊 Financial Forecast", "✅ Done"]

def step_cls(i):
    n = i + 1
    if n < step:  return "step-item done"
    if n == step: return "step-item active"
    return "step-item"

st.markdown(
    '<div class="step-bar">' +
    "".join(f'<div class="{step_cls(i)}">{s}</div>' for i, s in enumerate(steps)) +
    '</div>',
    unsafe_allow_html=True,
)


# STEP 1 - Farm Details 

if st.session_state["step"] == 1:

    col_left, col_right = st.columns([1.1, 1], gap="large")

    with col_left:
        # A. Name
        st.markdown('<div class="card"><div class="card-title"><span class="icon">👤</span>Farmer Information</div>', unsafe_allow_html=True)
        name = st.text_input("Your full name", value=st.session_state["name"], placeholder="e.g. Kwame Asante")
        st.markdown('</div>', unsafe_allow_html=True)

        # B. Region
        st.markdown('<div class="card"><div class="card-title"><span class="icon">📍</span>Farm Location</div>', unsafe_allow_html=True)
        region_opts = ["— Select a region —"] + list(REGION_CROPS.keys())
        region = st.selectbox(
            "Which region of Ghana?",
            region_opts,
            index=0 if not st.session_state["region"]
                  else region_opts.index(st.session_state["region"]),
            format_func=lambda x: f"{REGION_EMOJI.get(x,'')} {x}" if x in REGION_EMOJI else x,
        )
        valid_region = region != "— Select a region —"
        if valid_region:
            st.markdown(f'<div style="margin-top:8px"><span class="region-pill">{REGION_EMOJI[region]} {region}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:var(--muted);font-size:0.83rem;margin-top:8px">{REGION_NOTES[region]}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        # C. Crop
        st.markdown('<div class="card"><div class="card-title"><span class="icon">🌾</span>Crop Selection</div>', unsafe_allow_html=True)
        available_crops = REGION_CROPS.get(region if valid_region else "", [])

        if not available_crops:
            st.markdown('<p style="color:var(--muted);font-size:0.9rem">Select a region first to see available crops.</p>', unsafe_allow_html=True)
            crop = None
        else:
            crop_opts = ["— Select a crop —"] + available_crops
            prev_crop = st.session_state["crop"]
            crop_sel = st.selectbox(
                "Crop to cultivate",
                crop_opts,
                index=0 if not prev_crop or prev_crop not in available_crops
                      else crop_opts.index(prev_crop),
                format_func=lambda x: f"{CROP_EMOJI.get(x,'')} {x}" if x in CROP_EMOJI else x,
            )
            crop = crop_sel if crop_sel != "— Select a crop —" else None

            if crop:
                info = Information(crop)
                dur, n_crops, spacing, price, irr, fert = info.all_info()
                st.markdown(f"""
                <table class="info-table" style="margin-top:10px">
                  <tr><td>Duration</td><td>{dur} months</td></tr>
                  <tr><td>Spacing</td><td>{spacing}</td></tr>
                  <tr><td>Irrigation</td><td>{irr}</td></tr>
                  <tr><td>Fertilizer</td><td>{fert}</td></tr>
                  <tr><td>Price per kg</td><td>GH₵ {price:.2f}</td></tr>
                </table>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # D & E. Land details
        st.markdown('<div class="card"><div class="card-title"><span class="icon">🏡</span>Land Details</div>', unsafe_allow_html=True)
        acres = st.number_input("Number of acres to cultivate", min_value=1, max_value=500,
                                value=st.session_state["acres"], step=1)
        cleared_choice = st.radio(
            "Is the land already cleared and ready?",
            ["Yes — land is cleared", "No — clearing required"],
            index=0 if st.session_state["cleared"] else 1,
            horizontal=True,
        )
        is_cleared = cleared_choice.startswith("Yes")
        st.markdown('</div>', unsafe_allow_html=True)

    # Validation + proceed
    can_proceed = bool(name.strip()) and valid_region and crop is not None
    if not can_proceed:
        missing = [x for cond, x in [(not name.strip(), "your name"), (not valid_region, "a region"), (crop is None, "a crop")] if cond]
        st.markdown(f'<p style="color:var(--muted);font-size:0.87rem;text-align:center">Fill in: {", ".join(missing)} to continue.</p>', unsafe_allow_html=True)

    _, col_btn, _ = st.columns([2, 1.2, 2])
    with col_btn:
        if st.button("Generate Forecast →", disabled=not can_proceed):
            st.session_state.update({
                "name":    name.strip().title(),
                "region":  region,
                "crop":    crop,
                "acres":   acres,
                "cleared": is_cleared,
                "step":    2,
                "forecast": compute_forecast(region, crop, acres, is_cleared),
            })
            st.rerun()


# STEP 2 — Financial Forecast

elif st.session_state["step"] == 2:
    f      = st.session_state["forecast"]
    nm     = st.session_state["name"]
    crop   = st.session_state["crop"]
    region = st.session_state["region"]
    acres  = st.session_state["acres"]

    st.markdown(f'<div class="forecast-header">📈 Financial Forecast for {nm}</div>', unsafe_allow_html=True)

    # Profit / loss strip
    is_profit     = f["net"] >= 0
    strip_class   = "positive" if is_profit else "negative"
    profit_icon   = "📈" if is_profit else "📉"
    profit_label  = "Projected Profit" if is_profit else "Projected Loss"
    amount_colour = "var(--leaf)" if is_profit else "var(--red)"

    st.markdown(f"""
    <div class="profit-strip {strip_class}">
      <div>
        <div style="font-size:0.75rem;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:{amount_colour}">
          {profit_icon} {profit_label}
        </div>
        <div style="font-family:'Playfair Display',serif;font-size:2.2rem;font-weight:700;color:{amount_colour}">
          GH₵ {f['net']:,.2f}
        </div>
      </div>
      <div style="text-align:right;color:var(--muted);font-size:0.88rem;line-height:1.8">
        <div>{CROP_EMOJI.get(crop,'')} {crop} &nbsp;·&nbsp; {acres} acre(s)</div>
        <div>{REGION_EMOJI.get(region,'')} {region}</div>
        <div>📅 {f['dur']} month{'s' if f['dur'] != 1 else ''} crop cycle</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="veg-divider">· · · · ·</div>', unsafe_allow_html=True)

    # KPI cards
    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi"><div class="label">Gross Revenue</div><div class="amount gross">GH₵ {f['gross']:,.2f}</div></div>
      <div class="kpi"><div class="label">Total Expenses</div><div class="amount expense">GH₵ {f['expenses']:,.2f}</div></div>
      <div class="kpi"><div class="label">Expected Yield</div><div class="amount">{f['total_yield']:,} kg</div></div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        st.markdown(f"""
        <div class="card">
          <div class="card-title"><span class="icon">🌱</span>Crop Information</div>
          <table class="info-table">
            <tr><td>Crop</td><td>{CROP_EMOJI.get(crop,'')} {crop}</td></tr>
            <tr><td>Crop Duration</td><td>{f['dur']} months</td></tr>
            <tr><td>Seed Spacing</td><td>{f['spacing']}</td></tr>
            <tr><td>Plants per Acre</td><td>{f['n_crops']:,}</td></tr>
            <tr><td>Total Plants</td><td>{f['n_crops'] * acres:,}</td></tr>
            <tr><td>Irrigation Type</td><td>{f['irr']}</td></tr>
            <tr><td>Fertilizer Type</td><td>{f['fert']}</td></tr>
            <tr><td>Price per kg</td><td>GH₵ {f['price']:.2f}</td></tr>
            <tr><td>Total Yield</td><td>{f['total_yield']:,} kg</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown(f"""
        <div class="card">
          <div class="card-title"><span class="icon">💰</span>Cost Breakdown</div>
          <table class="info-table">
            <tr><td>Seed Cost (total)</td><td>GH₵ {f['seed_total']:,.2f}</td></tr>
            <tr><td>Fertilizer Cost</td><td>GH₵ {f['fert_cost_total']:,.2f}</td></tr>
            <tr><td>Labour Cost</td><td>GH₵ {f['labour']:,.2f}</td></tr>
            <tr><td>Land Clearing</td><td>GH₵ {f['clearing_cost']:,.2f}</td></tr>
            <tr><td style="border-top:1.5px solid var(--straw);padding-top:10px">
                  <b>All Farm Expenses</b></td>
                <td style="border-top:1.5px solid var(--straw);padding-top:10px">
                  <b>GH₵ {f['all_expenses']:,.2f}</b></td></tr>
          </table>
          <div style="margin-top:14px;background:var(--paper);border-radius:10px;padding:10px 14px">
            <div style="font-size:0.75rem;color:var(--muted);font-weight:600;letter-spacing:1px;
                        text-transform:uppercase;margin-bottom:8px">Expense Breakdown</div>
        """, unsafe_allow_html=True)

        components = {
            "Seed":       f["seed_total"],
            "Fertilizer": f["fert_cost_total"],
            "Labour":     f["labour"],
            "Clearing":   f["clearing_cost"],
        }
        bar_colors = {"Seed":"#4A7C59","Fertilizer":"#C8A96E","Labour":"#7A5C44","Clearing":"#E6C97A"}
        total_c = sum(components.values()) or 1
        for label, val in components.items():
            pct = val / total_c * 100
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
              <div style="width:72px;font-size:0.78rem;color:var(--muted)">{label}</div>
              <div style="flex:1;background:#e0d8cc;border-radius:4px;height:10px">
                <div style="background:{bar_colors[label]};width:{pct:.1f}%;height:100%;border-radius:4px"></div>
              </div>
              <div style="width:82px;text-align:right;font-size:0.78rem;font-weight:600">GH₵ {val:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    # Consultancy note
    st.markdown(f"""
    <div style="background:var(--paper);border-radius:14px;padding:1.2rem 1.6rem;
                border:1.5px solid rgba(90,60,40,0.12);margin-top:0.5rem;
                display:flex;align-items:center;gap:14px">
      <div style="font-size:2rem">📞</div>
      <div>
        <div style="font-weight:700;font-size:0.9rem;color:var(--earth)">Need expert advice?</div>
        <div style="color:var(--muted);font-size:0.85rem">
          Call CropCompass consultants: <b style="color:var(--leaf)">{COMPANY_NUMBER}</b>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
    col_b1, col_b2, col_b3 = st.columns([1.5, 1, 1.5])
    with col_b2:
        if st.button("← Start Over"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
    with col_b3:
        if st.button("Finish ✓"):
            st.session_state["step"] = 3
            st.rerun()

# STEP 3 - End page

elif st.session_state["step"] == 3:
    nm = st.session_state["name"]
    st.markdown(f"""
    <div class="thankyou">
      <div style="font-size:3.5rem;margin-bottom:1rem">🌾</div>
      <h2>Thank you, {nm}!</h2>
      <p>Thank you for using CropCompass — your financial guide to successful farming.</p>
      <p style="margin-top:8px">For further consultations, reach us at
         <b style="color:var(--gold)">{COMPANY_NUMBER}</b>.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
    _, col_x, _ = st.columns([2, 1, 2])
    with col_x:
        if st.button("New Projection"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
