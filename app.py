from flask import Flask, render_template, jsonify
import plotly.express as px
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_chart_data')
def get_chart_data():
    df = pd.read_csv(r"C:\Users\Mayank Rathore\Desktop\EducationStatistic\education08_1.csv")
    fig = px.bar(df, x="State", y="Literacy Rate", title="State-wise Literacy Rate")
    graph_json = fig.to_json()
    return jsonify(graph_json)

if __name__ == '__main__':
    app.run(debug=True)
