import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
import pickle

data = fetch_california_housing()

df = pd.DataFrame(data.data, columns=data.feature_names)
df['Price'] = data.target

X = df.drop("Price", axis=1)
y = df["Price"]

model = RandomForestRegressor()
model.fit(X, y)

pickle.dump(model, open("house_model.pkl", "wb"))

print("Model trained and saved!")