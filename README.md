# Doctor Recommender with Appointment Booking

A smart web application that recommends doctor specializations based on user symptoms using OpenAI's GPT model, filters doctors by location, shows doctor details including Google Maps links, and allows users to book appointment slots.

---

## Features

- **Symptom-based Doctor Specialization Prediction:**  
  Enter symptoms, and the app uses GPT to suggest the right doctor specialization (e.g., General Physician, Neurologist, ENT Specialist).

- **Location-based Doctor Search:**  
  After selecting the specialization, the app filters available doctors based on the user's input location.

- **Doctor Details & Google Maps:**  
  View doctors' clinic addresses, fees, available time slots, and clickable links to Google Maps for clinic location.

- **Appointment Booking:**  
  Users can select an available time slot and book appointments directly within the app.

- **State Management with LangGraph:**  
  The app uses LangGraph to manage the flow of states — from symptom input to specialization prediction, doctor search, and booking.

---

## Technologies Used

- **Python 3.8+**  
- **Streamlit:** For building the interactive web UI  
- **LangGraph:** To manage application state and workflow  
- **LangChain & OpenAI API:** For LLM-driven doctor specialization prediction  
- **dotenv:** To load OpenAI API keys from `.env` securely  

---

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/doctor-recommender.git
   cd doctor-recommender
