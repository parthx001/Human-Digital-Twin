# Sleep Adjustment Prediction Feature

## Overview

The **Sleep Adjustment Prediction** panel shows you what happens if you increase assignments by just 1 per week. It calculates the minimum additional sleep hours needed to maintain your current dropout risk level.

## What It Shows

When you run a simulation, the prediction displays:

```
Sleep Adjustment Prediction
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Current: 4 assignments/week

If +1 assignment: Need 1.5h more sleep

Sleep would rise from 7h to 8.5h/night
```

## How It Works

### The Question It Answers
*"If my assignment workload increases by 1 assignment per week, how much more sleep should I get to avoid increased dropout risk?"*

### The Calculation
1. **Baseline**: Runs simulation with your current parameters
2. **What-If**: Simulates adding 1 assignment to your weekly load
3. **Sleep Search**: Tests increasing sleep from 0 to +5 hours
4. **Finding**: Returns minimum sleep increase to keep dropout risk ≤ baseline

### Example Scenarios

**Scenario 1: Moderate Load**
```
Current: 4 assignments/week, 7h sleep
→ If +1 assignment (5 total):
  Need +1.5h sleep
→ New requirement: 8.5h/night
```

**Scenario 2: Heavy Load**
```
Current: 10 assignments/week, 8h sleep
→ If +1 assignment (11 total):
  Need +2h sleep
→ New requirement: 10h/night (capped at system max)
```

**Scenario 3: Light Load**
```
Current: 2 assignments/week, 7h sleep
→ If +1 assignment (3 total):
  Need +0.5h sleep
→ New requirement: 7.5h/night
```

## When It Appears

The prediction box shows when:
- You've successfully run a simulation
- The backend calculated that additional sleep is needed (`sleep_increase > 0`)

It hides when:
- No simulation has run yet
- The backend found no additional sleep needed

## Use Cases

### For Students
- **Planning**: Cut/add assignments strategically
- **Sleep optimization**: Know exact sleep requirements for stress management
- **Decision making**: See the cost of taking on more courses/work

### For Advisors
- **Course planning**: Show curriculum impact on sleep/stress
- **Interventions**: "You need 1.5h more sleep if we add this course"
- **Workload balancing**: Evidence-based assignment distribution

### For Institutions
- **Policy evaluation**: See policy impact on required student sleep
- **Fairness analysis**: Ensure workload distribution is sustainable
- **Health monitoring**: Track if policies violate healthy sleep recommendations

## What The Data Means

- **Current assignments**: Your simulated weekly assignment count
- **Sleep increase needed**: Extra hours of sleep to offset +1 assignment
- **Sleep would rise from X to Y**: Visual summary of the change

## Technical Details

### Backend Implementation
Implemented in `model.py` function `recommend_sleep_adjustment()`:

```python
def recommend_sleep_adjustment(data: SimulationInput):
    """
    If assignments increase by 1, 
    find minimum sleep increase to maintain dropout risk
    """
    # Test adding 1-5 hours of sleep
    # Return when dropout risk no longer increases
```

### API Response Fields
```json
{
  "stress": 45.2,
  "engagement": 72.5,
  "risk_prob": 18,
  "risk_level": "Low",
  "recommended_sleep": 8.5,
  "sleep_increase": 1.5
}
```

### Frontend Display
JavaScript function updates the UI with:
- Current assignments
- Sleep increase needed
- New recommended sleep total

## Important Notes

⚠️ **This is a predictive model**, not actual medical advice:
- Based on normalized scoring, not clinical sleep science
- Real students vary in sleep needs
- Should be combined with other factors (health, stress, workload)

✅ **Useful for**:
- Relative comparisons ("This policy requires more sleep")
- Evidence-based discussions
- Institutional capacity planning
- Student awareness of workload impacts

## Examples

### Adding 1 Assignment to High Load
```
Before: 11 assignments/week, 8h sleep, 35% dropout risk
After:  12 assignments/week, 8h sleep, 52% dropout risk (BAD!)

Solution: Increase sleep to 9.5h/night
After:    12 assignments/week, 9.5h sleep, 35% dropout risk (OK!)
```

### Increasing Exams or Assignments
```
"If you add one more assignment per week,
you should increase sleep from 7 to 8.5 hours
to maintain your current stress level."
```

This helps counselors and students make informed decisions about course loads and time management.
