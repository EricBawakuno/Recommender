import os
from flask import Flask, json, request, render_template, redirect, session, url_for
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generates a random 24-byte string for the secret key


# Define skill categories

# Note: All skills should be case sensetive
skill_categories = {
    'Programming Languages': ['Python', 'Java', 'JavaScript', 'C++', 'Ruby', 'Go', 'Rust', 'Swift', 'Kotlin'],
    'Data Science': ['Machine Learning', 'Deep Learning', 'Natural Language Processing', 'Computer Vision', 'Data Analysis', 'Statistics', 'Big Data', 'Data Visualization'],
    'Web Development': ['Front-end Development', 'Back-end Development', 'Full-stack Development', 'React', 'Angular', 'Vue.js', 'Node.js', 'Django', 'Flask'],
    'Databases': ['SQL', 'NoSQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'Oracle', 'Redis', 'Cassandra'],
    'Cloud Computing': ['AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes', 'Serverless Computing', 'Cloud Security'],
    'DevOps': ['CI/CD', 'Jenkins', 'GitLab', 'Ansible', 'Terraform', 'Prometheus', 'ELK Stack'],
    'Artificial Intelligence': ['Reinforcement Learning', 'Generative AI', 'Expert Systems', 'Robotics', 'Cognitive Computing'],
    'Cybersecurity': ['Network Security', 'Ethical Hacking', 'Cryptography', 'Blockchain', 'Information Security'],
    'Internet of Things (IoT)': ['Embedded Systems', 'Sensor Networks', 'MQTT', 'Edge Computing', 'IoT Protocols'],
    'Quantum Computing': ['Quantum Algorithms', 'Quantum Cryptography', 'Quantum Machine Learning', 'Quantum Programming'],
    'Bioinformatics': ['Genomics', 'Proteomics', 'Computational Biology', 'Systems Biology', 'Biostatistics'],
    'Renewable Energy': ['Solar Energy', 'Wind Energy', 'Hydroelectric Energy', 'Geothermal Energy', 'Energy Storage'],
    'Nanotechnology': ['Nanomaterials', 'Nanoelectronics', 'Nanobiotechnology', 'Molecular Nanotechnology'],
    'Aerospace': ['Aerodynamics', 'Propulsion Systems', 'Spacecraft Design', 'Satellite Technology', 'Avionics'],
    'Advanced Manufacturing': ['3D Printing', 'Robotics in Manufacturing', 'Smart Manufacturing', 'Industrial IoT', 'Digital Twin Technology']
}

# Create a reverse mapping of skills to categories
skill_to_category = {skill: category for category, skills in skill_categories.items() for skill in skills}

# Flatten the categories into a single list of skills
all_skills = [skill for category in skill_categories.values() for skill in category]

# Load and preprocess data
data = pd.read_csv('skills_data.csv')
data['skills'] = data['skills'].apply(lambda x: x.split(','))
mlb = MultiLabelBinarizer()
skills_matrix = mlb.fit_transform(data['skills'])
skills_df = pd.DataFrame(skills_matrix, columns=mlb.classes_, index=data['user_id'])
similarity_matrix = cosine_similarity(skills_df)
similarity_df = pd.DataFrame(similarity_matrix, index=skills_df.index, columns=skills_df.index)

def get_similar_users(skills, num_recommendations=5):
    input_vector = mlb.transform([skills])
    input_df = pd.DataFrame(input_vector, columns=mlb.classes_)
    input_similarity = cosine_similarity(input_df, skills_df)[0]
    similarity_series = pd.Series(input_similarity, index=skills_df.index)
    similar_users = similarity_series.sort_values(ascending=False).head(num_recommendations)
    return similar_users

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_skills = request.form.getlist('skills')

        if len(selected_skills) > 7:
            return render_template('index.html', skill_categories=skill_categories, error_message="Please select a maximum of 7 skills in total.")
        elif len(selected_skills) == 0:
            return render_template('index.html', skill_categories=skill_categories, error_message="Please select at least one skill.")
        else:
            similar_users = get_similar_users(selected_skills).to_dict()
            session['similar_users'] = similar_users
            session['selected_skills'] = selected_skills
            return redirect(url_for('results'))

    return render_template('index.html', skill_categories=skill_categories)

@app.route('/results')
def results():
    similar_users = session.get('similar_users')
    selected_skills = session.get('selected_skills')
    if not similar_users or not selected_skills:
        return redirect(url_for('index'))

    sorted_users = sorted(similar_users.items(), key=lambda x: x[1], reverse=True)

    # Separate into top users and other users
    top_users = {k: v for k, v in sorted_users if v > 0.1}
    other_users = {k: v for k, v in sorted_users if v <= 0.1}

    return render_template('results.html', top_users=top_users, other_users=other_users, selected_skills=selected_skills)


if __name__ == '__main__':
    app.run(debug=True)