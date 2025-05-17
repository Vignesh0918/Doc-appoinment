DOCTOR-APPOINMENT -BOOKING

---

LangGraph-based Doctor Recommender with Appointment Booking

This is a Streamlit web app powered by LangGraph, LangChain, and OpenAI that helps users:

Identify the right doctor specialization based on symptoms.

View a list of available doctors in their location.

Book appointments by selecting available time slots.



---

Demo

Features:

LLM-powered specialization prediction based on symptoms

Location-based doctor filtering

Streamlit sidebar UI to show doctors and appointments

Google Maps integration for clinic addresses

Stateful appointment tracking using st.session_state



---

Tech Stack

LangChain

LangGraph

OpenAI API

Streamlit

Python 3.9+



---

How It Works

1. User inputs symptoms and their location


2. LLM predicts the best doctor specialization


3. Doctors are filtered by location and shown


4. User can select time slots and book appointments




---

Setup Instructions

1. Clone the Repository

git clone https://github.com/your-username/doctor-recommender-langgraph.git
cd doctor-recommender-langgraph

2. Install Dependencies

Create a virtual environment and install:

python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt

requirements.txt sample:

openai
langchain
langgraph
streamlit
python-dotenv

3. Set Up OpenAI API Key

Create a .env file in the project root:

OPENAI_API_KEY=your_openai_api_key_here

4. Run the App

streamlit run app.py


---

Folder Structure

.
├── app.py             # Main Streamlit app with LangGraph integration
├── .env               # Your OpenAI API key
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation


---

Example Input

> Symptoms: Headache, dizziness, blurry vision
Location: Salem



Output:

Recommended Specialist: Neurologist

Available Doctors:

Dr. Kumar at Neuro Center (Salem)

Dr. Priya at Brain Care (Coimbatore)




---

Screenshot

(Add a screenshot here of the app running with an example search and booked appointment)


---

License

MIT License


---

Let me know if you'd like me to generate a requirements.txt file or add badges, Dockerfile, or GitHub Actions workflow.
