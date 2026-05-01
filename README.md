# 🎬 Movie Recommendation System

This is a content-based movie recommendation system built using machine learning techniques. It suggests movies based on user preferences by analyzing movie features and computing similarity scores.

## 🚀 Features
- Content-based recommendation
- Fast similarity search using vectors
- Simple Python implementation

## 🛠️ Tech Stack
- Python
- Pandas
- Scikit-learn
- Streamlit

## 📸 Screenshots
<img width="1874" height="859" alt="Screenshot 2026-04-29 161455" src="https://github.com/user-attachments/assets/96554558-26c7-46d9-ab62-10892bf80464" />

<img width="1862" height="906" alt="Screenshot 2026-04-29 161705" src="https://github.com/user-attachments/assets/8baced3d-a78e-4406-87ac-65e3c7310d78" />

## ⚙️ How It Works
- Movie data is collected and cleaned
- Features like genres, keywords, cast are combined
- Text data is converted using TF-IDF Vectorization
- Similarity between movies is calculated using Cosine Similarity
- Top similar movies are recommended to the user

## 📂 Dataset

This project uses the TMDB Movies Dataset from Kaggle:

👉 https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset

Files used:
- movies_metadata.csv
- credits.csv
- keywords.csv

Note: Large files like `ratings.csv` were not used.

## 📦 Installation
```bash
pip install -r requirements.txt
```
## ▶️ Run the App
```bash
streamlit run app.py
```
## 🔮 Future Improvements
- Add collaborative filtering
- Improve recommendation accuracy
- Deploy as a web application
- Add user login system
## 📌 Conclusion

This project demonstrates how machine learning techniques like TF-IDF and cosine similarity can be used to build an efficient recommendation system
