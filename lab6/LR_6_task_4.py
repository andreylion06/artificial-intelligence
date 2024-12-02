import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load dataset from local file
df = pd.read_csv('ticket_data.csv')
df.dropna(inplace=True)

print(f"Dataset shape after removing NaN: {df.shape}")

# Preview data
print("Dataset preview:\n", df.head())

# Unique values for each column
print("\nUnique values per column:")
for col in df.columns:
    print(f"{col}: {df[col].nunique()} unique values")

# Focus on relevant columns (simplify for this example)
selected_cols = ["origin", "destination", "train_type", "train_class", "fare", "price"]
df = df[selected_cols]

# Encode categorical features
df = pd.get_dummies(df, columns=["origin", "destination", "train_type", "train_class", "fare"], drop_first=True)

# Splitting features and target
X = df.drop("price", axis=1)
y = df["price"]

# Binning the price into categories (cheap, moderate, expensive)
price_bins = [0, 30, 60, np.inf]
price_labels = ["Cheap", "Moderate", "Expensive"]
y_binned = pd.cut(y, bins=price_bins, labels=price_labels)

# Distribution of ticket prices
plt.figure(figsize=(8, 6))
sns.histplot(y_binned, kde=False)
plt.title("Distribution of Ticket Prices (Binned)")
plt.xlabel("Price Category")
plt.ylabel("Frequency")
plt.show()

# Splitting the data
X_train, X_test, y_train, y_test = train_test_split(X, y_binned, test_size=0.3, random_state=42)

# Gaussian Naive Bayes
gnb = GaussianNB()
gnb.fit(X_train, y_train)
y_pred = gnb.predict(X_test)

# Evaluate the Gaussian Naive Bayes model
print("\nGaussian Naive Bayes Classification Report:")
print(classification_report(y_test, y_pred))

# Confusion matrix for Gaussian Naive Bayes
cm_gnb = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm_gnb, annot=True, fmt="d", cmap="Blues", xticklabels=price_labels, yticklabels=price_labels)
plt.title("Confusion Matrix: Gaussian Naive Bayes")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# Multinomial Naive Bayes (only for non-negative discrete features)
mnb = MultinomialNB()
X_train_discrete = (X_train * 100).astype(int)  # Scale to convert to discrete
X_test_discrete = (X_test * 100).astype(int)
mnb.fit(X_train_discrete, y_train)
y_pred_mnb = mnb.predict(X_test_discrete)

# Evaluate the Multinomial Naive Bayes model
print("\nMultinomial Naive Bayes Classification Report:")
print(classification_report(y_test, y_pred_mnb))

# Confusion matrix for Multinomial Naive Bayes
cm_mnb = confusion_matrix(y_test, y_pred_mnb)
plt.figure(figsize=(8, 6))
sns.heatmap(cm_mnb, annot=True, fmt="d", cmap="Greens", xticklabels=price_labels, yticklabels=price_labels)
plt.title("Confusion Matrix: Multinomial Naive Bayes")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# Accuracy comparison
print("\nAccuracy Comparison:")
print(f"Gaussian Naive Bayes Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(f"Multinomial Naive Bayes Accuracy: {accuracy_score(y_test, y_pred_mnb):.2f}")
