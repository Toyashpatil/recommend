from flask import Flask, request, jsonify
import pickle

# Load your pre-trained models
with open('user_similarity.pkl', 'rb') as f:
    user_similarity = pickle.load(f)

with open('user_bus_matrix.pkl', 'rb') as f:
    user_bus_matrix = pickle.load(f)

# Initialize Flask app
app = Flask(__name__)

# Define the recommendation function (same as in Jupyter Notebook)
def recommend_buses(user_id, user_similarity_matrix, user_bus_matrix, num_recommendations=5):
    user_index = user_bus_matrix.index.get_loc(user_id)
    similar_users = user_similarity_matrix[user_index]
    top_similar_users = similar_users.argsort()[::-1][1:num_recommendations + 1]
    
    recommendations = []
    for similar_user in top_similar_users:
        similar_user_id = user_bus_matrix.index[similar_user]
        recommendations.extend(user_bus_matrix.columns[user_bus_matrix.loc[similar_user_id] > 0].tolist())
    
    return list(set(recommendations))

# Define a route for making recommendations
@app.route('/recommend', methods=['POST'])
def get_recommendation():
    data = request.get_json()  # Get the JSON payload
    user_id = data['user_id']  # Extract the user_id
    num_recommendations = data.get('num_recommendations', 5)  # Default is 5
    
    # Get recommendations
    recommendations = recommend_buses(user_id, user_similarity, user_bus_matrix, num_recommendations)
    
    # Return recommendations as JSON
    return jsonify({
        'user_id': user_id,
        'recommendations': recommendations
    })

if __name__ == '__main__':
    app.run(debug=True)
