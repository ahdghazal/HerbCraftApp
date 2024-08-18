from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import spacy

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load SpaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Example symptom-diagnosis database
symptom_diagnosis_db = {
    "stomach pain": "Gastritis",
    "diarrhea": "Gastroenteritis",
    "headache": "Tension Headache",
    "fever": "Viral Infection",
    "cough": "Common Cold",
    "sore throat": "Pharyngitis",
    "back pain": "Muscle Strain",
    "nausea": "Food Poisoning",
    "fatigue": "Anemia",
    "chest pain": "Angina",
    "joint pain": "Arthritis",
    "dizziness": "Vertigo",
    "constipation": "Irritable Bowel Syndrome",
    "runny nose": "Allergic Rhinitis",
    "shortness of breath": "Asthma",
    "rash": "Dermatitis",
    "muscle pain": "Fibromyalgia",
    "insomnia": "Sleep Disorder",
    "anxiety": "Anxiety",
    "indigestion": "Indigestion",
    "inflammation": "Inflammation",
    "high blood pressure": "Hypertension",
    "migraine": "Migraine",
    "motion sickness": "Motion Sickness",
    "digestive disorders": "Digestive Disorders",
    "liver disease": "Liver Disease",
    "depression": "Depression",
    "heart disease": "Heart Disease",
    "high cholesterol": "High Cholesterol",
    "cancer prevention": "Cancer Prevention",
    "skin conditions": "Skin Conditions",
    "adrenal fatigue": "Adrenal Fatigue",
    "bad breath": "Bad Breath",
    "type 2 diabetes": "Type 2 Diabetes",
    "neurodegenerative diseases": "Neurodegenerative Diseases",
    "cognitive decline": "Cognitive Decline",
    "memory loss": "Memory Loss",
    "hair loss": "Hair Loss",
    "stress": "Stress",
    "eczema": "Eczema",
    "psoriasis": "Psoriasis",
    "dry skin": "Dry Skin",
    "oral health": "Oral Health",
    "weight loss": "Weight Loss",
    "burns": "Burns",
    "insect bites": "Insect Bites",
    "bloating": "Bloating",
    "cold sores": "Cold Sores",
    "bronchitis": "Bronchitis",
    "acne": "Acne",
    "menstrual cramps": "Menstrual Cramps",
    "allergies": "Allergies",
    "urinary tract infections": "Urinary Tract Infections",
    "sciatica": "Sciatica",
    "lupus": "Lupus",
    "gout": "Gout",
    "shingles": "Shingles",
    "toothache": "Toothache",
    "yeast infection": "Yeast Infection",
    "hemorrhoids": "Hemorrhoids",
    "warts": "Warts",
    "ringworm": "Ringworm",
    "varicose veins": "Varicose Veins",
    "sinusitis": "Sinusitis",
    "ear infection": "Ear Infection",
    "hangover": "Hangover",
    "cold hands": "Cold Hands",
    "gingivitis": "Gingivitis",
    "ulcer": "Ulcer",
    "spider bites": "Spider Bites",
    "sunburn": "Sunburn",
    "athlete's foot": "Athlete's Foot",
    "itchy scalp": "Itchy Scalp",
    "hives": "Hives",
    "hair thinning": "Hair Thinning",
    "prostatitis": "Prostatitis",
    "bladder infection": "Bladder Infection",
    "chronic fatigue syndrome": "Chronic Fatigue Syndrome",
    "esophagitis": "Esophagitis",
    "laryngitis": "Laryngitis",
    "muscle cramps": "Muscle Cramps",
    "pinworms": "Pinworms",
    "plantar fasciitis": "Plantar Fasciitis",
    "rosacea": "Rosacea",
    "snoring": "Snoring",
    "sore muscles": "Sore Muscles",
    "teething": "Teething",
    "tinnitus": "Tinnitus",
    "trench mouth": "Trench Mouth",
    "wrinkles": "Wrinkles"
}

