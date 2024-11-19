import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures


m = 100
X = np.linspace(-3, 3, m)
y = 2 * np.sin(X) + np.random.uniform(-0.5, 0.5, m)

lin_reg = linear_model.LinearRegression()
lin_reg.fit(X.reshape(-1, 1), y)

X_plot = np.linspace(-3, 3, 100)
y_plot = lin_reg.predict(X_plot.reshape(-1, 1))
plt.scatter(X, y, label="Дані")
plt.plot(X_plot, y_plot, label="Прогнози", color="green")
plt.legend()
plt.show()


poly_features = PolynomialFeatures(degree=3, include_bias=False)
X_poly = poly_features.fit_transform(X.reshape(-1, 1))

lin_reg = linear_model.LinearRegression()
lin_reg.fit(X_poly, y)

print("Features X[0]:", X[0])
print("Features after transformation:", X_poly[0])

print("Regression coefficient =", lin_reg.coef_)
print("Regression interception =", lin_reg.intercept_)

X_plot = np.linspace(-3, 3, 100)
y_plot = lin_reg.predict(poly_features.transform(X_plot.reshape(-1, 1)))
plt.scatter(X, y, label="Дані")
plt.plot(X_plot, y_plot, label="Прогнози", color="green")
plt.legend()
plt.show()
