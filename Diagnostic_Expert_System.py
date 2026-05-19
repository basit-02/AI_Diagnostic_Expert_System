import streamlit as st

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
        """
        Confidence-Based Inference: 
        Calculates the percentage match between user facts and rule premises.
        """
        results = []
        for rule in self.rules:
            # Intersection finds which symptoms match the rule
            matching_symptoms = rule.premises.intersection(self.facts)
            match_count = len(matching_symptoms)
            total_required = len(rule.premises)
            
            if match_count > 0:
                confidence = (match_count / total_required) * 100
                results.append({
                    "conclusion": rule.conclusion,
                    "description": rule.description,
                    "confidence": round(confidence, 2),
                    "matched": list(matching_symptoms)
                })
        
        # Sort results: Highest confidence first
        return sorted(results, key=lambda x: x['confidence'], reverse=True)

# --- Knowledge Base Configuration ---
def load_expert_system():
    engine = ExpertSystem()
    
    engine.add_rule(["fever", "cough", "fatigue"], "Influenza (Flu)", 
                    "A viral infection that attacks your respiratory system. Common in seasonal outbreaks.")
    
    engine.add_rule(["headache", "sensitivity_to_light", "nausea"], "Migraine", 
                    "A recurring type of headache that can cause severe throbbing pain or a pulsing sensation.")
    
    engine.add_rule(["fever", "rash", "sore_throat"], "Scarlet Fever", 
                    "A bacterial illness that develops in some people who have strep throat.")
    
    engine.add_rule(["cough", "shortness_of_breath", "chest_pain"], "Respiratory Infection", 
                    "Inflammation or infection in the lungs or airways, often requiring rest or antibiotics.")
    
    engine.add_rule(["sneezing", "itchy_eyes", "runny_nose"], "Allergies", 
                    "The body's immune system reacting to harmless substances like pollen or dust.")
    
    engine.add_rule(["fever", "headache", "stiff_neck"], "Meningitis", 
                    "An inflammation of the fluid and membranes surrounding your brain and spinal cord.")
    
    return engine

# --- Streamlit UI Layout ---
def main():
    st.set_page_config(page_title="AI Expert System", page_icon="🩺", layout="centered")

    # Header Section
    st.title("🩺 AI Diagnostic Expert System")
    st.markdown("""
    **Forward Chaining & Pattern Matching Engine**  
    This system analyzes input symptoms against a professional Knowledge Base to provide a ranked list of potential diagnoses.
    """)
    st.divider()

    # Sidebar
    st.sidebar.header("System Logic")
    st.sidebar.write("**Inference Method:** Forward Chaining")
    st.sidebar.write("**Matching Algorithm:** Confidence-Weighted Subset Analysis")
    st.sidebar.info("Designed for KRR Lab 10: Mini Project")

    # Initialize Engine
    engine = load_expert_system()

    # Extract all unique symptoms for the UI
    all_possible_symptoms = set()
    for rule in engine.rules:
        all_possible_symptoms.update(rule.premises)
    
    # User Input
    st.subheader("1. Symptom Entry")
    selected_symptoms = st.multiselect(
        "Select your current symptoms:",
        options=sorted(list(all_possible_symptoms)),
        placeholder="Choose symptoms..."
    )

    # Inference Execution
    if st.button("Generate Diagnostic Report", type="primary"):
        if not selected_symptoms:
            st.warning("Please select at least one symptom to begin the inference process.")
        else:
            engine.set_facts(selected_symptoms)
            diagnoses = engine.run_inference()

            st.subheader("2. Diagnostic Results")
            
            if diagnoses:
                st.success(f"Analysis Complete: Found {len(diagnoses)} potential match(es).")
                
                for item in diagnoses:
                    # Professional UI Component for each match
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"### {item['conclusion']}")
                            st.write(item['description'])
                            st.caption(f"Matched symptoms: {', '.join(item['matched'])}")
                        
                        with col2:
                            st.metric("Confidence", f"{item['confidence']}%")
                            st.progress(item['confidence'] / 100)
            else:
                st.error("No matches found. The symptoms provided do not match any rules in the Knowledge Base.")

    st.divider()
    st.caption("Developed by Muhammad Basit Memon | Artificial Intelligence Dept. | DUET Karachi")

if __name__ == "__main__":
    main()
