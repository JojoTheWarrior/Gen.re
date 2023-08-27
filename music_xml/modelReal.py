#!/usr/bin/env python
# coding: utf-8

# In[65]:


# Environment
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import sklearn
warnings.simplefilter("ignore")


# In[66]:


# Data Loading - R 
path = "xml_folder/working_txt/"

# Data Loading - R 
Data_Right_5 = pd.read_csv(f"{path}right_White_Christmas_-_piano.musicxml.txt").to_numpy()
Data_Right_6 = pd.read_csv(f"{path}right_The_Blue_Danube.musicxml.txt").to_numpy()
Data_Right_7 = pd.read_csv(f"{path}right_Menuet_-_g-minor__J.S.Bach.musicxml.txt").to_numpy()
Data_Right_8 = pd.read_csv(f"{path}right_sonatina.musicxml.txt").to_numpy()
Data_Right_9 = pd.read_csv(f"{path}right_Invention_No_13_Bach.musicxml.txt").to_numpy()
Data_Right_10 = pd.read_csv(f"{path}right_Sonatina_in_F_Major_Anh.5_No.2_Beethoven_.musicxml.txt").to_numpy()

Data_Right_11 = pd.read_csv(f"{path}right_sonnyita_end.musicxml.txt").to_numpy()
Data_Right_12 = pd.read_csv(f"{path}right_sonnyita.musicxml.txt").to_numpy()

# In[67]:


Data_Right = np.concatenate((Data_Right_5,Data_Right_6,Data_Right_7, Data_Right_8, Data_Right_9, Data_Right_10, Data_Right_11, Data_Right_12), axis=0)
Data_Right.shape

# In[68]:


Data_Left_5 = pd.read_csv(f"{path}left_White_Christmas_-_piano.musicxml.txt").to_numpy()
Data_Left_6 = pd.read_csv(f"{path}left_The_Blue_Danube.musicxml.txt").to_numpy()
Data_Left_7 = pd.read_csv(f"{path}left_Menuet_-_g-minor__J.S.Bach.musicxml.txt").to_numpy()
Data_Left_8 = pd.read_csv(f"{path}left_sonatina.musicxml.txt").to_numpy()
Data_Left_9 = pd.read_csv(f"{path}left_Invention_No_13_Bach.musicxml.txt").to_numpy()
Data_Left_10 = pd.read_csv(f"{path}left_Sonatina_in_F_Major_Anh.5_No.2_Beethoven_.musicxml.txt").to_numpy()
Data_Left_11 = pd.read_csv(f"{path}left_sonnyita_end.musicxml.txt").to_numpy()
Data_Left_12 = pd.read_csv(f"{path}left_sonnyita.musicxml.txt").to_numpy()
Data_Left = np.concatenate((   Data_Left_5, Data_Left_6,Data_Left_7, Data_Left_8, Data_Left_9, Data_Left_10, Data_Left_11, Data_Left_12), axis=0)
Data_Left.shape


# In[69]:


# Featuring Engineering
from sklearn.preprocessing import OneHotEncoder

OHE = OneHotEncoder(sparse_output=False)
Data_Right_OHE = OHE.fit_transform(Data_Right)
Data_Right_OHE.shape


# In[70]:


# train_test split
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(Data_Right_OHE, 
                                                    Data_Left, test_size=0.2)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)


# In[71]:


# Model - RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
RFC = RandomForestClassifier(max_features=None, n_estimators=140)
Model_RFC = RFC.fit(X_train, y_train)
Model_RFC


# In[72]:


from sklearn.metrics import accuracy_score
accuracy_score(y_test, Model_RFC.predict(X_test))


# In[74]:


Left = Model_RFC.predict(X_test)
Left


# In[76]:


df = pd.DataFrame(Left, columns=["L"])
df


# In[78]:


decode = OHE.inverse_transform(X_test)


# In[94]:


a = decode.reshape(-1)


# In[95]:


List = [i for i in a]


# In[96]:


df["R"] = List


# In[97]:


df


# In[100]:


# saving the dataframe
df.to_csv('result.csv')