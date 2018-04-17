from convert_to_numpys import DataHandler
import pandas as pd
import numpy as np
import timeit
import matplotlib.pyplot as plt
from sklearn import svm, cross_validation, model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_selection import RFE, SelectKBest, chi2
from sklearn.metrics import precision_recall_fscore_support, classification_report
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, learning_curve, cross_validate
from sklearn.metrics import average_precision_score, precision_recall_curve, accuracy_score, roc_auc_score
from sklearn.feature_selection import SelectFromModel


class Prediction:
    def __init__(self, X_train, y_train, X_test, y_test):
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

    def run_logistic_regression(self):
        print("-" * 100)
        print("RUNNING LOGISTIC REGRESSION CLASSIFIER")
        model = LogisticRegression()
        model.fit(self.X_train, self.y_train)
        y_score = model.decision_function(self.X_test)
        print("Accuracy: %.10f" % (model.score(self.X_test, self.y_test)))
        print(model.predict(self.X_test))
        print(self.y_test)

    def run_svm(self):
        print("-" * 100)
        print("RUNNING SVM CLASSIFIER")
        model = svm.SVC()
        model.fit(self.X_train, self.y_train)
        y_score = model.decision_function(self.X_test)
        print(model.predict(self.X_test))
        print(self.y_test)
        print("Accuracy: %.10f" % (model.score(self.X_test, self.y_test)))

    def run_linear_svm(self):
        print("-" * 100)
        print("RUNNING LINEAR SVM CLASSIFIER")
        model = svm.LinearSVC()
        model.fit(self.X_train, self.y_train)
        y_score = model.decision_function(self.X_test)
        print(model.predict(self.X_test))
        print(self.y_test)
        print("Accuracy: %.10f" % (model.score(self.X_test, self.y_test)))

    def run_neural_network(self):
        print("-" * 100)
        print("RUNNING NEURAL NETWORK CLASSIFIER")
        model = MLPClassifier()
        model.fit(self.X_train, self.y_train)
        y_pred = model.predict(self.X_test)
        self.print_metrics(y_pred, model)
        precision, recall, _, _ = precision_recall_fscore_support(self.y_test, y_pred)
        self.plot_precision_recall_curve(precision, recall)

    def run_naive_bayes(self):
        print("-" * 100)
        print("RUNNING NAIVE BAYES CLASSIFIER")
        model = GaussianNB()
        model.fit(self.X_train, self.y_train)
        y_pred = model.predict(self.X_test)
        self.print_metrics(y_pred, model)
        precision, recall, _, _ = precision_recall_fscore_support(self.y_test, y_pred)
        self.plot_precision_recall_curve(precision, recall)

    def run_random_forests(self):
        print("-" * 100)
        print("RUNNING RANDOM FORESTS CLASSIFIER")
        model = RandomForestClassifier()
        model.fit(self.X_train, self.y_train)
        y_pred = model.predict(self.X_test)
        self.print_metrics(y_pred, model)
        precision, recall, _, _ = precision_recall_fscore_support(self.y_test, y_pred)
        self.plot_precision_recall_curve(precision, recall)

    def plot_precision_recall_curve(self, precision, recall):
        plt.step(recall, precision, color='b', alpha=0.2, where='post')
        plt.fill_between(recall, precision, alpha=0.2, color='b')

        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.title('2-class Precision-Recall curve, K = 2000')
        plt.show()

    def print_metrics(self, y_pred, model):
        test_accuracy = model.score(self.X_test, self.y_test)
        print("Number of mislabeled points out of a total %d points : %d"
              % (self.X_test.shape[0], np.sum(self.y_test != y_pred)))
        report = classification_report(self.y_test, y_pred)
        kfold = model_selection.KFold(n_splits=10, random_state=42)
        training_accuracy = model_selection.cross_val_score(model, self.X_train, self.y_train,
                                                            cv=kfold, scoring='accuracy')
        training_roc_auc = model_selection.cross_val_score(model, self.X_train, self.y_train, cv=kfold, scoring='roc_auc')
        training_precision = model_selection.cross_val_score(model, self.X_train, self.y_train, cv=kfold,
                                                             scoring='precision')
        training_recall = model_selection.cross_val_score(model, self.X_train, self.y_train, cv=kfold,
                                                             scoring='recall')
        training_f1 = model_selection.cross_val_score(model, self.X_train, self.y_train, cv=kfold,
                                                             scoring='f1')
        print(report)
        print("Test Accuracy: %.10f" % test_accuracy)
        print(training_accuracy.mean())
        print(training_accuracy.std())
        print(training_roc_auc.mean())
        print(training_roc_auc.std())
        print(training_precision.mean())
        print(training_precision.std())
        print(training_recall.mean())
        print(training_recall.std())
        print(training_f1.mean())
        print(training_f1.std())

    def plot_learning_curve(self, model, title, X, y, ylim=None,
                            cv=None,n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5)):
        plt.figure()
        plt.title(title)
        if ylim is not None:
            plt.ylim(*ylim)
        plt.xlabel("Training examples")
        plt.ylabel("Score")
        train_sizes, train_scores, test_scores = learning_curve(
            model, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
        train_scores_mean = np.mean(train_scores, axis=1)
        train_scores_std = np.std(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)
        test_scores_std = np.std(test_scores, axis=1)
        plt.grid()

        plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std, alpha=0.1,
                         color="r")
        plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.1, color="g")
        plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
                 label="Training score")
        plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
                 label="Cross-validation score")

        plt.legend(loc="best")
        plt.show()


def main():
    data_handler = DataHandler('player_tup.pickle', 'club_tup.pickle', 'transfer_new.pickle')

    player_df, club_df, transfer_df = data_handler.get_data_frames()
    club_transfer_df = data_handler.merge_df(club_df, transfer_df, 'club')
    player_club_transfer_df = data_handler.merge_df(player_df, club_transfer_df, 'player')
    player_club_transfer_df = data_handler.drop_column(player_club_transfer_df, 'uri_x')
    player_club_transfer_df = data_handler.drop_column(player_club_transfer_df, 'uri_y')
    player_club_transfer_df = pd.get_dummies(player_club_transfer_df)

    X = player_club_transfer_df
    X = X.drop('successful', 1)
    y = player_club_transfer_df['successful']
    X = SelectKBest(chi2, k=1000).fit_transform(X, y)    # selects the best features
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    prediction = Prediction(X_train, y_train.values, X_test, y_test.values)
    # print(timeit.timeit(prediction.run_random_forests, number=10))
    # print(timeit.timeit(prediction.run_naive_bayes, number=10))
    # print(timeit.timeit(prediction.run_neural_network, number=10))
    # prediction.run_naive_bayes()
    # prediction.run_random_forests()
    # prediction.run_neural_network()
    cv = cross_validation.ShuffleSplit(player_club_transfer_df.values.shape[0], n_iter=100,
                                      test_size=0.2, random_state=0)
    prediction.plot_learning_curve(MLPClassifier(), 'Learning Curves (Naive Bayes), K = 1000',
                                  X, y.values, ylim=(0.4, 1.01), cv=cv, n_jobs=1)


main()
