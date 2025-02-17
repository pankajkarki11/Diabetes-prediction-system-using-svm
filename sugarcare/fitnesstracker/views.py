from django.shortcuts import render, redirect
from .models import DailyData
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from datetime import date as datetime_date  # Avoid naming conflict
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for rendering graphs
from .forms import FoodInputForm, RiskAssessmentForm
import requests
from .utils import calculate_risk

API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
API_KEY = "v71WYXr7EngKrANIcH02XIbKFALF4eNmRJyT0ndE"
EXERCISE_DATA = {
    "Running": 10,  # calories burned per minute
    "Cycling": 8,
    "Swimming": 7,
    "Walking": 5,
}

def food_nutrition_view(request):
    nutrients = None
    exercises = None

    if request.method == "POST":
        form = FoodInputForm(request.POST)
        if form.is_valid():
            food_name = form.cleaned_data["food_name"]
            
            # Fetch nutrient data from API
            params = {"query": food_name, "api_key": API_KEY}
            response = requests.get(API_URL, params=params)

            if response.status_code == 200:
                data = response.json()
                if data["foods"]:
                    food_data = data["foods"][0]
                    calories = food_data["foodNutrients"][3]["value"]
                    protein = food_data["foodNutrients"][0]["value"]
                    sugar = food_data["foodNutrients"][1]["value"]
                    fat = food_data["foodNutrients"][2]["value"]

                    nutrients = {
                        "Food Name": food_data["description"],
                        "Calories": calories,
                        "Protein": protein,
                        "Sugar": sugar,
                        "Fat": fat,
                    }

                    # Recommend exercises
                    exercises = {
                        exercise: round(calories / rate, 2) for exercise, rate in EXERCISE_DATA.items()
                    }
    else:
        form = FoodInputForm()

    return render(request, "food_nutrition.html", {"form": form, "nutrients": nutrients, "exercises": exercises})


@login_required
def track_activity(request):
    # Get today's date
    today = datetime_date.today()

    # Fetch the latest data for the logged-in user, if available
    latest_data = DailyData.objects.filter(user=request.user).order_by('-date').first()

    # Set default values
    default_steps = latest_data.steps if latest_data else 0
    default_calories_burned = latest_data.calories_burned if latest_data else 0.0
    default_calories_intake = latest_data.calories_intake if latest_data else 0.0

    if request.method == "POST":
        # Retrieve data from the form
        date = request.POST.get('date', today)
        steps = int(request.POST.get('steps', default_steps))
        calories_burned = float(request.POST.get('calories_burned', default_calories_burned))
        calories_intake = float(request.POST.get('calories_intake', default_calories_intake))

        # Update or create the record in the database
        DailyData.objects.update_or_create(
            user=request.user, 
            date=date,
            defaults={
                'steps': steps,
                'calories_burned': calories_burned,
                'calories_intake': calories_intake,
            }
        )
        # Redirect to avoid duplicate form submissions
        return redirect('dashboard')

    # Retrieve data for the logged-in user
    data = DailyData.objects.filter(user=request.user).order_by('date')

    # Extract data for graphs
    dates = [entry.date.strftime('%Y-%m-%d') for entry in data]
    steps_data = [entry.steps for entry in data]
    calories_burned_data = [entry.calories_burned for entry in data]
    calories_intake_data = [entry.calories_intake for entry in data]

    # Generate graphs
    steps_graph_url = create_graph(dates, steps_data, "Steps Over Time", "Date", "Steps")
    calories_burned_graph_url = create_graph(dates, calories_burned_data, "Calories Burned Over Time", "Date", "Calories Burned")
    calories_intake_graph_url = create_graph(dates, calories_intake_data, "Calories Intake Over Time", "Date", "Calories Intake")

    # Render the template with graphs and default values
    return render(request, 'dashboard.html', {
        'steps_graph_url': steps_graph_url,
        'calories_burned_graph_url': calories_burned_graph_url,
        'calories_intake_graph_url': calories_intake_graph_url,
        'today': today,
        'default_steps': default_steps,
        'default_calories_burned': default_calories_burned,
        'default_calories_intake': default_calories_intake,
    })

def create_graph(dates, data, title, xlabel, ylabel):
    # Create a new figure
    plt.figure(figsize=(8, 6))

    # Plot the data
    plt.plot(dates, data, marker='o', linestyle='-', color='b')

    # Set titles and labels
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Add grid
    plt.grid(True)

    # Rotate x-axis labels for better visibility
    plt.xticks(rotation=45)

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Encode the image to base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Close the plot to free up memory
    plt.close()

    return image_base64


def risk_calculator_view(request):
    if request.method == 'POST':
        form = RiskAssessmentForm(request.POST)
        if form.is_valid():
            # Extract form data
            age = form.cleaned_data['age']
            bmi = form.cleaned_data['bmi']
            family_history = form.cleaned_data['family_history']
            physical_activity = form.cleaned_data['physical_activity']
            smoking = form.cleaned_data['smoking']
            alcohol_consumption = form.cleaned_data['alcohol_consumption']

            # Calculate risk
            risk_score = calculate_risk(age, bmi, family_history, physical_activity, smoking, alcohol_consumption)

            # Save to database (optional)
            risk_assessment = form.save(commit=False)
            risk_assessment.risk_score = risk_score
            risk_assessment.save()

            return render(request, 'risk_calculator_result.html', {'risk_score': risk_score})

    else:
        form = RiskAssessmentForm()

    return render(request, 'risk_calculator.html', {'form': form})



