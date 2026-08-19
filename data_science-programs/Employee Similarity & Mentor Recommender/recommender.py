"""
recommender.py – Content-based employee similarity.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics.pairwise import cosine_similarity

class EmployeeRecommender:
    def __init__(self, employees_df: pd.DataFrame):
        """
        employees_df: DataFrame with columns: id, name, job_title, department, salary (optional)
        """
        self.employees_df = employees_df.copy()
        self.employee_ids = self.employees_df['id'].tolist()
        self.names = self.employees_df['name'].tolist()

        # Feature engineering
        # We'll use job_title, department, and salary (scaled)
        # Optionally, we can also include years of experience (if hire_date available)
        # Compute years of experience (approximate from hire_date to now)
        if 'hire_date' in self.employees_df.columns:
            self.employees_df['years_exp'] = (pd.Timestamp.now() - self.employees_df['hire_date']).dt.days / 365.25
        else:
            self.employees_df['years_exp'] = 0

        # Select features
        categorical_features = ['job_title', 'department']
        numerical_features = ['salary', 'years_exp']

        # Build a column transformer to encode categoricals and scale numerics
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
                ('num', StandardScaler(), numerical_features)
            ],
            remainder='drop'
        )

        # Fit and transform to get feature matrix
        self.feature_matrix = self.preprocessor.fit_transform(self.employees_df)

    def recommend_for_employee(self, employee_id, top_n=5, exclude_self=True):
        """
        Return top N most similar employees for a given employee_id.
        """
        if employee_id not in self.employee_ids:
            return pd.DataFrame()  # employee not found

        # Find index of employee
        idx = self.employee_ids.index(employee_id)

        # Get feature vector for target employee
        target_features = self.feature_matrix[idx].reshape(1, -1)

        # Compute cosine similarity with all employees
        similarities = cosine_similarity(target_features, self.feature_matrix).flatten()

        # Exclude self if requested
        if exclude_self:
            similarities[idx] = -1

        # Get top N indices
        top_indices = np.argsort(similarities)[::-1][:top_n]
        top_ids = [self.employee_ids[i] for i in top_indices]
        top_scores = similarities[top_indices]

        # Get names and other details
        result = self.employees_df.iloc[top_indices][['id', 'name', 'job_title', 'department']].copy()
        result['similarity'] = top_scores

        return result

    def recommend_random(self, top_n=5):
        """Recommend similar employees for a random employee."""
        import random
        emp_id = random.choice(self.employee_ids)
        recs = self.recommend_for_employee(emp_id, top_n=top_n)
        return emp_id, recs

    def most_similar_pair(self):
        """Find the pair of employees with the highest cosine similarity (excluding self)."""
        sim_matrix = cosine_similarity(self.feature_matrix)
        np.fill_diagonal(sim_matrix, -1)
        i, j = np.unravel_index(np.argmax(sim_matrix), sim_matrix.shape)
        return self.employee_ids[i], self.employee_ids[j], sim_matrix[i, j]
