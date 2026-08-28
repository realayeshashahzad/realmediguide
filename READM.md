# 🩺 MediGuide AI

## AI-Powered Medical Symptom Assessment and Patient Guidance Assistant

MediGuide AI is an educational AI prototype built with **Python, LangChain, OpenAI, and Streamlit**.

The application allows users to enter basic patient information and symptoms. A LangChain-powered OpenAI model then generates structured, safety-focused preliminary guidance.

> ⚠️ **IMPORTANT MEDICAL & SAFETY NOTICE**
>
> MediGuide AI is an educational AI prototype only.
>
> It is **NOT a doctor, medical device, professional diagnosis, emergency service, or replacement for qualified medical advice or treatment.**
>
> The application must never be used to make a confirmed medical diagnosis.
>
> If symptoms are severe, rapidly worsening, or potentially life-threatening, seek emergency medical help immediately.

---

## 📌 Project Overview

People often search random websites when they experience symptoms. This can result in unreliable information, anxiety, and confusion.

MediGuide AI demonstrates how an AI application can provide structured educational information while following important medical-safety principles.

The application:

* Collects patient age and gender.
* Accepts multiple symptoms.
* Collects symptom duration.
* Records symptom severity from 1–10.
* Accepts existing medical conditions.
* Accepts current medications.
* Accepts additional notes.
* Uses LangChain and OpenAI.
* Generates structured JSON.
* Provides an urgency level.
* Provides possible conditions for educational purposes only.
* Provides recommended next steps.
* Provides questions to ask a healthcare professional.
* Displays warning signs.
* Supports English and Urdu responses.
* Supports LLM response streaming.
* Demonstrates InMemoryCache and SQLiteCache.

---

# 🎯 Learning Objectives

This project demonstrates the following LangChain concepts:

1. `ChatOpenAI`
2. `PromptTemplate`
3. `ChatPromptTemplate`
4. `SystemMessage`
5. `HumanMessage`
6. `AIMessage`
7. `LLMChain`
8. Structured JSON output
9. Safe JSON parsing
10. Streaming using `.stream()`
11. Streamlit `st.write_stream()`
12. `InMemoryCache`
13. `SQLiteCache`

---

# 🛠️ Technologies Used

| Technology          | Purpose                         |
| ------------------- | ------------------------------- |
| Python 3.10+        | Programming language            |
| LangChain           | LLM application framework       |
| LangChain OpenAI    | OpenAI integration              |
| LangChain Community | Caching                         |
| OpenAI              | Language model provider         |
| Streamlit           | User interface                  |
| python-dotenv       | Environment variable management |
| SQLite              | Persistent cache storage        |

---

# 📁 Project Structure

```text
medical_ai_assistant/
│
├── app.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── prompts.py
│   ├── chains.py
│   ├── cache_manager.py
│   └── utils.py
│
└── docs/
```

---

# ⚙️ Installation

## 1. Clone or download the project

Open the project folder in VS Code.

---

## 2. Create a virtual environment

Open the VS Code terminal:

```powershell
python -m venv .venv
```

---

## 3. Activate the virtual environment

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

After activation, the terminal should show:

```text
(.venv)
```

---

## 4. Install dependencies

Run:

```powershell
pip install -r requirements.txt
```

---

# 🔑 OpenAI API Key Setup

Create a `.env` file in the project root:

```text
medical_ai_assistant/
├── .env
├── app.py
└── ...
```

Add:

```env
OPENAI_API_KEY=your_real_openai_api_key
OPENAI_MODEL=gpt-4o-mini
```

Never hard-code the API key inside Python files.

Never upload `.env` to GitHub.

The `.gitignore` file already prevents `.env` from being committed.

---

# 🚀 Running the Application

Make sure the virtual environment is activated.

Run:

```powershell
streamlit run app.py
```

Streamlit will start the application in your browser.

---

# 🖥️ Application Features

## Patient Information

The application collects:

* Age
* Gender
* Symptoms
* Symptom duration
* Severity from 1–10
* Existing medical conditions
* Current medications
* Additional notes

---

## 🌐 Language Selection

The application supports:

* English
* Urdu

The selected language is included in the prompt sent to the model.

---

# 🧠 LangChain Architecture

The application follows this flow:

```text
User Input
    ↓
Streamlit Form
    ↓
Input Validation
    ↓
Patient Data
    ↓
PromptTemplate / ChatPromptTemplate
    ↓
System + Human Messages
    ↓
LLMChain
    ↓
ChatOpenAI
    ↓
Structured JSON Response
    ↓
Safe JSON Parsing
    ↓
Streamlit Dashboard
```

---

# 📝 PromptTemplate

The project uses `PromptTemplate` to create a reusable single-string patient prompt.

The template contains variables such as:

```text
age
gender
symptoms
duration
severity
existing_conditions
medications
additional_notes
language
```

---

# 💬 ChatPromptTemplate

The project also uses `ChatPromptTemplate`.

It separates the conversation into:

```text
System Message
        ↓
Human Message
```

The system message contains the medical safety rules.

The human message contains patient information.

---

# 🛡️ Medical Safety

Medical safety is one of the most important parts of this project.

The system prompt instructs the model to:

* Never provide a confirmed diagnosis.
* Never claim certainty.
* Present possible conditions only for educational purposes.
* Encourage professional medical consultation.
* Avoid prescribing medication.
* Avoid changing prescribed medication.
* Provide emergency guidance when appropriate.
* Use calm and understandable language.

The application also displays medical disclaimers in the interface.

---

# 🚨 Urgency Levels

The application uses four urgency levels:

