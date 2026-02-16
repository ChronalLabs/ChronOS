
def calculate_travel_emission(distance, mode):
    factors = {
        "car": 0.21,
        "bus": 0.10,
        "train": 0.05,
        "flight": 0.25
    }
    return distance * factors.get(mode, 0)


def calculate_electricity_emission(kwh):
    return kwh * 0.82


def calculate_diet_emission(diet_type):
    diet_values = {
        "vegan": 50,
        "vegetarian": 100,
        "nonveg": 200
    }
    return diet_values.get(diet_type, 0)

def calculate_score(total_emission):

    if total_emission < 150:
        return 90, "Low Impact", "🌿 Eco Beginner"
    elif total_emission < 300:
        return 70, "Moderate Impact", "🌳 Green Warrior"
    else:
        return 40, "High Impact", "🌎 Climate Improver"


def calculate_offset(total_emission):

    trees_required = total_emission / 21
    offset_cost_estimate = trees_required * 5

    return round(trees_required, 1), round(offset_cost_estimate, 2)

def generate_recommendations(data, total):

    recommendations = []

    distance = float(data["distance"])
    electricity = float(data["electricity"])
    diet = data["diet"]

    if distance > 300:
        recommendations.append(
            "Consider using public transport, cycling, or carpooling to reduce travel emissions."
        )

    if electricity > 250:
        recommendations.append(
            "Switch to LED bulbs and energy-efficient appliances to reduce electricity usage."
        )

    if diet == "nonveg":
        recommendations.append(
            "Reducing meat consumption can significantly lower your carbon footprint."
        )

    if total > 300:
        recommendations.append(
            "Planting trees or investing in verified carbon offset programs can help neutralize emissions."
        )

    if not recommendations:
        recommendations.append(
            "Excellent work! Your lifestyle is already environmentally responsible."
        )

    return recommendations


def calculate_total(data):

    distance = float(data["distance"])
    electricity_units = float(data["electricity"])
    diet_type = data["diet"]
    travel_mode = data["travel_mode"]

    # Individual calculations
    travel = calculate_travel_emission(distance, travel_mode)
    electricity = calculate_electricity_emission(electricity_units)
    diet = calculate_diet_emission(diet_type)

    total = travel + electricity + diet
    yearly = total * 12

    # Score
    score, category, badge = calculate_score(total)

    # Offset
    trees_required, offset_cost = calculate_offset(total)

    # Recommendations
    recommendations = generate_recommendations(data, total)

    return {
        "travel": round(travel, 2),
        "electricity": round(electricity, 2),
        "diet": round(diet, 2),
        "total": round(total, 2),
        "yearly": round(yearly, 2),
        "score": score,
        "category": category,
        "badge": badge,
        "trees_required": trees_required,
        "offset_cost": offset_cost,
        "recommendations": recommendations
    }
