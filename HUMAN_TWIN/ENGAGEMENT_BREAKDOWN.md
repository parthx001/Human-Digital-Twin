# Engagement Breakdown Feature

## What's New

The Human Digital Twin frontend now includes a **Student Engagement Breakdown** section that displays engagement metrics across four key categories:

### Engagement Categories

1. **Attendance** - Direct percentage of classes attended (0-100%)
   - Your input value is displayed
   - Green: 75%+ | Orange: 50-75% | Red: <50%

2. **Assignments** - Assignment submission rate (0-100%)
   - Calculated as: (assignments/week ÷ 14) × 100
   - 14 is the assumed maximum assignments per week
   - Green: 75%+ | Orange: 50-75% | Red: <50%

3. **Sleep Quality** - Sleep health indicator (0-100%)
   - Calculated as: (hours/night ÷ 8) × 100
   - 8 hours is considered ideal
   - Green: 75%+ | Orange: 50-75% | Red: <50%

4. **Academic Performance** - CGPA-based metric (0-100%)
   - Calculated as: (CGPA ÷ 10) × 100
   - Higher CGPA = higher engagement in academics
   - Green: 75%+ | Orange: 50-75% | Red: <50%

5. **Overall Engagement** - Average of all categories
   - Combined indicator of total student engagement
   - Color-coded same as individual categories

## Visual Design

Each category displays:
- **Category name** with description
- **Percentage value** (color-coded)
- **Mini progress bar** showing relative strength
- **Context information** (e.g., "4 per week", "7 hours/night")

## How It Works

1. Adjust the sliders in **Simulation Controls**:
   - Attendance % (0-100)
   - Assignments / week (0-14)
   - Exam gap in days (0-30)
   - Sleep hours (0-12)
   - CGPA (0-10)

2. Click **"Run AI Simulation"**

3. The **Engagement Breakdown** section updates with:
   - Individual engagement scores for each category
   - Color-coded performance indicators (green/orange/red)
   - Progress bars
   - Overall engagement average

## Color Coding

- 🟢 **Green (75-100%)** - Excellent engagement in this category
- 🟡 **Orange (50-75%)** - Moderate engagement, room for improvement
- 🔴 **Red (<50%)** - Low engagement, needs attention

## Use Cases

- **Students**: Identify which areas of engagement need improvement
- **Advisors**: Understand student engagement patterns at a glance
- **Policy Makers**: See how different policies affect overall engagement
- **Institutions**: Track population-wide engagement metrics

## Technical Details

The engagement scores are calculated from the simulation inputs using normalized formulas:

```
Attendance Score = input_attendance (0-100)
Assignment Score = min(100, (assignments / 14) * 100)
Sleep Score = min(100, (sleep / 8) * 100)
Academic Score = (cgpa / 10) * 100
Overall = (Attendance + Assignments + Sleep + Academic) / 4
```

The breakdown updates in real-time when you run new simulations, and colors update dynamically based on the scores.
