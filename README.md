# Excel Predictive Dashboard

A lightweight Streamlit app for mocking sports viewership predictions.

- Displays fixed model settings (target feature, model, season controls)
- Lets you enter model parameters (numeric priors + playoff/national flags)
- Generates a mock predicted viewership value in a styled results panel

Note: prediction logic is currently a placeholder (`mock_prediction`) in `app.py`.

## Installation

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal (usually `http://localhost:8501`).
