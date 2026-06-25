import streamlit as st
import datetime

# --- Core Logic: The Expert System Engine ---
class Rule:
    def __init__(self, premises, conclusion, description):
        self.premises = set(premises)
        self.conclusion = conclusion
        self.description = description

class ExpertSystem:
    def __init__(self):
        self.rules = []
        self.facts = set()

    def add_rule(self, symptoms, diagnosis, description=""):
        self.rules.append(Rule(symptoms, diagnosis, description))

    def set_facts(self, symptoms_list):
        self.facts = set([s.lower() for s in symptoms_list])

    def run_inference(self):
        results = []
        for rule in self.rules:
            matching_symptoms = rule.premises.intersection(self.facts)
            match_count = len(matching_symptoms)
            total_required = len(rule.premises)
            
            if match_count > 0:
                confidence = (match_count / total_required) * 100
                results.append({
                    "conclusion": rule.conclusion,
                    "description": rule.description,
                    "confidence": round(confidence, 2),
                    "matched": list(matching_symptoms),
                    "total_required": total_required
                })
        
        return sorted(results, key=lambda x: x['confidence'], reverse=True)

# --- Knowledge Base Configuration ---
@st.cache_resource
def load_expert_system():
    engine = ExpertSystem()
    engine.add_rule(["fever", "cough", "fatigue"], "Influenza (Flu)", "A viral infection that attacks your respiratory system. Common in seasonal outbreaks.")
    engine.add_rule(["headache", "sensitivity_to_light", "nausea"], "Migraine", "A recurring type of headache that can cause severe throbbing pain or a pulsing sensation.")
    engine.add_rule(["fever", "rash", "sore_throat"], "Scarlet Fever", "A bacterial illness that develops in some people who have strep throat.")
    engine.add_rule(["cough", "shortness_of_breath", "chest_pain"], "Respiratory Infection", "Inflammation or infection in the lungs or airways, often requiring rest or antibiotics.")
    engine.add_rule(["sneezing", "itchy_eyes", "runny_nose"], "Allergies", "The body's immune system reacting to harmless substances like pollen or dust.")
    engine.add_rule(["fever", "headache", "stiff_neck"], "Meningitis", "An inflammation of the fluid and membranes surrounding your brain and spinal cord.")
    return engine

# --- UI/UX Enhancements (Modern Dark Gradient CSS) ---

def inject_custom_css():
    st.markdown("""
        <style>
        /* FIX: Prevent the scrollbar jump/jerk */
        html, body, [data-testid="stAppViewContainer"] {
            overflow-y: scroll !important; 
        }

        /* 1. Modern Gradient Background (Black at top, Deep Blue at bottom) */
        .stApp {
            background: linear-gradient(to top, #020617 0%, #0a192f 50%, #000000 100%);
            background-attachment: fixed;
            color: #f8fafc;
        }
        
        /* FIX: Completely remove Streamlit clutter so it takes up zero space */
        header {display: none !important;}
        #MainMenu {display: none !important;}
        footer {display: none !important;}
        
        /* 2. Glassmorphism Result Cards */
        .result-card {
            background: rgba(30, 41, 59, 0.4); 
            backdrop-filter: blur(12px);       
            -webkit-backdrop-filter: blur(12px);
            padding: 24px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.1); 
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            margin-bottom: 20px;
        }
        
        /* Typography inside cards */
        .result-title {
            color: #e0e7ff;
            font-size: 1.4rem;
            font-weight: 700;
            margin-bottom: 8px;
            letter-spacing: 0.5px;
        }
        .result-desc {
            color: #94a3b8;
            font-size: 0.95rem;
            margin-bottom: 16px;
            line-height: 1.6;
        }
        
        /* 3. Neon Pill Tags for Symptoms */
        .symptom-tag {
            background-color: rgba(59, 130, 246, 0.15);
            color: #60a5fa;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-right: 8px;
            margin-bottom: 8px;
            display: inline-block;
            border: 1px solid rgba(59, 130, 246, 0.3);
            text-transform: capitalize;
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.1); 
        }
        
        /* Customize Tabs to look modern */
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 4px 4px 0px 0px;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
        }
        
        /* Force dark theme for inputs regardless of Streamlit base setting */
        div[data-baseweb="select"] > div {
            background-color: #1e293b;
            color: #f8fafc;
            border: 1px solid #334155;
        }
        </style>
    """, unsafe_allow_html=True)