# Example diagnosis-treatment database
diagnosis_treatment_db = {
    "Gastritis": ["Ginger", "Mint"],
    "Gastroenteritis": ["Chamomile"],
    "Tension Headache": ["Mint"],  # Mint replacing Peppermint
    "Viral Infection": ["Thyme"],
    "Common Cold": ["Mint", "Anise"],       # Mint replacing Peppermint
    "Pharyngitis": ["Liquorice"],
    "Muscle Strain": ["Turmeric"],
    "Muscle Cramps": ["Turmeric", "Chamomile"],
    "Sore Muscles": ["Turmeric", "Chamomile"],
    "Food Poisoning": ["Fennel"],
    "Anemia": ["Fenugreek", "Turmeric"],
    "Angina": ["Green Tea"],
    "Arthritis": ["Turmeric", "Ginger"],
    "Vertigo": ["Thyme"],
    "Irritable Bowel Syndrome": ["Mint", "Fennel"],  # Mint replacing Peppermint
    "Allergic Rhinitis": ["Anise"],
    "Asthma": ["Thyme"],
    "Dermatitis": ["Sage"],
    "Fibromyalgia": ["Marjoram"],
    "Sleep Disorder": ["Lavender"],
    "Anxiety": ["Chamomile", "Lavender"],
    "Indigestion": ["Ginger", "Mint"],  # Mint replacing Peppermint
    "Inflammation": ["Turmeric"],
    "Hypertension": ["Green Tea"],
    "Migraine": ["Mint"],  # Mint replacing Peppermint
    "Motion Sickness": ["Ginger"],
    "Digestive Disorders": ["Mint", "Chamomile"],  # Mint replacing Peppermint
    "Liver Disease": ["Turmeric"],
    "Depression": ["Green Tea", "Lavender"],
    "Heart Disease": ["Green Tea", "Ginger"],
    "High Cholesterol": ["Green Tea", "Turmeric"],
    "Cancer Prevention": ["Green Tea", "Rosemary"],
    "Skin Conditions": ["Chamomile", "Lavender"],
    "Adrenal Fatigue": ["Liquorice"],
    "Bad Breath": ["Mint", "Sage"],  # Mint replacing Peppermint
    "Type 2 Diabetes": ["Cinnamon"],
    "Neurodegenerative Diseases": ["Green Tea"],
    "Cognitive Decline": ["Sage"],
    "Memory Loss": ["Rosemary"],
    "Hair Loss": ["Rosemary"],
    "Stress": ["Lavender"],
    "Weight Loss": ["Green Tea"],
    "Bloating": ["Fennel"],
    "Bronchitis": ["Thyme"],
    "Acne": ["Green Tea"],
    "Menstrual Cramps": ["Chamomile"],
    "Allergies": ["Anise"],
    "Urinary Tract Infections": ["Fenugreek"],
    "Sciatica": ["Turmeric"],
    "Lupus": ["Ginger"],
    "Gout": ["Cinnamon"],
    "Shingles": ["Thyme"],
    "Yeast Infection": ["Fenugreek"],
    "Hemorrhoids": ["Chamomile"],
    "Warts": ["Fennel"],
    "Ringworm": ["Thyme"],
    "Sinusitis": ["Thyme"],
    "Hangover": ["Mint"],
    "Cold Hands": ["Ginger"],
    "Gingivitis": ["Sage"],
    "Ulcer": ["Chamomile"],
    "Hives": ["Chamomile"],
    "Prostatitis": ["Fenugreek"],
    "Bladder Infection": ["Fenugreek"],
    "Chronic Fatigue Syndrome": ["Green Tea"],  # Assuming " Tea" meant Green Tea
    "Esophagitis": ["Liquorice"],
    "Laryngitis": ["Ginger"],
    "Pinworms": ["Fenugreek"],
    "Plantar Fasciitis": ["Turmeric"],
    "Rosacea": ["Green Tea"],
    "Teething": ["Chamomile", "Mint"],
    "Tinnitus": ["Rosemary"]
}

ingredient_key_map = {
    "Lavender": "1", #missing
    "Green Tea": "2",
    "Fennel": "3", #missing
    "Mint": "4",
    "Ginger": "5",
    "Turmeric": "6", #missing
    "Marjoram": "7",
    "Cinnamon": "8",
    "Felty Germander": "o3",
    "Thyme": "o2",
    "Rosemary": "o5",
    "Fenugreek": "o4",
    "Anise": "o8",
    "Cumin": "o6",
    "Sage": "o7",
    "Chamomile": "o1"
}

# Predefined list of symptoms
predefined_symptoms = set(symptom_diagnosis_db.keys())

def extract_symptoms(text):
    print(f"Analyzing text: {text}")  # Debug output
    doc = nlp(text.lower())
    symptoms = []
    for token in doc:
        # Match multi-word symptoms
        for length in range(1, 3):  # Check for symptoms of 1 or 2 words
            span = ' '.join([doc[i].text for i in range(token.i, min(token.i + length, len(doc)))])
            if span in predefined_symptoms:
                symptoms.append(span)
                print(f"Identified symptom: {span}")  # Debug output
                break  # Stop if a match is found for the current token
    return list(set(symptoms))  # Remove duplicates

def diagnose(symptoms):
    diagnoses = []
    for symptom in symptoms:
        if symptom in symptom_diagnosis_db:
            diagnosis = symptom_diagnosis_db[symptom]
            diagnoses.append(diagnosis)
            print(f"Symptom '{symptom}' diagnosed as '{diagnosis}'")  # Debug output
    return list(set(diagnoses))  # Remove duplicates

def get_treatment(diagnoses):
    treatments = []
    for diagnosis in diagnoses:
        if diagnosis in diagnosis_treatment_db:
            treatment = diagnosis_treatment_db[diagnosis]
            treatments.extend(treatment)
            print(f"Diagnosis '{diagnosis}' treated with '{treatment}'")  # Debug output

    # Print all treatments before mapping
    print(f"All treatments: {treatments}")  # Debug output

    # Map treatments to their keys
    treatment_keys = [ingredient_key_map[ingredient] for ingredient in treatments if ingredient in ingredient_key_map]

    # Concatenate the keys into a single string
    concatenated_keys = ''.join(treatment_keys)
    print(f"Concatenated treatment keys: {concatenated_keys}")  # Debug output

    # Return treatment keys and the concatenated string
    return {
        "treatments": treatments,
        "treatment_keys": treatment_keys,
        "concatenated_keys": concatenated_keys
    }


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    complaint = data.get('complaint', '')
    print(f"Received complaint: {complaint}")  # Debug output
    symptoms = extract_symptoms(complaint)
    print(f"Extracted symptoms: {symptoms}")  # Debug output
    diagnosis = diagnose(symptoms)
    print(f"Diagnosis: {diagnosis}")  # Debug output
    treatment = get_treatment(diagnosis)
    print(f"Treatment: {treatment}")  # Debug output
    response = {
        'symptoms': symptoms,
        'diagnosis': diagnosis,
        'herbs': treatment["treatments"],
        'treatment_keys': treatment["treatment_keys"],
        'concatenated_keys': treatment["concatenated_keys"]
    }

    print(f"Response: {response}")  # Debug output
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4000, debug=True)
