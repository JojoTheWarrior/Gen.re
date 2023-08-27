#!/usr/bin/env python
# coding: utf-8

# In[132]:


# Environment
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter("ignore")


# In[133]:

path = "xml_folder/working_txt/"

# Data Loading - R 
Data_Right_5 = pd.read_csv(f"{path}right_White_Christmas_-_piano.musicxml.txt").to_numpy()
Data_Right_6 = pd.read_csv(f"{path}right_The_Blue_Danube.musicxml.txt").to_numpy()
Data_Right_7 = pd.read_csv(f"{path}right_Menuet_-_g-minor__J.S.Bach.musicxml.txt").to_numpy()
Data_Right_8 = pd.read_csv(f"{path}right_sonatina.musicxml.txt").to_numpy()
Data_Right_9 = pd.read_csv(f"{path}right_Invention_No_13_Bach.musicxml.txt").to_numpy()
Data_Right_10 = pd.read_csv(f"{path}right_Sonatina_in_F_Major_Anh.5_No.2_Beethoven_.musicxml.txt").to_numpy()


# In[134]:


Data_Right = np.concatenate((Data_Right_5, 
                             Data_Right_6, Data_Right_7, Data_Right_8, Data_Right_9, Data_Right_10), axis=0)
Data_Right.shape


# In[135]:


# Data loading - L

Data_Left_5 = pd.read_csv(f"{path}left_White_Christmas_-_piano.musicxml.txt").to_numpy()
Data_Left_6 = pd.read_csv(f"{path}left_The_Blue_Danube.musicxml.txt").to_numpy()
Data_Left_7 = pd.read_csv(f"{path}left_Menuet_-_g-minor__J.S.Bach.musicxml.txt").to_numpy()
Data_Left_8 = pd.read_csv(f"{path}left_sonatina.musicxml.txt").to_numpy()
Data_Left_9 = pd.read_csv(f"{path}left_Invention_No_13_Bach.musicxml.txt").to_numpy()
Data_Left_10 = pd.read_csv(f"{path}left_Sonatina_in_F_Major_Anh.5_No.2_Beethoven_.musicxml.txt").to_numpy()
Data_Left = np.concatenate(( Data_Left_5, 
                            Data_Left_6, Data_Left_7, Data_Left_8, Data_Left_9, Data_Left_10), axis=0)
Data_Left.shape


# In[136]:


# Featuring Engineering
from sklearn.preprocessing import OneHotEncoder

OHE = OneHotEncoder(sparse_output=False)
Data_Right_OHE = OHE.fit_transform(Data_Right)
Data_Right_OHE.shape


# In[137]:


Data_Right_OHE[:1]


# In[138]:


# train_test split
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(Data_Right_OHE, 
                                                    Data_Left, test_size=0.2)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)


# In[139]:


# Model - KNN
from sklearn.neighbors import KNeighborsClassifier
KNN = KNeighborsClassifier(n_neighbors=2)

Model_KNN = KNN.fit(X_train, y_train)
Model_KNN


# In[140]:


from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, Model_KNN.predict(X_test)))


# In[141]:


# Model - SVC
from sklearn import svm
SVC = svm.SVC()

Model_SVC = SVC.fit(X_train, y_train)
Model_SVC


# In[142]:


print(accuracy_score(y_test, Model_SVC.predict(X_test)))


# In[143]:


# Model - SGDClassifier
from sklearn.linear_model import SGDClassifier
SGD = SGDClassifier()

Model_SGD = SGD.fit(X_train, y_train)
Model_SGD


# In[144]:


print(accuracy_score(y_test, Model_SGD.predict(X_test)))


# In[145]:


# Model - DecisionTreeClassifier
from sklearn.tree import DecisionTreeClassifier
DTC = DecisionTreeClassifier()

Model_DTC = SGD.fit(X_train, y_train)
Model_DTC


# In[146]:


print(accuracy_score(y_test, Model_DTC.predict(X_test)))


# In[147]:


# Model - RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
RFC = RandomForestClassifier()
Model_RFC = RFC.fit(X_train, y_train)
Model_RFC


# In[148]:


print(accuracy_score(y_test, Model_RFC.predict(X_test)))


# In[149]:


# Mode - Extremely Randomized Trees
from sklearn.ensemble import ExtraTreesClassifier
ETC = RandomForestClassifier()
Model_ETC = ETC.fit(X_train, y_train)
Model_ETC


# In[150]:


print(accuracy_score(y_test, Model_ETC.predict(X_test)))


# In[151]:


# Model - Gradient Tree Boosting
from sklearn.ensemble import GradientBoostingClassifier
GBC = GradientBoostingClassifier()
Model_GBC = GBC.fit(X_train, y_train)
Model_GBC


# In[ ]:


print(accuracy_score(y_test, Model_GBC.predict(X_test)))


# In[ ]:


from sklearn.ensemble import BaggingClassifier
Bag = BaggingClassifier(KNeighborsClassifier(),
                            max_samples=0.5, max_features=0.5)
Model_Bag = Bag.fit(X_train, y_train)
Model_Bag


# In[ ]:


print(accuracy_score(y_test, Model_Bag.predict(X_test)))


# In[ ]:


# Model - AdaBoostClassifier
from sklearn.ensemble import AdaBoostClassifier
Ada = AdaBoostClassifier()
Model_Ada = Ada.fit(X_train, y_train)
Model_Ada


# In[ ]:


print(accuracy_score(y_test, Model_Ada.predict(X_test)))


# In[ ]:


# Model - Histogram-Based Gradient Boosting
from sklearn.ensemble import HistGradientBoostingClassifier
HBC = HistGradientBoostingClassifier()
Model_HBC = HBC.fit(X_train, y_train)
Model_HBC


# In[ ]:


accuracy_score(y_test, Model_HBC.predict(X_test))


# In[ ]:


# Model - Voting Classifier
from sklearn.ensemble import VotingClassifier
List = [("KNN", KNN), ("SVC", SVC), ("SGD", SGD), ("DTC", DTC), ("RFC", RFC),
        ("ETC", ETC), ("GBC", GBC), ("Bag", Bag), ("Ada", Ada), ("HBC", HBC)]
VC = VotingClassifier(estimators=List)
Model_VC = VC.fit(X_train, y_train)
Model_VC


# In[ ]:


accuracy_score(y_test, Model_VC.predict(X_test))


# In[ ]:


# a == 


# # In[ ]:


# get_ipython().run_cell_magic('time', '', '# Optimize - RFC\nfrom sklearn.model_selection import GridSearchCV\n\nparameters = {"n_estimators": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 150]),\n              "criterion": ["gini", "entropy", "log_loss"], \n              "max_features": ["sqrt", "log2", None]}\nGSCV = GridSearchCV(estimator=Model_RFC, param_grid=parameters)\nGSCV.fit(X_train, y_train)\n')

