import re
import time
import os
import json
import random
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import List, Dict, Any

# Configure Gemini API
genai.configure(api_key=os.environ.get('GEMINI_API_KEY', 'AIzaSyAdN1HbMsPUR4bGNyyowFeVSY550S2515I'))

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Enhanced knowledge base for RAG-like functionality
BENEFITS_KNOWLEDGE_BASE = {
    'Dental': [
        {
            'title': 'Comprehensive Dental Care',
            'coverage': '100% coverage for preventive care, 80% for major procedures',
            'description': 'Complete dental coverage including cleanings, fillings, crowns, and orthodontics. Includes access to a network of 50,000+ dentists nationwide.',
            'tags': ['preventive', 'major procedures', 'orthodontics', 'network dentists'],
            'eligibility': 'All employees and dependents',
            'annual_limit': '$2,500 per person'
        },
        {
            'title': 'Dental Implants & Surgery',
            'coverage': '70% coverage up to $3,000',
            'description': 'Advanced dental procedures including implants, oral surgery, and periodontal treatments. Includes pre-authorization for complex procedures.',
            'tags': ['implants', 'oral surgery', 'periodontal', 'advanced procedures'],
            'eligibility': 'Employees with 6+ months tenure',
            'annual_limit': '$3,000 per person'
        },
        {
            'title': 'Orthodontic Coverage',
            'coverage': '50% coverage for braces and aligners',
            'description': 'Coverage for traditional braces, Invisalign, and other orthodontic treatments. Includes consultation and treatment planning.',
            'tags': ['braces', 'invisalign', 'orthodontics', 'teeth straightening'],
            'eligibility': 'Employees and children under 19',
            'annual_limit': '$2,000 per person'
        },
        {
            'title': 'Emergency Dental Care',
            'coverage': '100% coverage for emergency procedures',
            'description': '24/7 emergency dental coverage for pain relief, infection treatment, and trauma care. Includes after-hours hotline.',
            'tags': ['emergency', 'pain relief', 'infection', 'trauma', '24/7'],
            'eligibility': 'All employees and dependents',
            'annual_limit': 'No annual limit for emergencies'
        }
    ],
    'Mental Health': [
        {
            'title': 'Therapy & Counseling Services',
            'coverage': '100% coverage for up to 20 sessions',
            'description': 'Access to licensed therapists and counselors through our mental health network. Includes CBT, DBT, and specialized therapies.',
            'tags': ['therapy', 'counseling', 'CBT', 'DBT', 'licensed therapists'],
            'eligibility': 'All employees and dependents',
            'annual_limit': '20 sessions per person'
        },
        {
            'title': 'Crisis Intervention & Support',
            'coverage': '100% coverage, 24/7 access',
            'description': 'Immediate crisis support through hotline and online chat. Includes suicide prevention and emergency mental health services.',
            'tags': ['crisis', 'hotline', 'suicide prevention', '24/7', 'emergency'],
            'eligibility': 'All employees and dependents',
            'annual_limit': 'Unlimited for crisis situations'
        },
        {
            'title': 'Wellness & Mindfulness Programs',
            'coverage': 'Fully covered wellness programs',
            'description': 'Access to meditation apps, yoga classes, stress management workshops, and mindfulness training programs.',
            'tags': ['wellness', 'meditation', 'yoga', 'stress management', 'mindfulness'],
            'eligibility': 'All employees',
            'annual_limit': 'Unlimited access to programs'
        },
        {
            'title': 'Psychiatric Care',
            'coverage': '80% coverage for psychiatric services',
            'description': 'Coverage for psychiatrist visits, medication management, and psychiatric evaluations. Includes access to specialists.',
            'tags': ['psychiatry', 'medication', 'specialists', 'evaluation'],
            'eligibility': 'All employees and dependents',
            'annual_limit': '$1,500 per person'
        }
    ],
    'Vision': [
        {
            'title': 'Comprehensive Eye Exams',
            'coverage': '100% coverage annually',
            'description': 'Annual comprehensive eye examinations including vision testing, glaucoma screening, and retinal imaging.',
            'tags': ['eye exam', 'vision testing', 'glaucoma', 'retinal imaging'],
            'eligibility': 'All employees and dependents',
            'annual_limit': '1 exam per person per year'
        },
        {
            'title': 'Prescription Eyewear',
            'coverage': 'Up to $300 for frames and lenses',
            'description': 'Coverage for prescription glasses and contact lenses. Includes designer frames and premium lens options.',
            'tags': ['glasses', 'contacts', 'prescription', 'frames', 'lenses'],
            'eligibility': 'All employees and dependents',
            'annual_limit': '$300 per person every 2 years'
        },
        {
            'title': 'Laser Vision Correction',
            'coverage': 'Up to $2,500 coverage',
            'description': 'Coverage for LASIK and other laser vision correction procedures. Includes pre-operative and post-operative care.',
            'tags': ['lasik', 'laser correction', 'vision surgery', 'pre-op', 'post-op'],
            'eligibility': 'Employees with 2+ years tenure',
            'annual_limit': '$2,500 per person lifetime'
        }
    ],
    'OPD': [
        {
            'title': 'Primary Care Physician Visits',
            'coverage': '100% coverage for office visits',
            'description': 'Regular check-ups and consultations with primary care physicians. Includes preventive care and chronic condition management.',
            'tags': ['primary care', 'check-ups', 'preventive care', 'chronic conditions'],
            'eligibility': 'All employees and dependents',
            'annual_limit': 'Unlimited office visits'
        },
        {
            'title': 'Specialist Consultations',
            'coverage': '80% coverage for specialist visits',
            'description': 'Access to specialists including cardiologists, dermatologists, and gastroenterologists. Requires referral from primary care.',
            'tags': ['specialists', 'cardiologist', 'dermatologist', 'gastroenterologist', 'referral'],
            'eligibility': 'All employees and dependents',
            'annual_limit': '$2,000 per person'
        },
        {
            'title': 'Diagnostic Services',
            'coverage': '90% coverage for lab work and imaging',
            'description': 'Coverage for blood tests, X-rays, MRIs, CT scans, and other diagnostic procedures ordered by physicians.',
            'tags': ['lab work', 'x-rays', 'MRI', 'CT scan', 'diagnostics'],
            'eligibility': 'All employees and dependents',
            'annual_limit': '$1,500 per person'
        }
    ],
    'Nutrition': [
        {
            'title': 'Nutrition Counseling',
            'coverage': '100% coverage for 6 sessions',
            'description': 'One-on-one nutrition counseling with registered dietitians. Includes personalized meal planning and dietary guidance.',
            'tags': ['dietitian', 'meal planning', 'dietary guidance', 'counseling'],
            'eligibility': 'All employees and dependents',
            'annual_limit': '6 sessions per person'
        },
        {
            'title': 'Weight Management Programs',
            'coverage': 'Fully covered programs',
            'description': 'Access to weight loss programs, bariatric surgery consultations, and obesity management support.',
            'tags': ['weight loss', 'bariatric', 'obesity', 'management'],
            'eligibility': 'Employees with BMI over 30',
            'annual_limit': 'Program access included'
        },
        {
            'title': 'Healthy Eating Resources',
            'coverage': 'Fully covered educational resources',
            'description': 'Access to nutrition education, cooking classes, and healthy eating workshops. Includes meal delivery discounts.',
            'tags': ['education', 'cooking classes', 'workshops', 'meal delivery'],
            'eligibility': 'All employees',
            'annual_limit': 'Unlimited access to resources'
        }
    ],
    'Fitness': [
        {
            'title': 'Gym Membership Reimbursement',
            'coverage': 'Up to $50/month reimbursement',
            'description': 'Monthly reimbursement for gym memberships at participating fitness centers nationwide.',
            'tags': ['gym', 'membership', 'reimbursement', 'fitness centers'],
            'eligibility': 'All employees',
            'annual_limit': '$600 per person'
        },
        {
            'title': 'Personal Training Sessions',
            'coverage': 'Up to $100 per session',
            'description': 'Coverage for personal training sessions with certified trainers. Includes fitness assessments and program design.',
            'tags': ['personal training', 'certified trainers', 'fitness assessment'],
            'eligibility': 'All employees',
            'annual_limit': '$1,200 per person'
        },
        {
            'title': 'Wellness Challenges & Programs',
            'coverage': 'Fully covered participation',
            'description': 'Access to company wellness challenges, fitness classes, and virtual workout programs.',
            'tags': ['wellness challenges', 'fitness classes', 'virtual workouts'],
            'eligibility': 'All employees',
            'annual_limit': 'Unlimited participation'
        }
    ],
    'Chronic Diseases': [
        {
            'title': 'Diabetes Management Program',
            'coverage': '100% coverage for diabetes supplies and education',
            'description': 'Comprehensive diabetes care including glucose monitors, insulin pumps, and diabetes education programs.',
            'tags': ['diabetes', 'glucose monitors', 'insulin', 'education'],
            'eligibility': 'Employees diagnosed with diabetes',
            'annual_limit': '$3,000 for supplies'
        },
        {
            'title': 'Cardiovascular Disease Management',
            'coverage': '90% coverage for cardiac care',
            'description': 'Specialized care for heart conditions including cardiology consultations, cardiac rehabilitation, and preventive screenings.',
            'tags': ['cardiac', 'heart conditions', 'rehabilitation', 'screenings'],
            'eligibility': 'Employees with cardiac conditions',
            'annual_limit': '$5,000 per person'
        },
        {
            'title': 'Chronic Condition Monitoring',
            'coverage': '80% coverage for ongoing care',
            'description': 'Regular monitoring and management of chronic conditions including asthma, hypertension, and arthritis.',
            'tags': ['monitoring', 'asthma', 'hypertension', 'arthritis'],
            'eligibility': 'All employees with chronic conditions',
            'annual_limit': '$2,500 per person'
        }
    ],
    "Women's Health": [
        {
            'title': 'Maternity & Prenatal Care',
            'coverage': '100% coverage for prenatal care',
            'description': 'Comprehensive maternity care including prenatal visits, ultrasounds, and delivery. Includes parental leave support.',
            'tags': ['maternity', 'prenatal', 'ultrasounds', 'delivery', 'parental leave'],
            'eligibility': 'All female employees',
            'annual_limit': 'Covered through delivery'
        },
        {
            'title': 'Gynecological Services',
            'coverage': '100% coverage for annual exams',
            'description': 'Annual gynecological examinations, Pap smears, mammograms, and preventive women\'s health screenings.',
            'tags': ['gynecology', 'pap smear', 'mammogram', 'screenings'],
            'eligibility': 'All female employees and dependents',
            'annual_limit': '1 exam per year'
        },
        {
            'title': 'Fertility Support',
            'coverage': 'Up to $10,000 coverage',
            'description': 'Coverage for fertility treatments, IVF consultations, and reproductive health services.',
            'tags': ['fertility', 'IVF', 'reproductive health'],
            'eligibility': 'Employees with infertility diagnosis',
            'annual_limit': '$10,000 per person'
        }
    ],
    "Men's Health": [
        {
            'title': 'Prostate Health Screening',
            'coverage': '100% coverage for annual screenings',
            'description': 'Annual prostate exams, PSA testing, and prostate cancer screenings for men over 50.',
            'tags': ['prostate', 'PSA testing', 'cancer screening'],
            'eligibility': 'Male employees over 50',
            'annual_limit': '1 screening per year'
        },
        {
            'title': 'Testosterone & Hormone Therapy',
            'coverage': '80% coverage for hormone treatments',
            'description': 'Coverage for hormone testing, testosterone replacement therapy, and male hormone management.',
            'tags': ['testosterone', 'hormone therapy', 'male hormones'],
            'eligibility': 'Employees with hormone deficiencies',
            'annual_limit': '$1,500 per person'
        },
        {
            'title': 'Men\'s Preventive Care',
            'coverage': '100% coverage for annual physicals',
            'description': 'Comprehensive annual physical examinations tailored for men, including cardiovascular and cancer screenings.',
            'tags': ['preventive care', 'physicals', 'cardiovascular', 'cancer screening'],
            'eligibility': 'All male employees',
            'annual_limit': '1 physical per year'
        }
    ],
    'Pediatrics': [
        {
            'title': 'Well-Child Visits',
            'coverage': '100% coverage for preventive visits',
            'description': 'Regular well-child check-ups, vaccinations, and developmental screenings from birth through adolescence.',
            'tags': ['well-child', 'vaccinations', 'developmental screening'],
            'eligibility': 'All children dependents',
            'annual_limit': 'Unlimited preventive visits'
        },
        {
            'title': 'Pediatric Specialist Care',
            'coverage': '90% coverage for specialist visits',
            'description': 'Access to pediatric specialists including allergists, endocrinologists, and developmental pediatricians.',
            'tags': ['pediatric specialists', 'allergists', 'endocrinologists'],
            'eligibility': 'All children dependents',
            'annual_limit': '$2,000 per child'
        },
        {
            'title': 'Vision & Dental for Children',
            'coverage': '100% coverage for children\'s eye and dental care',
            'description': 'Comprehensive vision and dental care for children including exams, glasses, and orthodontic services.',
            'tags': ['children', 'vision', 'dental', 'orthodontic'],
            'eligibility': 'All children dependents',
            'annual_limit': '$1,000 per child'
        }
    ],
    'Geriatrics': [
        {
            'title': 'Senior Wellness Programs',
            'coverage': 'Fully covered wellness programs',
            'description': 'Age-appropriate wellness programs including fall prevention, memory enhancement, and senior fitness classes.',
            'tags': ['senior', 'wellness', 'fall prevention', 'memory', 'fitness'],
            'eligibility': 'Employees and dependents over 65',
            'annual_limit': 'Unlimited program access'
        },
        {
            'title': 'Geriatric Specialist Care',
            'coverage': '90% coverage for geriatric consultations',
            'description': 'Specialized care for aging-related conditions including osteoporosis, cognitive impairment, and polypharmacy management.',
            'tags': ['geriatric', 'osteoporosis', 'cognitive', 'polypharmacy'],
            'eligibility': 'Employees and dependents over 65',
            'annual_limit': '$2,500 per person'
        },
        {
            'title': 'Home Health Services',
            'coverage': '80% coverage for in-home care',
            'description': 'Coverage for home health services including nursing visits, physical therapy, and home safety assessments.',
            'tags': ['home health', 'nursing', 'physical therapy', 'home safety'],
            'eligibility': 'Employees and dependents over 65',
            'annual_limit': '$3,000 per person'
        }
    ],
    'Emergency Care': [
        {
            'title': 'Emergency Room Coverage',
            'coverage': '90% coverage for emergency visits',
            'description': 'Coverage for emergency room visits and urgent care center visits. Includes ambulance transportation.',
            'tags': ['emergency room', 'urgent care', 'ambulance'],
            'eligibility': 'All employees and dependents',
            'annual_limit': '$5,000 per person'
        },
        {
            'title': '24/7 Nurse Hotline',
            'coverage': 'Fully covered telehealth support',
            'description': 'Access to registered nurses 24/7 for medical advice, triage, and guidance on when to seek emergency care.',
            'tags': ['nurse hotline', 'telehealth', 'triage', '24/7'],
            'eligibility': 'All employees and dependents',
            'annual_limit': 'Unlimited calls'
        },
        {
            'title': 'International Emergency Coverage',
            'coverage': '80% coverage for overseas emergencies',
            'description': 'Emergency medical coverage while traveling internationally. Includes medical evacuation and repatriation.',
            'tags': ['international', 'travel', 'evacuation', 'repatriation'],
            'eligibility': 'All employees and dependents',
            'annual_limit': '$100,000 per incident'
        }
    ]
}

