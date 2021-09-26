import pandas as pd ; 
from sklearn.metrics import confusion_matrix
import numpy as np
OURCSVFILE ='results.csv'
test_df = pd.read_csv(OURCSVFILE)
actualvalue = test_df['Absolute frequency']
predictedValue = test_df['Relative frequency']
actualvalue = actualvalue.values
predictedValue = predictedValue.values

rounded_labels=np.argmax(predictedValue, axis=0)
# rounded_labels[0]
# cmt = confusion_matrix(actualvalue,rounded_labels)
print (actualvalue)
print(predictedValue)

