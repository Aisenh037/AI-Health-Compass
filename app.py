import re
import time
import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configure Gemini API
genai.configure(api_key=os.environ.get('GEMINI_API_KEY', 'AIzaSyAdN1HbMsPUR4bGNyyowFeVSY550S2515I'))

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def classify_need(user_input):
    """
    Mock classification using regex patterns to categorize the user's need.
    """
    print(f"Classifying user input: '{user_input}'")
    time.sleep(2)  # Simulate processing time

    lower_input = user_input.lower()

    if re.search(r'\b(tooth|teeth|dental|gums|cavity|root canal|dentist)\b', lower_input):
        return 'Dental'
    if re.search(r'\b(stress|anxiety|anxious|stressed|depressed|sad|mental|therapy|counseling|depression|panic)\b', lower_input):
        return 'Mental Health'
    if re.search(r'\b(eye|vision|glasses|blurry|contact lens|optometrist|sight)\b', lower_input):
        return 'Vision'
    if re.search(r'\b(doctor|fever|cold|flu|checkup|sick|general practitioner|gp)\b', lower_input):
        return 'OPD'
    if re.search(r'\b(diet|nutrition|food|eat|weight|obesity|calories)\b', lower_input):
        return 'Nutrition'
    if re.search(r'\b(gym|fitness|exercise|workout|running|swimming|health club)\b', lower_input):
        return 'Fitness'
    if re.search(r'\b(diabetes|hypertension|chronic|heart disease|asthma|arthritis)\b', lower_input):
        return 'Chronic Diseases'
    if re.search(r'\b(pregnancy|maternity|prenatal|gynecology|women|female)\b', lower_input):
        return "Women's Health"
    if re.search(r'\b(prostate|men|male|testosterone)\b', lower_input):
        return "Men's Health"
    if re.search(r'\b(child|kid|baby|pediatric|infant|vaccination)\b', lower_input):
        return 'Pediatrics'
    if re.search(r'\b(elderly|senior|aging|geriatric|osteoporosis)\b', lower_input):
        return 'Geriatrics'
    if re.search(r'\b(emergency|accident|urgent|ambulance|hospital)\b', lower_input):
        return 'Emergency Care'

    # Fallback
    return 'Unknown'

def generate_action_plan(benefit_title):
    """
    Mock action plan generation based on benefit title.
    """
    print(f"Generating action plan for: '{benefit_title}'")
    time.sleep(1.5)  # Simulate processing time

    plans = {
        'Comprehensive Dental Care': [
            'Find a network dentist on the company portal.',
            'Schedule an appointment and mention your insurance plan.',
            'The clinic will handle direct billing for covered services.'
        ],
        'Therapy & Counseling': [
            'Visit the employee wellness portal to see our therapy partners.',
            'Request a session directly through the portal.',
            'Your first 10 sessions are fully covered automatically.'
        ],
        'Annual Eye Exam': [
            'Locate an in-network optometrist using our provider search tool.',
            'Book your annual exam.',
            'Present your employee ID at the appointment for 100% coverage.'
        ],
        'General Physician Consultation': [
            'Use our telehealth app to book a virtual appointment.',
            'Consult with the doctor online.',
            'Submit the digital receipt on the portal for reimbursement.'
        ]
    }

    return plans.get(benefit_title, [
        'Log in to the main benefits portal.',
        'Search for this specific benefit to see the providers.',
        'Follow the instructions listed on the provider\'s page.'
    ])

def generate_action_plan_ai(benefit_title):
    """
    Generate action plan for a benefit using Gemini AI.
    """
    print(f"Generating AI action plan for: '{benefit_title}'")

    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Generate a simple 3-step action plan for an employee to avail the '{benefit_title}' benefit.
    Return it as a JSON array of strings, like:
    ["Step 1: ...", "Step 2: ...", "Step 3: ..."]

    Only return the JSON array, no other text.
    """

    try:
        response = model.generate_content(prompt)
        import json
        plan = json.loads(response.text.strip())
        return plan
    except Exception as e:
        print(f"Error generating action plan: {e}")
        # Fallback to mock
        return generate_action_plan(benefit_title)

def generate_benefits(category):
    """
    Generate employee benefits for a given category using Gemini AI.
    """
    print(f"Generating benefits for category: '{category}'")

    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Generate 3-5 employee health benefits for the category '{category}'.
    Each benefit should have:
    - title: a string title
    - coverage: a string describing coverage (e.g., '100% coverage', 'Up to $500')
    - description: a brief description

    Return the result as a JSON array of objects, like:
    [
        {{
            "title": "Benefit Title",
            "coverage": "Coverage details",
            "description": "Description here"
        }},
        ...
    ]

    Only return the JSON array, no other text.
    """

    try:
        response = model.generate_content(prompt)
        # Parse the JSON response
        import json
        benefits = json.loads(response.text.strip())
        # Add id to each benefit
        for i, benefit in enumerate(benefits):
            benefit['id'] = f"{category.lower().replace(' ', '')}{i+1}"
        return benefits
    except Exception as e:
        print(f"Error generating benefits: {e}")
        # Fallback to static if AI fails
        return [
            {
                "id": f"{category.lower().replace(' ', '')}1",
                "title": f"Sample {category} Benefit",
                "coverage": "Varies",
                "description": f"A benefit related to {category}."
            }
        ]

@app.route('/classify', methods=['POST'])
def classify():
    data = request.get_json()
    user_input = data.get('input', '')
    category = classify_need(user_input)
    return jsonify({'category': category})

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    data = request.get_json()
    benefit_title = data.get('benefit_title', '')
    plan = generate_action_plan_ai(benefit_title)
    return jsonify({'plan': plan})

@app.route('/benefits/<category>', methods=['GET'])
def get_benefits(category):
    benefits = generate_benefits(category)
    return jsonify(benefits)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
