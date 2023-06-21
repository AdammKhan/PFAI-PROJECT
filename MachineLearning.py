import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics  # Add this line

# Load the dataset
data = pd.read_csv('names_dataset.csv')

# Remove duplicates (if any)
data = data.drop_duplicates()

# Shuffle the dataset
data = data.sample(frac=1).reset_index(drop=True)

# Split the dataset into features (X) and labels (y)
X = data['name']
y = data['gender']

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the CountVectorizer
vectorizer = CountVectorizer(analyzer='char', ngram_range=(1, 3))

# Fit and transform the training set
X_train_features = vectorizer.fit_transform(X_train)

# Transform the testing set
X_test_features = vectorizer.transform(X_test)

# Initialize the model
model = MultinomialNB()

# Train the model
model.fit(X_train_features, y_train)

# Make predictions on the testing set
y_pred = model.predict(X_test_features)

# Calculate accuracy
accuracy = metrics.accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Prompt the user to input a name
new_name = input("Enter a name: ")

# Preprocess the input name and transform it into features
new_name_features = vectorizer.transform([new_name])

# Predict the gender of the input name
predicted_gender = model.predict(new_name_features)
print("Predicted gender:", predicted_gender)