# --- Helper: Generate Text Report ---
def generate_report(diagnoses, user_symptoms):
    report = f"--- CLINICAL DIAGNOSTIC REPORT ---\n"
    report += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"Patient Symptoms Reported: {', '.join(user_symptoms).title()}\n\n"
    report += "--- POTENTIAL DIAGNOSES ---\n"
    for d in diagnoses:
        report += f"[{d['confidence']}%] {d['conclusion']}\n"
        report += f"Description: {d['description']}\n"
        report += f"Matched Rules: {', '.join(d['matched']).title()} ({len(d['matched'])}/{d['total_required']})\n\n"
    report += "DISCLAIMER: This report is generated by an AI simulation and is not medical advice."
    return report

# --- Main Application ---
def main():
    st.set_page_config(page_title="AI Diagnostic Expert System", page_icon="🧬", layout="centered")
    inject_custom_css()

    # --- Header ---
    st.markdown("<h1 style='text-align: center; color: #f8fafc; font-weight: 800; letter-spacing: -1px;'>🧬 AI Diagnostic Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom: 30px; font-size: 1.1rem;'>Advanced Knowledge Representation & Reasoning Engine</p>", unsafe_allow_html=True)

    engine = load_expert_system()
    all_possible_symptoms = set()
    for rule in engine.rules:
        all_possible_symptoms.update(rule.premises)

    # --- Tabbed Layout ---
    tab1, tab2 = st.tabs(["Symptom Analysis", "View Knowledge Base"])

    with tab1:
        st.markdown("<h4 style='color: #e2e8f0;'>Patient Information</h4>", unsafe_allow_html=True)
        selected_symptoms = st.multiselect(
            "Select all actively presenting symptoms:",
            options=sorted(list(all_possible_symptoms)),
            placeholder="Type or select symptoms from the registry..."
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Run Diagnostic Inference", type="primary", use_container_width=True):
            if not selected_symptoms:
                st.error("Please select at least one symptom to begin the inference process.")
            else:
                engine.set_facts(selected_symptoms)
                diagnoses = engine.run_inference()

                st.divider()
                st.markdown("Diagnostic Results")
                
                if diagnoses:
                    for item in diagnoses:
                        # Constructing the Custom HTML Card
                        tags_html = "".join([f"<span class='symptom-tag'>{s.replace('_', ' ')}</span>" for s in item['matched']])
                        
                        st.markdown(f"""
                        <div class="result-card">
                            <div class="result-title">{item['conclusion']}</div>
                            <div class="result-desc">{item['description']}</div>
                            <div>{tags_html}</div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.progress(item['confidence'] / 100, text=f"Confidence Match: {item['confidence']}%")
                        st.markdown("<br>", unsafe_allow_html=True)
                    
                    # --- Download Report ---
                    report_text = generate_report(diagnoses, selected_symptoms)
                    st.download_button(
                        label="Download Clinical Report",
                        data=report_text,
                        file_name=f"Diagnosis_Report_{datetime.datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                else:
                    st.info("No clinical matches found in the current system parameters.")

    with tab2:
        st.markdown("<h4 style='color: #e2e8f0;'>Active Rule Base</h4>", unsafe_allow_html=True)
        st.markdown("<p style='color: #94a3b8;'>This system operates on a forward-chaining logic framework. Below are the current rules loaded in the engine.</p>", unsafe_allow_html=True)
        for i, rule in enumerate(engine.rules):
            with st.expander(f"Rule {i+1}: {rule.conclusion}"):
                st.write(f"**Required Symptoms:** {', '.join(rule.premises).replace('_', ' ').title()}")
                st.write(f"**Description:** {rule.description}")

    # --- Footer ---
    st.divider()
    st.markdown("<p style='text-align: center; color: #475569; font-size: 0.85rem;'>Engineered by Muhammad Basit Memon | DUET Karachi</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
