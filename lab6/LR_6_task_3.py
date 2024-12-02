from collections import Counter

playData = [
    {"Day": "D1", "Outlook": "Sunny", "Humidity": "High", "Wind": "Weak", "Play": "No"},
    {"Day": "D2", "Outlook": "Sunny", "Humidity": "High", "Wind": "Strong", "Play": "No"},
    {"Day": "D3", "Outlook": "Overcast", "Humidity": "High", "Wind": "Weak", "Play": "Yes"},
    {"Day": "D4", "Outlook": "Rain", "Humidity": "High", "Wind": "Weak", "Play": "Yes"},
    {"Day": "D5", "Outlook": "Rain", "Humidity": "Normal", "Wind": "Weak", "Play": "Yes"},
    {"Day": "D6", "Outlook": "Rain", "Humidity": "Normal", "Wind": "Strong", "Play": "No"},
    {"Day": "D7", "Outlook": "Overcast", "Humidity": "Normal", "Wind": "Strong", "Play": "Yes"},
    {"Day": "D8", "Outlook": "Sunny", "Humidity": "High", "Wind": "Weak", "Play": "No"},
    {"Day": "D9", "Outlook": "Sunny", "Humidity": "Normal", "Wind": "Weak", "Play": "Yes"},
    {"Day": "D10", "Outlook": "Rain", "Humidity": "Normal", "Wind": "Weak", "Play": "Yes"},
    {"Day": "D11", "Outlook": "Sunny", "Humidity": "Normal", "Wind": "Strong", "Play": "Yes"},
    {"Day": "D12", "Outlook": "Overcast", "Humidity": "High", "Wind": "Strong", "Play": "Yes"},
    {"Day": "D13", "Outlook": "Overcast", "Humidity": "Normal", "Wind": "Weak", "Play": "Yes"},
    {"Day": "D14", "Outlook": "Rain", "Humidity": "High", "Wind": "Strong", "Play": "No"},
]



play_yes_count = Counter(row["Play"] for row in playData if row["Play"] == "Yes").total()
play_count = len(playData)
play_yes_prob = play_yes_count / play_count
print("Probability of the game being played: {0}/{1} = {2}"
      .format(play_yes_count, play_count, round(play_yes_prob, 3)))

sunny_yes_count = Counter(
    row["Outlook"] for row in playData if row["Play"] == "Yes" and row["Outlook"] == "Sunny").total()
sunny_yes_prob = sunny_yes_count / play_yes_count
print("Probability of sunny for the game: {0}/{1} = {2}"
      .format(sunny_yes_count, play_yes_count, round(sunny_yes_prob, 3)))

humidity_high_yes_count = Counter(
    row["Humidity"] for row in playData if row["Play"] == "Yes" and row["Humidity"] == "High").total()
humidity_high_yes_prob = humidity_high_yes_count / play_yes_count
print("Probability of high humidity for the game: {0}/{1} = {2}"
      .format(humidity_high_yes_count, play_yes_count, round(humidity_high_yes_prob, 3)))

wind_weak_yes_count = Counter(
    row["Wind"] for row in playData if row["Play"] == "Yes" and row["Wind"] == "Weak").total()
wind_weak_yes_prob = wind_weak_yes_count / play_yes_count
print("Probability of weak wind for the game: {0}/{1} = {2}"
      .format(wind_weak_yes_count, play_yes_count, round(wind_weak_yes_prob, 3)))


total_probability = play_yes_prob * sunny_yes_prob * humidity_high_yes_prob * wind_weak_yes_prob
print("\nProbability of the game with outlook sunny, high humidity, weak wind:"
      " \n{:.3f} * {:.3f} * {:.3f} * {:.3f} = {:.4f}"
      .format(play_yes_prob, sunny_yes_prob, humidity_high_yes_prob, wind_weak_yes_prob, total_probability))
