# Recommendation System

## Overview

This Recommendation System tool  allows users to select skills from various STEM and innovative categories. Based on the selected skills, the application finds and displays similar users from a pre-existing dataset.

## Tech Stack

- Backend: Python with Flask
- Frontend: HTML, CSS, JavaScript
- Data Processing: pandas, scikit-learn

## Project Structure

```
Recommendation System/
│
├── app.py                 # Main Flask application
├── templates/
│   └── index.html         # HTML template for the web interface
├── skills_data.csv        # CSV file containing user skills data
└── README.md              # This file
```

1. Download this project.

2. Start the Flask server:
   ```
   python app.py
   ```

3. Open a web browser and navigate to `http://localhost:5000`

4. Use the interface to select skills (up to 3 per category) and submit to find similar users.

## Customizing Skills and Categories

To modify the available skills or categories:

1. Open `app.py`
2. Locate the `skill_categories` dictionary
3. Modify the categories or skills as needed
4. Restart the Flask server for changes to take effect

Note: Ensure that your `skills_data.csv` file is updated to include any new skills you add.
