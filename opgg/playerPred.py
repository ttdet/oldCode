import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV
from sklearn.decomposition import PCA, KernelPCA
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, LabelBinarizer, OneHotEncoder
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.manifold import TSNE, LocallyLinearEmbedding
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

matches = pd.read_csv('opgg_enlarged.csv')

X = matches.iloc[:, 2:11]
y = matches.iloc[:, -1]


num_list = {'kill', 'death', 'assist'}
cat_list = {'result', 'champion', 'd', 'f', 'mainRune', 'minorRune'}

def ScaleFeatures(X):
    scaler = StandardScaler()
    scaled = scaler.fit_transform(X.loc[:, num_list])
    scaled_frame = pd.DataFrame(scaled)
    X_scaled = pd.concat([X, scaled_frame], axis = 1)
    return X_scaled


def BinarizeFeatures(X_scaled):
    flag = False
    for cat in cat_list:
        FeatureBinarizer = LabelBinarizer()
        bin = FeatureBinarizer.fit_transform(X_scaled.loc[:, cat])
        binarized_frame = pd.DataFrame(bin)
        if flag:
            X_binarized = pd.concat([X_binarized, binarized_frame], axis = 1)
        else:
            X_binarized = pd.concat([X_scaled, binarized_frame], axis = 1)
            flag = True

    return X_binarized


def DropFeatures(X):
    for cat in cat_list:
        X.drop(cat, axis = 1, inplace = True)
    for num in num_list:
        X.drop(num, axis = 1, inplace = True)

def TransformInstance(match):
    new_matches = pd.concat([X, pd.DataFrame(match)], axis = 0)
    new_matches = new_matches.reset_index(drop = True)
    new_matches_scaled = ScaleFeatures(new_matches)
    new_matches_binarized = BinarizeFeatures(new_matches_scaled)
    DropFeatures(new_matches_binarized)

    return new_matches_binarized.iloc[-1]

rbf_svc = SVC(kernel = 'rbf', C = 3, gamma = 0.1)
simple_svc = SVC(kernel = 'poly', C = 0.1, coef0 = 1, degree = 5)
log_reg = LogisticRegression()
forest = RandomForestClassifier(n_estimators = 50, max_depth = 8, min_samples_split = 4)
knn = KNeighborsClassifier(n_neighbors = 3)

X_scaled = ScaleFeatures(X)
X_binarized = BinarizeFeatures(X_scaled)
DropFeatures(X_binarized)



match = {
    'result': ['Defeat'],
    'champion': ['Kai\'Sa'],
    'd': ['Flash'],
    'f': ['Cleanse'],
    'mainRune': ['Hail of Blades'],
    'minorRune': ['Inspiration'],
    'kill': [4.0],
    'death': [8.0],
    'assist': [5.0]
}

processed_match = TransformInstance(match)

simple_svc.fit(X_binarized.iloc[:, :], y)
print('prediction is: ' + str(simple_svc.predict([processed_match])))
#gumayushi = 1, Wayne = 0
