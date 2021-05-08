import numpy as np
import pandas as pd
import seaborn as sns
import os
from sklearn.preprocessing import LabelEncoder


def set_pandas():
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)

def resequence(df_, cols):
    df = df_.reindex(columns=cols)
    return df

def Encoder(df, cols):
    labels = LabelEncoder()
    for each in cols:
        df["{}".format(each)] = labels.fit_transform(df["{}".format(each)])
    return df