# Enhanced in-memory cache for generated benefits
benefits_cache = {}

def classify_need(user_input: str) -> str:
    """
    Enhanced AI classification using Gemini with better context and validation.
    """
    print(f"Classifying user input with AI: '{user_input}'")

    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Classify the following user health input into one of these categories:
    - Dental (teeth, mouth, dentist, orthodontics)
    - Mental Health (therapy, counseling, depression, anxiety, stress)
    - Vision (eyes, glasses, contacts, eye exam, lasik)
    - OPD (general physician, check-up, consultation, primary care)
    - Nutrition (diet, weight, food, dietitian, healthy eating)
    - Fitness (gym, exercise, workout, personal training, wellness)
    - Chronic Diseases (diabetes, heart disease, asthma, hypertension, arthritis)
    - Women's Health (maternity, pregnancy, gynecology, fertility, mammogram)
    - Men's Health (prostate, testosterone, male health screening)
    - Pediatrics (children, baby, infant, pediatrician, vaccinations)
    - Geriatrics (senior, elderly, aging, geriatric care)
    - Emergency Care (accident, injury, urgent care, emergency room)

    User input: "{user_input}"

    Analyze the input carefully and return ONLY the most appropriate category name. Consider synonyms and related terms.
    """

    try:
        response = model.generate_content(prompt)
        category = response.text.strip()

        # Enhanced validation with better matching
        valid_categories = ['Dental', 'Mental Health', 'Vision', 'OPD', 'Nutrition', 'Fitness',
                          'Chronic Diseases', "Women's Health", "Men's Health", 'Pediatrics',
                          'Geriatrics', 'Emergency Care']

        # Try exact match first
        if category in valid_categories:
            return category

        # Try case-insensitive match
        for valid_cat in valid_categories:
            if category.lower() == valid_cat.lower():
                return valid_cat

        # Try partial match
        for valid_cat in valid_categories:
            if valid_cat.lower() in category.lower() or category.lower() in valid_cat.lower():
                return valid_cat

        print(f"Classification failed, using fallback for: {category}")
        return 'OPD'  # Default fallback

    except Exception as e:
        print(f"Error classifying: {e}")
        return 'OPD'  # Default fallback

def search_knowledge_base(query: str, category: str) -> List[Dict[str, Any]]:
    """
    RAG-like search through the knowledge base for relevant benefits.
    """
    if category not in BENEFITS_KNOWLEDGE_BASE:
        return []

    benefits = BENEFITS_KNOWLEDGE_BASE[category]
    query_lower = query.lower()

    # Score benefits based on relevance to the query
    scored_benefits = []
    for benefit in benefits:
        score = 0

        # Title relevance
        if query_lower in benefit['title'].lower():
            score += 10

        # Tag relevance
        for tag in benefit['tags']:
            if tag.lower() in query_lower or query_lower in tag.lower():
                score += 5

        # Description relevance
        if query_lower in benefit['description'].lower():
            score += 3

        if score > 0:
            scored_benefits.append((benefit, score))

    # Sort by relevance score and return top matches
    scored_benefits.sort(key=lambda x: x[1], reverse=True)
    return [benefit for benefit, score in scored_benefits[:6]]  # Return top 6

def generate_benefits_enhanced(category: str, user_query: str = "", seed: int = None) -> List[Dict[str, Any]]:
    """
    Enhanced benefit generation using RAG approach with knowledge base and AI.
    """
    if seed is None:
        seed = int(time.time() * 1000) % 10000

    print(f"Generating enhanced benefits for category: '{category}' with query: '{user_query}' and seed {seed}")

    # First, try RAG approach with knowledge base
    knowledge_results = search_knowledge_base(user_query, category)

    if knowledge_results:
        print(f"Found {len(knowledge_results)} relevant benefits from knowledge base")
        # Add IDs and return knowledge base results
        for i, benefit in enumerate(knowledge_results):
            benefit['id'] = f"{category.lower().replace(' ', '')}kb{i+1}"
        return knowledge_results

    # Fallback to AI generation if no knowledge base matches
    print("No knowledge base matches, falling back to AI generation")

    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Generate 4-6 employee health benefits for the category '{category}'.
    The user query was: "{user_query}"
    Use seed {seed} for variety.

    Each benefit should include:
    - title: descriptive title
    - coverage: coverage details (e.g., '100% coverage', 'Up to $500')
    - description: detailed description of the benefit
    - tags: array of relevant keywords
    - eligibility: who can use this benefit
    - annual_limit: any limits on the benefit

    Return as JSON array of objects.
    """

    try:
        response = model.generate_content(prompt)
        benefits = json.loads(response.text.strip())

        # Add IDs
        for i, benefit in enumerate(benefits):
            benefit['id'] = f"{category.lower().replace(' ', '')}ai{i+1}"

        return benefits

    except Exception as e:
        print(f"Error generating benefits: {e}")
        # Final fallback to static data
        return [
            {
                "id": f"{category.lower().replace(' ', '')}fallback1",
                "title": f"Comprehensive {category} Coverage",
                "coverage": "Varies by service",
                "description": f"Access to {category.lower()} services and treatments through our provider network.",
                "tags": [category.lower()],
                "eligibility": "All employees and dependents",
                "annual_limit": "Based on plan terms"
            }
        ]

