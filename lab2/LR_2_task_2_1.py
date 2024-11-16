import numpy as np
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score

# Читання даних
X = []
y = []
count_class1 = 0
count_class2 = 0
max_datapoints = 10000  # Зменшую кількість даних для тестування

with open('income_data.txt', 'r') as f:
    for line in f.readlines():
        if count_class1 >= max_datapoints and count_class2 >= max_datapoints:
            break
        if '?' in line:
            continue
        data = line[:-1].split(', ')
        if data[-1] == '<=50K' and count_class1 < max_datapoints:
            X.append(data)
            count_class1 += 1
        if data[-1] == '>50K' and count_class2 < max_datapoints:
            X.append(data)
            count_class2 += 1

# Перетворення на масив numpy
X = np.array(X)

# Перетворення рядкових даних на числові
label_encoder = []
X_encoded = np.empty(X.shape)
for i, item in enumerate(X[0]):
    if item.isdigit():
        X_encoded[:, i] = X[:, i]
    else:
        label_encoder.append(preprocessing.LabelEncoder())
        X_encoded[:, i] = label_encoder[-1].fit_transform(X[:, i])

X = X_encoded[:, :-1].astype(float)  # Тепер використовуємо float, щоб було легше нормалізувати
y = X_encoded[:, -1].astype(int)

# Нормалізація даних
scaler = preprocessing.StandardScaler()
X = scaler.fit_transform(X)

# Поділ даних на тренувальні та тестові вибірки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)



classifier = SVC(kernel='poly', degree=3)
classifier.fit(X_train, y_train)

f1 = cross_val_score(classifier, X, y, scoring='f1_weighted', cv=3)
accuracy_values = cross_val_score(classifier, X, y, scoring='accuracy', cv=3)
precision_values = cross_val_score(classifier, X, y, scoring='precision_weighted', cv=3)
recall_values = cross_val_score(classifier, X, y, scoring='recall_weighted', cv=3)

print(f"SVM with poly kernel:")
print("F1 score: " + str(round(100 * f1.mean(), 2)) + "%")
print("Accuracy: " + str(round(100 * accuracy_values.mean(), 2)) + "%")
print("Precision: " + str(round(100 * precision_values.mean(), 2)) + "%")
print("Recall: " + str(round(100 * recall_values.mean(), 2)) + "%")

# Передбачення результату для тестової точки даних
input_data = ['37', 'Private', '215646', 'HS-grad', '9', 'Never-married', 'Handlers-cleaners', 'Not-in-family', 'White', 'Male',
             '0', '0', '40', 'United-States']

# Кодування тестової точки даних
input_data_encoded = [-1] * len(input_data)
count = 0
for i, item in enumerate(input_data):
    if item.isdigit():
        input_data_encoded[i] = int(input_data[i])
    else:
        input_data_encoded[i] = int(label_encoder[count].transform([item])[0])
        count += 1

input_data_encoded = np.array(input_data_encoded)
input_data_encoded = scaler.transform(input_data_encoded.reshape(1, -1))  # Нормалізуємо дані тестової точки

# Використання класифікатора для передбачення класу
predicted_class = classifier.predict(input_data_encoded)
print("Сlass:", label_encoder[-1].inverse_transform(predicted_class)[0])
