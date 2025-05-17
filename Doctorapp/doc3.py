from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
import streamlit as st
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

class GraphState(TypedDict):
    symptoms: str
    location: str
    specialization: str
    doctors: List[dict]

# Initialize LLM
llm = OpenAI(temperature=0)

# Prompt template to get specialization from symptoms
prompt = PromptTemplate(
    input_variables=["symptoms"],
    template="""
Given the symptoms below, suggest the doctor specialization (e.g., General Physician, Neurologist, ENT Specialist):

Symptoms: {symptoms}

Answer ONLY specialization name.
"""
)
llm_chain = LLMChain(llm=llm, prompt=prompt)

def normalize_specialization(spec: str) -> str:
    spec = spec.lower()
    if "general" in spec and "physician" in spec:
        return "General Physician"
    elif "neuro" in spec:
        return "Neurologist"
    elif "ent" in spec or "ear" in spec or "nose" in spec or "throat" in spec:
        return "Ent Specialist"
    else:
        return spec.title()

# Step 1: Predict specialization from symptoms
def predict_specialization(state: GraphState) -> GraphState:
    specialization = llm_chain.run(state["symptoms"]).strip()
    specialization = normalize_specialization(specialization)
    return {**state, "specialization": specialization}

# Step 2: Return doctors based on specialization + location filtering
def search_doctors(state: GraphState) -> GraphState:
    mock_data = {
        "General Physician": [
            {
                "name": "Dr. Ravi",
                "clinic": "City Clinic",
                "fee": "₹500",
                "slots": ["10:00 AM", "2:00 PM"],
                "location_address": "City Clinic, Salem"
            },
            {
                "name": "Dr. Anjali",
                "clinic": "Health Plus",
                "fee": "₹600",
                "slots": ["11:30 AM", "4:00 PM"],
                "location_address": "Health Plus, Chennai"
            },
            {
                  "name": "Dr. Ajay",
                "clinic": "medico",
                "fee": "₹600",
                "slots": ["11:30 AM", "4:00 PM"],
                "location_address": "Health Plus, Chennai" 
            }
        ],
        "Neurologist": [
            {
                "name": "Dr. Kumar",
                "clinic": "Neuro Center",
                "fee": "₹1200",
                "slots": ["9:00 AM", "3:00 PM"],
                "location_address": "Neuro Center, Salem"
            },
            {
                "name": "Dr. Priya",
                "clinic": "Brain Care",
                "fee": "₹1500",
                "slots": ["1:00 PM", "5:30 PM"],
                "location_address": "Brain Care, Coimbatore"
            },
        ],
        "Ent Specialist": [
            {
                "name": "Dr. Meena",
                "clinic": "ENT Clinic",
                "fee": "₹800",
                "slots": ["10:30 AM", "3:30 PM"],
                "location_address": "ENT Clinic, Namakkal"
            },
              {
                "name": "Dr. shraya",
                "clinic": "NEET Clinic",
                "fee": "₹800",
                "slots": ["10:30 AM", "3:30 PM"],
                "location_address": "ENT Clinic, Namakkal"
            },
            

        ],
    }

    all_doctors = mock_data.get(state["specialization"], [])
    location = state["location"].lower()

    # ✅ Filter by location match
    filtered_doctors = [
        doc for doc in all_doctors
        if location in doc["location_address"].lower()
    ]

    return {**state, "doctors": filtered_doctors}

# Build LangGraph flow
builder = StateGraph(GraphState)
builder.add_node("PredictSpecialization", predict_specialization)
builder.add_node("SearchDoctors", search_doctors)
builder.set_entry_point("PredictSpecialization")
builder.add_edge("PredictSpecialization", "SearchDoctors")
builder.add_edge("SearchDoctors", END)
graph = builder.compile()

def main():
    st.title("🧠 LangGraph-based Doctor Recommender with Appointment Booking")

    symptoms = st.text_area("Enter your symptoms:")
    location = st.text_input("Enter your location:")

    if st.button("🔍 Find Doctors"):
        if not symptoms.strip() or not location.strip():
            st.warning("Please enter both symptoms and location.")
            return

        input_state = {
            "symptoms": symptoms.strip(),
            "location": location.strip(),
            "specialization": "",
            "doctors": [],
        }

        final_state = graph.invoke(input_state)

        st.success(f"Recommended Specialist: **{final_state['specialization']}**")

        st.session_state["doctors"] = final_state["doctors"]
        st.session_state["location"] = location.strip()

    if "appointments" not in st.session_state:
        st.session_state["appointments"] = []

    if "doctors" in st.session_state and st.session_state["doctors"]:
        st.sidebar.title("👨‍⚕️ Available Doctors")

        for idx, doc in enumerate(st.session_state["doctors"]):
            with st.sidebar.expander(f"{doc['name']} - {doc['clinic']} (Fee: {doc['fee']})", expanded=False):
                st.write(f"📍 Address: {doc.get('location_address', 'Not Available')}")

                if "location_address" in doc:
                    map_url = f"https://www.google.com/maps/search/?api=1&query={doc['location_address'].replace(' ', '+')}"
                    st.markdown(f"[🌐 View on Google Maps]({map_url})", unsafe_allow_html=True)

                slot_key = f"slot_{idx}"
                book_key = f"booked_{idx}"

                selected_slot = st.selectbox(
                    f"Select time slot for {doc['name']}",
                    doc.get("slots", []),
                    key=slot_key,
                )

                if st.button(f"Book Appointment", key=f"book_{idx}"):
                    new_appointment = {
                        "doctor": doc["name"],
                        "clinic": doc["clinic"],
                        "slot": selected_slot,
                        "location": doc.get("location_address", ""),
                    }
                    if new_appointment not in st.session_state["appointments"]:
                        st.session_state["appointments"].append(new_appointment)
                    st.session_state[book_key] = True

                if st.session_state.get(book_key):
                    st.success(f"🎉 Appointment booked with **{doc['name']}** at **{selected_slot}**.")

        if st.session_state["appointments"]:
            st.sidebar.subheader("📋 Your Booked Appointments:")
            for appt in st.session_state["appointments"]:
                st.sidebar.write(
                    f"🩺 {appt['doctor']} at {appt['clinic']} — {appt['slot']} ({appt['location']})"
                )

if __name__ == "__main__":
    main()
