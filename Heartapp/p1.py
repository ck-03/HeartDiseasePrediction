import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle


data = pd.read_csv("Heart_Disease_Prediction.csv")
print(data.head())

print(data.isnull().sum())

features = data[["Age", "Chest pain type", "BP", "Cholesterol", "Max HR", "ST depression", "Number of vessels fluro", "Thallium"]]
target = data['Heart Disease']

print(features)
print(target)

x_train, x_test, y_train, y_test = train_test_split(features, target, random_state = 3136)

model = RandomForestClassifier()
model.fit(x_train, y_train)


print(model.feature_importances_)
plt.figure(figsize = (12,10))
x = features.columns
y = model.feature_importances_
plt.bar(x,y)
plt.xlabel("Features")
plt.ylabel("Importances")
plt.show()


y_pred = model.predict(x_test)


cr = classification_report(y_pred, y_test)
print(cr)


with open("heartdiseaseprediction.model", "wb") as f:
	pickle.dump(model, f)

