import matplotlib.pyplot as plt
import csv

x = []
y = []

with open('results.csv','r') as csvfile:
	plots = csv.reader(csvfile, delimiter = ',')
	
	for row in plots:
		x.append(row[0])
		y.append(row[1])

plt.bar(x, y, color = 'g', width = 0.92, label = "Words")
plt.xlabel('MOST COMMON WORDS')
plt.ylabel('ABSOLUTE FREQUENCY')
plt.title('VISUALIZATION OF RELATED WORDS')
plt.legend()
plt.show()