def generate_action_plan_ai_enhanced(benefit_title: str, benefit_data: Dict[str, Any] = None) -> List[str]:
    """
    Enhanced action plan generation with benefit context.
    """
    print(f"Generating enhanced action plan for: '{benefit_title}'")

    context_info = ""
    if benefit_data:
        context_info = f"""
        Benefit Details:
        - Coverage: {benefit_data.get('coverage', 'N/A')}
        - Eligibility: {benefit_data.get('eligibility', 'N/A')}
        - Annual Limit: {benefit_data.get('annual_limit', 'N/A')}
        """

    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Generate a detailed 3-4 step action plan for an employee to access the '{benefit_title}' benefit.

    {context_info}

    Make the steps specific and actionable. Consider:
    - How to find providers
    - What documentation is needed
    - How billing/claims work
    - Any pre-authorization requirements

    Return as JSON array of strings, each step clearly numbered.
    """

    try:
        response = model.generate_content(prompt)
        plan = json.loads(response.text.strip())
        return plan
    except Exception as e:
        print(f"Error generating action plan: {e}")
        # Enhanced fallback
        return [
            f"Visit the employee benefits portal and search for '{benefit_title}'",
            "Review the provider network and select a participating provider",
            "Contact the provider to schedule your appointment",
            "Present your employee ID and follow the provider's instructions for billing"
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
    benefit_data = data.get('benefit_data', {})
    plan = generate_action_plan_ai_enhanced(benefit_title, benefit_data)
    return jsonify({'plan': plan})

@app.route('/benefits/<category>', methods=['GET'])
def get_benefits(category):
    user_query = request.args.get('query', '')

    cache_key = f"{category}:{user_query}"
    if cache_key in benefits_cache:
        print(f"Using cached benefits for {cache_key}")
        return jsonify(benefits_cache[cache_key])

    benefits = generate_benefits_enhanced(category, user_query)
    benefits_cache[cache_key] = benefits
    return jsonify(benefits)

@app.route('/benefits/<category>/regenerate', methods=['POST'])
def regenerate_benefits(category):
    data = request.get_json() or {}
    user_query = data.get('query', '')

    benefits = generate_benefits_enhanced(category, user_query)
    cache_key = f"{category}:{user_query}"
    benefits_cache[cache_key] = benefits
    return jsonify(benefits)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': time.time()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
