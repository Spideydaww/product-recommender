from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

products_prob = pd.read_csv("recommender_model/products_prob.csv")

def recommend(prod, n):
    basket = prod
    no_of_suggestions = n
    all_of_basket = products_prob[basket]
    all_of_basket = all_of_basket.sort_values(ascending=False)
    suggestions_to_customer = list(all_of_basket.index[:no_of_suggestions])
    output = []
    for i in suggestions_to_customer:
        output.append(products_prob.loc[i, 'Unnamed: 0'])
    return output

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            basket = request.json['basket']
            num_recommendations = int(request.json['numRecommendations'])
        except KeyError:
            return jsonify({'error': 'Invalid request data'}), 400
        
        recommended_products = recommend(basket, num_recommendations)
        return jsonify({'recommendations': recommended_products})
    
    return render_template('index.html')
@app.route('/performance.html')
def performance():
    return render_template('performance.html')
if __name__ == '__main__':
    app.run(debug=True)
    
