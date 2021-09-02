from GUI_3 import *
from classification import *
from PyQt5.QtWidgets import QTableWidgetItem
import webbrowser


def _respond_none(given):
    """
    respons to case thet the original ype was None
    :param given: the value tet input in the hyper parameters table (type: unknown that why we have that program)
    :return:
    """
    try:
        given = int(given)
    except Exception:
        try:
            given = float(given)
        except Exception:
            try:
                given = str(given)
            except Exception:
                given = None
    return given


class GridSerch:
    def __init__(self, val_exact):
        self.val_exact = val_exact
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.ui.grid_search.clicked.connect(self._grid_search)
        self.ui.modal_modulation.clicked.connect(self._modal_modulation)
        self.ui.K_folds_nested_btn.clicked.connect(self._nested)
        self.ui.LLR.click()
        self.ui.skylearn_help_btn.clicked.connect(self._skylearn_help)
        # self.ui.next.clicked.connect(self._next)

    def set_model(self, model):
        """
        setting the classification model
        :param model: the model that defines in the last screen (type: Classification)
        :return:
        """
        self.model: Classification = model
        hiper_parms = list(self.model.model.get_params().keys())
        parms = list(self.model.model.get_params().values())
        self.ui.param_tabel.setColumnCount(len(hiper_parms))
        self.ui.K_folds_num.setText(str(PreProcess._K_FOLDS))
        self.ui.core_lim.setText(str(PreProcess._MALTY_PROCESSES))
        self.ui.nested_le.setText(str(self.model.features_size))
        self.ui.param_tabel.setHorizontalHeaderLabels(hiper_parms)
        self.ui.param_tabel.setRowCount(1)
        self.typs = []
        for num, i in enumerate(parms):
            self.typs.append(type(i))
            item = QTableWidgetItem(str(i))
            self.ui.param_tabel.setItem(0, num, item)

    def _nested(self):
        """
        using K fold nested validation on the data set to determn the hiper parmeter and the number of faetures
        :return:
        """
        if self.ui.LLR.isChecked():
            method = "most_likelihoods"
        elif self.ui.majorety_vote.isChecked():
            method = "majority_vote"
        elif self.ui.no_vote.isChecked():
            method = "no_vote"

        hiper_parms = list(self.model.model.get_params().keys())
        for_grid = []
        for num, i in enumerate(self.typs):
            tamp = self.ui.param_tabel.item(0, num).text()
            if tamp == "None":
                for_grid.append((hiper_parms[num], None))
                continue
            tamp_list = []
            if tamp[0] == "[" and tamp[-1] == "]":
                tamp = tamp[1:-1].split(",")
                for j in tamp:
                    if self.typs[num] == type(None):
                        j = _respond_none(j)
                    else:
                        j = self.typs[num](j)
                    tamp_list.append(j)
                for_grid.append((hiper_parms[num], tamp_list))
            else:
                if self.typs[num] == type(None):
                    tamp = _respond_none(tamp)
                else:
                    tamp = self.typs[num](tamp)
                for_grid.append((hiper_parms[num], tamp))
        self.model.set_global_setting(for_grid)

        features_list = self.ui.nested_le.text()
        if features_list[0] == "[":
            features_list = features_list[1:]
        if features_list[-1] == "]":
            features_list = features_list[:-1]
        features_list = features_list.split(",")
        for num, i in enumerate(features_list):
            features_list[num] = int(i)
        num_features, params_dic = self.model.K_folds_nested(N_features=features_list,
                                                             number_of_folds=int(self.ui.K_folds_num.text()),
                                                             method=method)

    def _grid_search(self):
        """
        using grid search on the data set to determine the hyper parameters and move to the next screen
        :return:
        """
        k_folds = int(self.ui.K_folds_num.text())
        core_lim = int(self.ui.core_lim.text())
        self.model.grid_search_k_folds(k_folds=k_folds, multi_proses=core_lim)
        hiper_parms = list(self.model.model.get_params().keys())
        for_grid = []
        for num, i in enumerate(self.typs):
            tamp = self.ui.param_tabel.item(0, num).text()
            if tamp == "None":
                for_grid.append((hiper_parms[num], None))
                continue
            tamp_list = []
            if tamp[0] == "[" and tamp[-1] == "]":
                temp_list = tamp[1:-1].split(",")
                for j in temp_list:
                    if self.typs[num] == type(None):
                        j = _respond_none(j)
                    else:
                        j = self.typs[num](j)
                    tamp_list.append(j)
                for_grid.append((hiper_parms[num], tamp_list))
            else:
                if self.typs[num] == type(None):
                    tamp = _respond_none(tamp)
                else:
                    tamp = self.typs[num](tamp)
                for_grid.append((hiper_parms[num], tamp))
        self.model.grid_search(tuple(for_grid))
        self._next()

    def _modal_modulation(self):
        """
        modulate the hyper parameters im the classifier and move to the next screen
        :return:
        """
        hiper_parms = list(self.model.model.get_params().keys())
        for_modolation = []
        for num, i in enumerate(self.typs):
            tamp = self.ui.param_tabel.item(0, num).text()
            if tamp == "None":
                for_modolation.append((hiper_parms[num], None))
                continue
            if self.typs[num] == type(None):
                tamp = _respond_none(tamp)
            else:
                tamp = self.typs[num](tamp)
            for_modolation.append((hiper_parms[num], tamp))
        self.model.model_modulation(for_modolation)
        self._next()

    def _next(self):
        """
        move to the next screen
        :return:
        """
        self.val_exact.MainWindow.show()
        self.val_exact.set_model(self.model)
        self.MainWindow.close()

    def _skylearn_help(self):
        """
        open help on the chosen classifier
        :return:
        """
        if self.model.model_name == "XGBoost":
            webbrowser.open('https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html')
        elif self.model.model_name == "Gaussian Naive Bayes":
            webbrowser.open('https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html')
        elif self.model.model_name == "support vector machine":
            webbrowser.open('https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html')
        elif self.model.model_name == "random_forest":
            webbrowser.open('https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html')
        elif self.model.model_name == "logistic regression":
            webbrowser.open('https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html')
        elif self.model.model_name == "logistic regression":
            webbrowser.open('https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html')
        elif self.model.model_name == "LDA":
            webbrowser.open('https://scikit-learn.org/stable/modules/generated/sklearn.discriminant_analysis.LinearDiscriminantAnalysis.html')