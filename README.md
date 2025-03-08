# Education Statistics Dashboard

## 📌 Overview
This project is a **Streamlit-based interactive dashboard** for visualizing education statistics in India. The dashboard allows users to upload datasets, analyze trends, and compare education-related metrics across different states.

## 🚀 Features
- 📂 **Upload CSV datasets** for analysis
- 📊 **Visualizations using Plotly & Matplotlib**
  - State-wise Literacy Rate
  - Choropleth Map
  - Scatter Plot with Regression Line
- 📈 **Comparison of states based on:**
  - Literacy Rate
  - Pupil-Teacher Ratio
- 📝 **Feedback Form** (MongoDB integration)
- ❄ **Interactive Effects** (Snowfall & Lottie Animations)

## 🛠️ Tech Stack
- **Frontend**: Streamlit, Plotly, Matplotlib, Seaborn, Lottie
- **Backend**: Flask (for authentication and APIs)
- **Database**: MongoDB (Feedback storage)
- **Deployment**: Local (can be extended to cloud services)

## 🔧 Installation & Setup
1. **Clone the repository**:
   ```sh
   git clone https://github.com/your-username/Education-Statistics-Dashboard.git
   cd Education-Statistics-Dashboard
   ```
2. **Create and activate a virtual environment**:
   ```sh
   python -m venv myvenv
   source myvenv/bin/activate  # Mac/Linux
   myvenv\Scripts\activate  # Windows
   ```
3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
4. **Run the application**:
   ```sh
   streamlit run app.py
   ```

## 🎯 Usage
1. **Upload a dataset** (CSV format)
2. Click on "Show Analysis" to visualize the data
3. Use the sidebar to explore different statistics
4. Click on "Show Comparison" for insights on top/bottom states
5. Submit feedback via the form (stored in MongoDB)

## 📌 Dataset Requirements
Ensure your dataset has at least these columns:
- `State`
- `Literacy Rate`
- `Pupil Teacher Ratio`

## 📌 Known Issues & Fixes
1. **Choropleth Map Not Displaying:** Ensure the dataset contains valid state names that match the GeoJSON file.
2. **Lottie Animation Error:** Use an alternative Lottie JSON link or download and load the file locally.
3. **Pupil-Teacher Ratio Not Displaying:** Ensure the dataset includes this column and contains valid numeric data.

## 📌 Future Improvements
- **User authentication system** for personalized data analysis
- **Live API integration** for real-time education data updates
- **Export analysis reports** in PDF/Excel format

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).

## 🙌 Contributing
Feel free to submit issues, feature requests, or pull requests!

---
✨ Built with ❤️ by Mayank & Contributors 🚀

