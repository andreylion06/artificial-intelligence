import numpy as np
import yfinance as yf
from sklearn import covariance, cluster
import json

with open("company_symbol_mapping.json", "r") as json_file:
    company_symbols_map = json.load(json_file)

symbols, names = np.array(list(company_symbols_map.items())).T

start_date = "2021-01-01"
end_date = "2024-11-01"

quotes = []

for symbol in symbols:
    try:
        data = yf.download(symbol, start=start_date, end=end_date, progress=False)
        if not data.empty:
            print(f"Успішно завантажено дані для {symbol}.")
            quotes.append(data)
        else:
            print(f"Не знайдено даних для завантаження {symbol}.")
    except Exception as e:
        print(f"Помилка при завантаженні {symbol}: {e}")

if len(quotes) == 0:
    print("Даних для аналізу не знайдено.")
    exit()

opening_quotes = [data['Open'].values for data in quotes]
closing_quotes = [data['Close'].values for data in quotes]

min_length = min(map(len, opening_quotes))
opening_quotes = np.array([x[:min_length] for x in opening_quotes], dtype=np.float64)
closing_quotes = np.array([x[:min_length] for x in closing_quotes], dtype=np.float64)

quotes_diff = np.array([closing - opening for closing, opening in zip(closing_quotes, opening_quotes)])
X = quotes_diff.T.squeeze()

print(f"Розмірність X: {X.shape}")

std_dev = X.std(axis=0)
std_dev[std_dev == 0] = 1
X /= std_dev

nan_mask = np.isnan(X)
col_means = np.nanmean(X, axis=0)
X[nan_mask] = np.take(col_means, np.where(nan_mask)[1])

edge_model = covariance.GraphicalLassoCV()
edge_model.fit(X)

_, labels = cluster.affinity_propagation(edge_model.covariance_)
num_labels = labels.max()

for i in range(num_labels + 1):
    print(f"\nCluster {i + 1} => {', '.join(names[labels == i])}")