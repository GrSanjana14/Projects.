import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

# Load dataset
df = pd.read_csv("D:/StudentsPerformance_dataset.csv")

# --- EDA ---
print("Dataset Head:\n", df.head())
print("\nInfo:\n")
df.info()
print("\nSummary Statistics:\n", df.describe())

# Combined boxplot of test, reading, and writing scores
plt.figure(figsize=(8, 6))
sns.boxplot(data=df[['test score', 'reading score', 'writing score']], palette='Set2')
plt.title("Combined Boxplot of Test, Reading, and Writing Scores")
plt.ylabel("Score")
plt.grid(True)
plt.tight_layout()
plt.show()

# Correlation heatmap
plt.figure(figsize=(6, 4))
sns.heatmap(df.select_dtypes(include=np.number).corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()

# --- Preprocessing ---
X = df.drop(columns=["test score"])
y = df["test score"]

num_cols = X.select_dtypes(exclude="object").columns
cat_cols = X.select_dtypes(include="object").columns

preprocessor = ColumnTransformer([
    ("onehot", OneHotEncoder(drop='first'), cat_cols),
    ("scaler", StandardScaler(), num_cols)
])

# Train-test split
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Models to compare
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42)
}

results = []

for name, model in models.items():
    pipe = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])
    pipe.fit(x_train, y_train)
    y_pred = pipe.predict(x_test)

    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    results.append({
        'Model': name,
        'MSE': mse,
        'MAE': mae,
        'R² Score': r2
    })

    # Actual vs Predicted Plot
    plt.figure(figsize=(6, 4))
    sns.regplot(x=y_test, y=y_pred, ci=None, line_kws={"color": "red"})
    plt.xlabel("Actual Test Score")
    plt.ylabel("Predicted Test Score")
    plt.title(f"{name} - Actual vs Predicted")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Create DataFrame of results
results_df = pd.DataFrame(results)
print("\nModel Performance Comparison:")
print(results_df)

# Comparison Bar Plot
plt.figure(figsize=(8, 5))
x = np.arange(len(results_df['Model']))
width = 0.25

plt.bar(x - width, results_df['MSE'], width, label='MSE')
plt.bar(x, results_df['MAE'], width, label='MAE')
plt.bar(x + width, results_df['R² Score'], width, label='R² Score')

plt.xticks(x, results_df['Model'])
plt.title("Model Comparison: MSE, MAE, R²")
plt.ylabel("Score")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Save best model (based on highest R²)
best_model_name = results_df.sort_values("R² Score", ascending=False).iloc[0]['Model']
best_pipe = Pipeline(steps=[('preprocessor', preprocessor), ('model', models[best_model_name])])
best_pipe.fit(X, y)
joblib.dump(best_pipe, 'best_model.pkl')
print(f"\nBest model ({best_model_name}) saved as 'best_model.pkl'")
