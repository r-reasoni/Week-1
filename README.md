# 🔋 EV Adoption Forecast App

**📍 Project Title:** County-wise Electric Vehicle Forecasting in Washington  
**🛠️ Developed During:** AICTE Green AI Internship  
**👩‍💻 Developer:** Rea Soni

## 🚗 Overview

This interactive web app forecasts the adoption of electric vehicles (EVs) across counties in **Washington State** over the next 3 years. Powered by machine learning and interactive visualizations, the app helps policymakers, researchers, and citizens better understand regional EV growth trends.

> 💡 Built using **Streamlit**, **scikit-learn**, and **matplotlib**, with a dark neon UI inspired by futuristic EV charging stations.

## 🔍 Features

- 📈 Forecast EV adoption for the next 3 years
- 🗺️ Compare EV trends across multiple counties
- ✨ Stylish dark neon UI with immersive visuals
- 📊 Dynamic charts showing historical vs forecasted EV growth

## 🧠 Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **ML Model:** Trained scikit-learn model (`joblib`)
- **Visualization:** Matplotlib
- **Data:** Preprocessed `.csv` dataset from Washington State open data

## 📁 Folder Structure

```
📁 EV AICTE
├── app.py                    # Streamlit application
├── forecasting_ev_model.pkl  # Trained ML model
├── preprocessed_ev_data.csv  # Cleaned input data
├── ev1.jpg                   # Background image
└── README.md                 # This file
```

## 🖥️ Run the App Locally

1. **Install dependencies** (recommended in a virtual environment):
   ```bash
   pip install streamlit pandas numpy matplotlib joblib
   ```

2. **Run the app:**
   ```bash
   streamlit run app.py
   ```

3. Visit `http://localhost:8501` in your browser.

## 🌍 Deployment (Streamlit Cloud)

To deploy this app on **Streamlit Cloud**:

- Push all files to your GitHub repo.
- Go to [streamlit.io/cloud](https://streamlit.io/cloud) → Click **"New App"**
- Choose:
  - Repository: your GitHub repo
  - Branch: `main`
  - File: `app.py`
- Click **Deploy**

That’s it — your app will be live on a public URL!

## 📸 UI Preview

### Forecast UI
![UI Background](ev1.jpg)

## ✅ Example Output

> EV adoption in *King County* is projected to **increase by 142.56%** in the next 3 years.

## 📜 License

This project is created under the **AICTE Green AI Internship** and is free for academic and non-commercial use.

## 🙌 Acknowledgments

- [AICTE Green AI Program](https://www.aicte-india.org/)
- [Streamlit](https://streamlit.io/)
- [Washington EV Open Data](https://data.wa.gov/)

## 👩‍💻 Author

**Rea Soni**  
B.Tech CSE | Mody University  
🔗 GitHub: [@r-reasoni](https://github.com/r-reasoni)  
📁 Project Repo: [Week-1](https://github.com/r-reasoni/Week-1)
