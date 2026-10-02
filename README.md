# 🥗 Healthy Meal Planner

A fully interactive **weekly meal planner** built with Python and Streamlit.
Plan nutritious meals, track macros, and generate a shopping list — all in one app.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📅 Weekly Planner | Plan Breakfast, Lunch, Dinner & Snack for every day of the week |
| 🔍 Browse Meals | Filter meals by category, dietary tag, and calorie limit |
| 📊 Nutrition Summary | Weekly bar/line charts + daily macro progress bars |
| 🛒 Shopping List | Auto-generated from your plan; downloadable as `.txt` |
| 🎯 Dietary Goals | Choose from Weight Loss, Muscle Gain, Maintenance, Heart Health, or Custom |
| 🔀 Auto-Generate | One-click random meal plan generator |
| ❌ / 🔀 Remove / Swap | Quickly remove or swap any meal in the plan |

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the app

```bash
cd healthy_meal_planner
streamlit run app.py
```

The app will open at **http://localhost:8501** in your browser.

---

## 📁 Project Structure

```
healthy_meal_planner/
├── app.py            # Main Streamlit application
├── meal_data.py      # Meals database & dietary goals
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## 🍽 Meal Database

The app ships with **15 pre-built vegetarian meals** across four categories:

- **Breakfast** — Oatmeal with Berries, Greek Yogurt Parfait, Avocado Toast with Eggs, Smoothie Bowl
- **Lunch** — Paneer Tikka Salad, Quinoa Buddha Bowl, Chickpea & Veggie Wrap, Lentil Soup
- **Dinner** — Paneer & Veggie Curry, Tofu Stir-Fry, Black Bean Tacos, Spaghetti with Lentil Sauce
- **Snack** — Apple & Almond Butter, Hummus & Veggie Sticks, Mixed Nuts & Dried Fruit

Each meal includes: **calories, protein, carbs, fat, fiber, prep time, ingredients, and dietary tags**.

---

## 🎯 Dietary Goals

| Goal | Calories | Protein | Carbs | Fat | Fiber |
|---|---|---|---|---|---|
| Weight Loss | 1500 kcal | 100g | 150g | 55g | 25g |
| Muscle Gain | 2500 kcal | 160g | 280g | 80g | 30g |
| Maintenance | 2000 kcal | 120g | 220g | 65g | 28g |
| Heart Health | 1800 kcal | 110g | 200g | 60g | 35g |
| Custom | user-defined | — | — | — | — |
