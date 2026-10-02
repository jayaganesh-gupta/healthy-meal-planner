import random
import streamlit as st
import pandas as pd
from meal_data import MEALS, DIETARY_GOALS, ALL_TAGS, CATEGORIES

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Healthy Meal Planner",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .meal-card {
        background: #f8fdf4;
        border: 1px solid #d4edda;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .meal-title { font-size: 18px; font-weight: 700; color: #1a6b2e; }
    .tag-badge {
        display: inline-block;
        background: #e8f5e9;
        color: #2e7d32;
        border-radius: 12px;
        padding: 2px 10px;
        font-size: 12px;
        margin: 2px;
        border: 1px solid #c8e6c9;
    }
    .section-header {
        font-size: 22px;
        font-weight: 700;
        color: #1a6b2e;
        border-bottom: 3px solid #4caf50;
        padding-bottom: 6px;
        margin-bottom: 16px;
    }
    .progress-bar-wrapper {
        background: #e0e0e0;
        border-radius: 6px;
        height: 12px;
        margin: 4px 0 12px 0;
        overflow: hidden;
    }
    .progress-bar-fill {
        height: 100%;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)


# ── Constants ─────────────────────────────────────────────────────────────────
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
SLOTS = ["Breakfast", "Lunch", "Dinner", "Snack"]


# ── Session state init ────────────────────────────────────────────────────────
if "meal_plan" not in st.session_state:
    st.session_state.meal_plan = {day: {slot: None for slot in SLOTS} for day in DAYS}

if "goal" not in st.session_state:
    st.session_state.goal = "Maintenance"

if "custom_goals" not in st.session_state:
    st.session_state.custom_goals = {k: int(v) for k, v in DIETARY_GOALS["Maintenance"].items()}


# ── Helper functions ──────────────────────────────────────────────────────────
def totals(meal_list):
    """Sum nutritional values across a list of meals."""
    return {
        "calories": sum(m["calories"] for m in meal_list),
        "protein":  sum(m["protein"]  for m in meal_list),
        "carbs":    sum(m["carbs"]    for m in meal_list),
        "fat":      sum(m["fat"]      for m in meal_list),
        "fiber":    sum(m["fiber"]    for m in meal_list),
    }


