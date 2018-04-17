from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV
from examples import load_data
import pandas as pd
from proactive_forest.estimator import DecisionForestClassifier, ForestClassifier


if __name__ == '__main__':

    data_name = 'test_db_1'
    X, y = load_data.load_test_db_1()

    rf_b = DecisionForestClassifier(n_estimators=100, criterion='gini', max_features='log', bootstrap=True)
    et_b = DecisionForestClassifier(n_estimators=100, criterion='gini', max_features='all', bootstrap=True, split='rand')
    pf_b = ForestClassifier(n_estimators=100, criterion='gini', max_features='log', bootstrap=True, alpha=0.5)

    rf = cross_val_score(rf_b, X, y, cv=10)
    et = cross_val_score(et_b, X, y, cv=10)
    pf = cross_val_score(pf_b, X, y, cv=10)

    data = pd.DataFrame(index=['RF', 'ET', 'PF'])

    data['CV Acc. Mean'] = pd.Series([rf.mean(), et.mean(), pf.mean()], index=['RF', 'ET', 'PF'])
    data['CV Acc. Std'] = pd.Series([rf.std(), et.std(), pf.std()], index=['RF', 'ET', 'PF'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

    rf_b.fit(X_train, y_train)
    et_b.fit(X_train, y_train)
    pf_b.fit(X_train, y_train)

    data['PCD Diversity'] = pd.Series([rf_b.diversity_measure(X_test, y_test),
                                       et_b.diversity_measure(X_test, y_test),
                                       pf_b.diversity_measure(X_test, y_test)], index=['RF', 'ET', 'PF'])

    data['QStat Diversity'] = pd.Series([rf_b.diversity_measure(X_test, y_test, type='qstat'),
                                         et_b.diversity_measure(X_test, y_test, type='qstat'),
                                         pf_b.diversity_measure(X_test, y_test, type='qstat')],
                                        index=['RF', 'ET', 'PF'])

    data['Forest Acc.'] = pd.Series([accuracy_score(y_test, rf_b.predict(X_test)),
                                     accuracy_score(y_test, et_b.predict(X_test)),
                                     accuracy_score(y_test, pf_b.predict(X_test))], index=['RF', 'ET', 'PF'])

    rf_weight = rf_b.trees_mean_weight()
    et_weight = et_b.trees_mean_weight()
    pf_weight = pf_b.trees_mean_weight()

    data['Tree Weight Mean'] = pd.Series([rf_weight, et_weight, pf_weight], index=['RF', 'ET', 'PF'])

    print(data)

