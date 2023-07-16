import csv
import random

people = list(range(1, 301))
preferences = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q']

rows = []
for person in people:
    preferences_shuffled = preferences.copy()
    random.shuffle(preferences_shuffled)
    preferences_selected = preferences_shuffled[:17]
    rows.append([person] + preferences_selected)

filename = 'lottery.csv'
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['number', '1w', '2w', '3w', '4w', '5w', '6w', '7w', '8w', '9w', '10w', '11w', '12w', '13w', '14w', '15w', '16w', '17w'])
    writer.writerows(rows)

print(f"CSV 파일 '{filename}'이 생성되었습니다.")