def macro_bar(label, value, target, color):
    """Render a labeled HTML progress bar for a single macro."""
    pct = min(int(value / target * 100), 100) if target else 0
    bar_color = "#e53935" if value > target else color
    st.markdown(
        f"""
        <div style="display:flex; justify-content:space-between; font-size:13px;">
            <span><b>{label}</b></span>
            <span>{value} / {target}</span>
        </div>
        <div class="progress-bar-wrapper">
            <div class="progress-bar-fill" style="width:{pct}%; background:{bar_color};"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_meal_card(meal, plan_day=None, plan_slot=None):
    """Render a styled meal card with optional quick-add button."""
    tags_html = " ".join(f'<span class="tag-badge">{t}</span>' for t in meal["tags"])
    ingredients = ", ".join(meal["ingredients"])
    with st.container():
        st.markdown(
            f"""
            <div class="meal-card">
                <div class="meal-title">🍽 {meal['name']}</div>
                <div style="color:#555; font-size:13px; margin:4px 0;">
                    📂 {meal['category']} &nbsp;|&nbsp; ⏱ {meal['prep_time']} min
                </div>
                <div style="margin:6px 0;">{tags_html}</div>
                <details>
                    <summary style="cursor:pointer; font-size:13px; color:#4caf50;">Ingredients</summary>
                    <p style="font-size:13px; color:#444; margin:6px 0 0 0;">{ingredients}</p>
                </details>
            </div>
            """,
            unsafe_allow_html=True,
        )
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Calories", f"{meal['calories']} kcal")
        col2.metric("Protein",  f"{meal['protein']}g")
        col3.metric("Carbs",    f"{meal['carbs']}g")
        col4.metric("Fat",      f"{meal['fat']}g")

        if plan_day and plan_slot:
            btn_key = f"add_{meal['name']}_{plan_day}_{plan_slot}"
            if st.button(f"➕ Add to {plan_day} — {plan_slot}", key=btn_key):
                st.session_state.meal_plan[plan_day][plan_slot] = meal
                st.success(f"Added **{meal['name']}** to {plan_day} – {plan_slot}!")
                st.rerun()


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="text-align:center; font-size:64px; line-height:1.2;">🥗</div>', unsafe_allow_html=True)
    st.title("Meal Planner")
    st.markdown("---")

    st.subheader("🎯 Dietary Goal")
    goal_options = list(DIETARY_GOALS.keys())
    goal = st.selectbox(
        "Select your goal",
        goal_options,
        index=goal_options.index(st.session_state.goal),
    )
    st.session_state.goal = goal

    if goal == "Custom":
        st.markdown("**Set daily targets:**")
        cg = st.session_state.custom_goals
        cg["calories"] = int(st.number_input("Calories (kcal)", min_value=800,  max_value=4000, value=int(cg["calories"]), step=50))
        cg["protein"]  = int(st.number_input("Protein (g)",     min_value=30,   max_value=300,  value=int(cg["protein"]),  step=5))
        cg["carbs"]    = int(st.number_input("Carbs (g)",       min_value=50,   max_value=500,  value=int(cg["carbs"]),    step=5))
        cg["fat"]      = int(st.number_input("Fat (g)",         min_value=20,   max_value=200,  value=int(cg["fat"]),      step=5))
        cg["fiber"]    = int(st.number_input("Fiber (g)",       min_value=10,   max_value=80,   value=int(cg["fiber"]),    step=1))

    active_goals = st.session_state.custom_goals if goal == "Custom" else DIETARY_GOALS[goal]

    st.markdown("---")
    st.subheader("🔀 Auto-Generate Plan")
    if st.button("✨ Generate Random Plan", use_container_width=True):
        for day in DAYS:
            for slot in SLOTS:
                options = [m for m in MEALS if m["category"] == slot]
                st.session_state.meal_plan[day][slot] = random.choice(options) if options else None
        st.success("Random meal plan generated!")
        st.rerun()

    if st.button("🗑 Clear Plan", use_container_width=True):
        st.session_state.meal_plan = {day: {slot: None for slot in SLOTS} for day in DAYS}
        st.rerun()


# ── Main tabs ─────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📅 Weekly Planner",
    "🔍 Browse Meals",
    "📊 Nutrition Summary",
    "🛒 Shopping List",
])


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — Weekly Planner
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-header">📅 Weekly Meal Plan</div>', unsafe_allow_html=True)

    selected_day = st.selectbox("Select a day to edit", DAYS)
    st.markdown(f"### {selected_day}")

    day_plan = st.session_state.meal_plan[selected_day]
    day_meals = [m for m in day_plan.values() if m]
    day_totals = totals(day_meals)

    # Daily macro summary row
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("🔥 Calories", day_totals["calories"],  delta=f"/ {active_goals['calories']}")
    c2.metric("💪 Protein",  f"{day_totals['protein']}g",  delta=f"/ {active_goals['protein']}g")
    c3.metric("🌾 Carbs",    f"{day_totals['carbs']}g",    delta=f"/ {active_goals['carbs']}g")
    c4.metric("🧈 Fat",      f"{day_totals['fat']}g",      delta=f"/ {active_goals['fat']}g")
    c5.metric("🌿 Fiber",    f"{day_totals['fiber']}g",    delta=f"/ {active_goals['fiber']}g")

    st.markdown("---")

    for slot in SLOTS:
        st.markdown(f"#### {slot}")
        meal = day_plan.get(slot)
        col_meal, col_action = st.columns([3, 1])

        with col_meal:
            if meal:
                tags_html = " ".join(f'<span class="tag-badge">{t}</span>' for t in meal["tags"])
                st.markdown(
                    f"""
                    <div class="meal-card">
                        <div class="meal-title">{meal['name']}</div>
                        <div style="color:#555; font-size:13px;">
                            ⏱ {meal['prep_time']} min &nbsp;|&nbsp;
                            🔥 {meal['calories']} kcal &nbsp;|&nbsp;
                            💪 {meal['protein']}g protein
                        </div>
                        <div style="margin-top:6px;">{tags_html}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.info("No meal selected yet.")

        with col_action:
            if meal:
                if st.button("❌ Remove", key=f"rm_{selected_day}_{slot}"):
                    st.session_state.meal_plan[selected_day][slot] = None
                    st.rerun()
                if st.button("🔀 Swap", key=f"swap_{selected_day}_{slot}"):
                    options = [m for m in MEALS if m["category"] == slot and m["name"] != meal["name"]]
                    if options:
                        st.session_state.meal_plan[selected_day][slot] = random.choice(options)
                        st.rerun()
            else:
                options = [m for m in MEALS if m["category"] == slot]
                meal_names = [m["name"] for m in options]
                chosen = st.selectbox(
                    f"Choose {slot}",
                    ["— pick one —"] + meal_names,
                    key=f"pick_{selected_day}_{slot}",
                )
                if chosen != "— pick one —":
                    picked = next(m for m in options if m["name"] == chosen)
                    st.session_state.meal_plan[selected_day][slot] = picked
                    st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — Browse Meals
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-header">🔍 Browse & Filter Meals</div>', unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        cat_filter = st.multiselect("Category", CATEGORIES, default=CATEGORIES)
    with col_f2:
        tag_filter = st.multiselect("Dietary Tags", ALL_TAGS)
    with col_f3:
        max_cal = st.slider("Max Calories", min_value=100, max_value=600, value=600, step=10)

    st.markdown("##### Quick-add to plan:")
    qa_day  = st.selectbox("Day",       DAYS,  key="qa_day")
    qa_slot = st.selectbox("Meal slot", SLOTS, key="qa_slot")

    filtered = [
        m for m in MEALS
        if m["category"] in cat_filter
        and m["calories"] <= max_cal
        and (not tag_filter or any(t in m["tags"] for t in tag_filter))
    ]

    st.markdown(f"**{len(filtered)} meals found**")
    st.markdown("---")

    for meal in filtered:
        render_meal_card(meal, plan_day=qa_day, plan_slot=qa_slot)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — Nutrition Summary
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-header">📊 Weekly Nutrition Summary</div>', unsafe_allow_html=True)

    # Build per-day totals
    weekly_data = {}
    for day in DAYS:
        day_meals_w = [m for m in st.session_state.meal_plan[day].values() if m]
        weekly_data[day] = totals(day_meals_w)

    cal_data     = [weekly_data[d]["calories"] for d in DAYS]
    protein_data = [weekly_data[d]["protein"]  for d in DAYS]
    carb_data    = [weekly_data[d]["carbs"]    for d in DAYS]
    fat_data     = [weekly_data[d]["fat"]      for d in DAYS]
    fiber_data   = [weekly_data[d]["fiber"]    for d in DAYS]

    def avg(key):
        vals = [weekly_data[d][key] for d in DAYS]
        return round(sum(vals) / len(vals))

    # Weekly averages vs targets
    st.subheader("📈 Weekly Averages vs Targets")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Avg Calories", avg("calories"), delta=f"target {active_goals['calories']}")
    m2.metric("Avg Protein",  f"{avg('protein')}g",  delta=f"target {active_goals['protein']}g")
    m3.metric("Avg Carbs",    f"{avg('carbs')}g",    delta=f"target {active_goals['carbs']}g")
    m4.metric("Avg Fat",      f"{avg('fat')}g",      delta=f"target {active_goals['fat']}g")
    m5.metric("Avg Fiber",    f"{avg('fiber')}g",    delta=f"target {active_goals['fiber']}g")

    st.markdown("---")

    # Daily calorie bar chart using a DataFrame so axis labels work correctly
    st.subheader("📅 Daily Calorie Breakdown")
    cal_df = pd.DataFrame({"Calories (kcal)": cal_data}, index=DAYS)
    st.bar_chart(cal_df)

    # Macros line chart
    st.subheader("Macros per Day (g)")
    macro_df = pd.DataFrame(
        {
            "Protein (g)": protein_data,
            "Carbs (g)":   carb_data,
            "Fat (g)":     fat_data,
        },
        index=DAYS,
    )
    st.line_chart(macro_df)

    st.markdown("---")

    # Today's goal progress bars
    st.subheader("🎯 Today's Goal Progress (Monday)")
    today_meals = [m for m in st.session_state.meal_plan[DAYS[0]].values() if m]
    today_totals = totals(today_meals)
    macro_bar("Calories (kcal)", today_totals["calories"], active_goals["calories"], "#4caf50")
    macro_bar("Protein (g)",     today_totals["protein"],  active_goals["protein"],  "#2196f3")
    macro_bar("Carbs (g)",       today_totals["carbs"],    active_goals["carbs"],    "#ff9800")
    macro_bar("Fat (g)",         today_totals["fat"],      active_goals["fat"],      "#f44336")
    macro_bar("Fiber (g)",       today_totals["fiber"],    active_goals["fiber"],    "#9c27b0")


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — Shopping List
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-header">🛒 Shopping List</div>', unsafe_allow_html=True)

    # Collect all ingredients from the full week plan
    all_ingredients = {}  # type: dict
    for day in DAYS:
        for slot in SLOTS:
            planned_meal = st.session_state.meal_plan[day][slot]
            if planned_meal:
                for ing in planned_meal["ingredients"]:
                    all_ingredients[ing] = all_ingredients.get(ing, 0) + 1

    if not all_ingredients:
        st.info("Your meal plan is empty. Add meals to generate a shopping list.")
    else:
        st.markdown(f"**{len(all_ingredients)} unique ingredients** across your week's plan.")

        items = sorted(all_ingredients.items())
        half = len(items) // 2
        col_a, col_b = st.columns(2)

        with col_a:
            for ing, count in items[:half]:
                label = f"**{ing.title()}**" + (f" ×{count}" if count > 1 else "")
                st.checkbox(label, key=f"shop_a_{ing}")

        with col_b:
            for ing, count in items[half:]:
                label = f"**{ing.title()}**" + (f" ×{count}" if count > 1 else "")
                st.checkbox(label, key=f"shop_b_{ing}")

        st.markdown("---")

        export_text = "\n".join(
            f"[ ] {ing.title()}" + (f" x{count}" if count > 1 else "")
            for ing, count in sorted(all_ingredients.items())
        )
        st.download_button(
            label="⬇ Download Shopping List",
            data=export_text,
            file_name="shopping_list.txt",
            mime="text/plain",
            use_container_width=True,
        )
