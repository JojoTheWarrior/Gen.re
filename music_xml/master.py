import to_mid
import utils
import pandas as pd
import numpy as np
Data = pd.read_csv("result.csv")


output = np.array(Data["L"])

input = np.array(Data["R"])


output = utils.turn_to_training(output)
input = utils.turn_to_training(input)

print(output)

to_mid.audio(input, output, "TEST")