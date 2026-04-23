from model import Student

def create_population_from_data(df):

    students = []

    for _, row in df.iterrows():

        if row["stress_proxy"] < 0.3:
            resilience = 0.8
        elif row["stress_proxy"] < 0.6:
            resilience = 0.5
        else:
            resilience = 0.2

        s = Student(resilience)

        s.stress = row["stress_proxy"]
        s.motivation = row["engagement_norm"]
        s.learning = row["grade_norm"]

        students.append(s)

    return students


def simulate(students, weeks=16, policy_pressure=1.0):

    stress_history = []
    learning_history = []
    motivation_history = []

    for week in range(weeks):

        active_students = [s for s in students if not s.dropped_out]

        if len(active_students) == 0:
            break

        avg_stress = sum(s.stress for s in active_students) / len(active_students)

        for s in active_students:
            s.update(policy_pressure, avg_stress)

        stress_history.append(
            sum(s.stress for s in active_students) / len(active_students)
        )

        learning_history.append(
            sum(s.learning for s in active_students) / len(active_students)
        )

        motivation_history.append(
            sum(s.motivation for s in active_students) / len(active_students)
        )

    # Create population data structure
    population = []
    for student in students:
        population.append({
            "stress": student.stress,
            "motivation": student.motivation,
            "learning": student.learning,
            "dropped_out": student.dropped_out,
            "burned_out": student.burned_out
        })

    return stress_history, motivation_history, learning_history, population