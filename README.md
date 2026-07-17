# Advance Recommendation System

This repository is a Streamlit-based Crop & Fertilizer Recommendation web app.

## Summary
- Interactive web app to recommend optimal crops and fertilizer using trained models.
- Built with Python, scikit-learn, CatBoost, LightGBM and Streamlit.

## Setup (Windows, `venv`)
1. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Upgrade pip and install dependencies:

```bash
venv\Scripts\pip install --upgrade pip setuptools wheel
venv\Scripts\pip install -r requirements.txt
```

3. Run the app:

```bash
venv\Scripts\streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Docker
Build and run with Docker:

```bash
docker build -t advance-reco .
docker run -p 8501:8501 advance-reco
```

## Easy Live Deployment (Recommended)
The simplest way to publish this app is Streamlit Community Cloud:

1. Push your project to GitHub.
2. Open https://share.streamlit.io and sign in.
3. Click **New app**, choose your GitHub repo, branch `main`, and set the file path to `app.py`.
4. Click **Deploy**.

Streamlit will build the app and give you a public URL you can share.

## Troubleshooting
- If model loading fails, ensure `Models/` exists and contains the `.pkl` files.
- If a dependency fails to install, try upgrading pip and installing the failing package separately.

## Resume bullets
- Implemented a Streamlit-based Crop & Fertilizer Recommendation web app using scikit-learn, CatBoost, and LightGBM to predict optimal crops and fertilizer based on soil and weather features.
- Built end-to-end pipeline: data preprocessing, model serialization, and an interactive Streamlit UI for recommendations and visualizations.
- Containerized the app with Docker for reproducible deployment and documented setup with a step-by-step `README.md`.
