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

herbs = {
    "herb1": 100,
    "herb2": 100,
    "herb3": 100,
    "herb4": 100,
    "herb5": 100,
    "herb6": 100,
    "herb7": 100,
    "herb8": 100,
    "herb9": 100,
    "herb10": 100,
    "herb11": 100,
    "herb12": 100,
    "herb13": 100,
    "herb14": 100,
    "herb15": 100,
    "herb16": 100,
}

# Predefined list of symptoms
predefined_symptoms = set(symptom_diagnosis_db.keys())


@app.route('/')
def index():
    return render_template('index.html')


last_analysis_result = {}
last_concatenated_keys = ''


@app.route('/submit', methods=['POST'])
def submit():
    global last_concatenated_keys, last_analysis_result

    data = request.json
    print("Received data:", data)  # Debugging: Print received data

    complaint = data.get('complaint', '')
    selected_product_keys = data.get('selectedProductKeys', [])
    print("Complaint:", complaint)  # Debugging: Print the complaint
    print("Selected Product Keys:", selected_product_keys)  # Debugging: Print selected keys

    # Step 1: Text Analysis for Symptoms, Diagnosis, and Treatments
    doc = nlp(complaint.lower())
    detected_symptoms = []
    detected_diagnosis = []
    detected_treatments = []

    for token in doc:
        if token.text in symptom_diagnosis_db:
            symptom = token.text
            diagnosis = symptom_diagnosis_db[symptom]
            treatments = diagnosis_treatment_db.get(diagnosis, [])
            detected_symptoms.append(symptom)
            detected_diagnosis.append(diagnosis)
            detected_treatments.extend(treatments)

    print("Detected Symptoms:", detected_symptoms)  # Debugging: Print detected symptoms
    print("Detected Diagnosis:", detected_diagnosis)  # Debugging: Print detected diagnosis
    print("Detected Treatments:", detected_treatments)  # Debugging: Print detected treatments

    detected_treatments = list(set(detected_treatments))  # Remove duplicates
    treatment_keys = [ingredient_key_map[treatment] for treatment in detected_treatments if treatment in ingredient_key_map]

    print("Treatment Keys:", treatment_keys)  # Debugging: Print treatment keys

    # Step 2: Concatenate treatment keys with selected product keys
    all_keys = treatment_keys + selected_product_keys
    concatenated_keys = ''.join(all_keys)
    print("Concatenated Keys:", concatenated_keys)  # Debugging: Print concatenated keys
    last_concatenated_keys = concatenated_keys  # Update the global variable

    # Save the last analysis result
    last_analysis_result = {
        "symptoms": detected_symptoms,
        "diagnosis": detected_diagnosis,
        "herbs": detected_treatments,
        "treatment_keys": treatment_keys,
        "concatenated_keys": concatenated_keys,
        "selectedProductKeys": selected_product_keys
    }

    print("Last Analysis Result:", last_analysis_result)  # Debugging: Print the final result

    return jsonify(last_analysis_result)


@app.route('/last_keys', methods=['GET'])
def get_last_keys():
    global last_concatenated_keys
    return jsonify(last_concatenated_keys)


@app.route('/add_herb', methods=['POST'])
def add_herb():
    new_herb = request.json.get('herb_name')
    if new_herb and new_herb not in herbs:
        herbs[new_herb] = 100
        return jsonify({"message": f"Herb '{new_herb}' added successfully."})
    return jsonify({"error": "Herb already exists or invalid name."}), 400


@app.route('/delete_herb', methods=['POST'])
def delete_herb():
    herb_name = request.json.get('herb_name')
    if herb_name in herbs:
        del herbs[herb_name]
        return jsonify({"message": f"Herb '{herb_name}' deleted successfully."})
    return jsonify({"error": "Herb not found."}), 400


@app.route('/herbs', methods=['GET'])
def get_herbs():
    return jsonify(herbs)


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)