| Level     | Meaning                                                       |
| --------- | ------------------------------------------------------------- |
| LOW       | Symptoms appear less concerning based on provided information |
| MEDIUM    | Professional evaluation may be appropriate                    |
| HIGH      | Prompt professional evaluation may be required                |
| EMERGENCY | Immediate emergency medical help should be sought             |

An urgency level is **not a medical diagnosis**.

---

# 📦 Structured JSON Output

The model is instructed to return the following structure:

```json
{
  "summary": "",
  "possible_conditions": [
    {
      "name": "",
      "reason": ""
    }
  ],
  "urgency_level": "",
  "recommended_next_steps": [],
  "questions_for_doctor": [],
  "warning_signs": []
}
```

---

# 🔒 Safe JSON Parsing

LLMs may sometimes return:

````text
```json
{
    ...
}
````

````

or additional text around the JSON.

The project handles this using helper functions in:

```text
src/utils.py
````

The parser:

1. Removes accidental Markdown JSON fences.
2. Extracts the JSON object.
3. Attempts `json.loads()`.
4. Validates the resulting dictionary.
5. Provides a safe fallback if parsing fails.
6. Prevents invalid JSON from crashing the application.

---

# ⚡ Streaming

MediGuide AI demonstrates LLM streaming.

The application uses:

```python
llm.stream()
```

to receive response chunks.

Streamlit displays the chunks using:

```python
st.write_stream()
```

This creates a natural typing-style experience instead of making the user wait for the entire response.

---

# 💾 Caching

The application demonstrates two LangChain cache types.

## InMemoryCache

```text
Stored in:
RAM / memory

Speed:
Fastest

Survives restart:
No

Best for:
Repeated requests during one session
```

## SQLiteCache

```text
Stored in:
SQLite database file

Speed:
Fast, but slightly slower than memory

Survives restart:
Yes

Best for:
Reusing responses across application sessions
```

The selected cache is registered using LangChain's:

```python
set_llm_cache()
```

---

# 📊 Cache Comparison

| Feature          | InMemoryCache | SQLiteCache       |
| ---------------- | ------------- | ----------------- |
| Storage          | RAM           | SQLite file       |
| Speed            | Fastest       | Fast              |
| Survives restart | No            | Yes               |
| Persistent       | No            | Yes               |
| Best use         | One session   | Multiple sessions |

When the same patient input is submitted again with caching enabled, LangChain can reuse the previous LLM response instead of making another model request.

---

# 🧪 Testing Scenarios

The following scenarios should be tested before submission.

## Test 1 — Mild Symptoms

```text
Age: 25
Symptoms: Runny nose + sore throat
Duration: 1-3 days
Severity: 2
```

Expected:

```text
LOW
```

The application should provide calm monitoring guidance.

---

## Test 2 — Fever and Cough

```text
Age: 40
Symptoms: Fever + cough
Duration: 4-7 days
Severity: 6
```

Expected:

```text
MEDIUM or HIGH
```

The application should recommend professional evaluation.

---

## Test 3 — Severe Symptoms

```text
Symptoms:
Chest pain + shortness of breath
```

Expected:

```text
HIGH or EMERGENCY
```

The application should clearly recommend immediate professional/emergency medical help when appropriate.

---

## Test 4 — Cache

Submit exactly the same form twice with caching enabled.

Expected:

```text
First request:
LLM call

Second identical request:
Cached response
```

The second request should generally be faster.

---

## Test 5 — Empty Symptoms

Submit the form without selecting or entering symptoms.

Expected:

```text
Warning/error message
```

The application should not call the OpenAI API.

---

## Test 6 — Urdu

Select:

```text
Answer language: Urdu
```

Expected:

The generated guidance should be provided in Urdu while maintaining the medical safety rules.

---

# 🔐 Security

Important security practices:

* API key is stored in `.env`.
* `.env` is excluded through `.gitignore`.
* API keys are never hard-coded.
* Real API keys should never be uploaded to GitHub.
* The application should not expose secrets in the Streamlit interface.

---

# 📌 Important Limitations

MediGuide AI is an educational prototype.

It has important limitations:

* It cannot physically examine a patient.
* It cannot perform laboratory tests.
* It cannot perform imaging.
* It cannot replace a doctor.
* Its output may be incorrect or incomplete.
* Possible conditions are not confirmed diagnoses.
* Emergency situations require real emergency medical services.

---

# 🎓 Assignment Requirements Covered

| Requirement        | Status |
| ------------------ | ------ |
| Streamlit UI       | ✅      |
| ChatOpenAI         | ✅      |
| PromptTemplate     | ✅      |
| ChatPromptTemplate | ✅      |
| SystemMessage      | ✅      |
| HumanMessage       | ✅      |
| AIMessage          | ✅      |
| LLMChain           | ✅      |
| Structured JSON    | ✅      |
| Safe JSON parsing  | ✅      |
| Streaming          | ✅      |
| InMemoryCache      | ✅      |
| SQLiteCache        | ✅      |
| Medical disclaimer | ✅      |
| Input validation   | ✅      |
| English / Urdu     | ✅      |

---

# ▶️ Quick Start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

---

# 📚 Educational Purpose

This project was developed as a programming assignment for learning:

* LangChain
* Large Language Model applications
* Prompt engineering
* Structured outputs
* Streaming
* Caching
* Streamlit application development
* Responsible AI design

---

# ⚠️ Final Medical Disclaimer

**MediGuide AI is an educational AI prototype and is not a medical device, doctor, professional diagnosis system, emergency service, or treatment system.**

Do not use this application to diagnose or treat a medical condition.

Always consult a qualified healthcare professional for medical advice.

For severe or life-threatening symptoms, seek emergency medical help immediately.

---

## 👩‍💻 Project

**Project Name:** MediGuide AI
**Type:** LangChain + Streamlit Programming Assignment
**Purpose:** Educational AI Prototype
