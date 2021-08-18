import os

from GUI_4 import *
from classification import *
from PyQt5.QtWidgets import QFileDialog

class ValidationExecute:

    def __init__(self):

        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.ui.leave_one_out.click()
        self.ui.K_folds_le.setText(str(5))
        self.ui.test_size_le.setText(str(0.7))
        self.ui.save_url_btn.clicked.connect(self._save_url)
        self.ui.LLR.click()
        self.ui.train.clicked.connect(self._train)

    def set_model(self, model):
        self.model: Classification = model

    def _train(self):
        if self.ui.LLR.isChecked():
            method = "most_likelihoods"
        elif self.ui.majorety_vote.isChecked():
            method = "majority_vote"
        elif self.ui.no_vote.isChecked():
            method = "no_vote"

        if self.ui.leave_one_out.isChecked():
            self.model.leave_one_out(method=method)
        elif self.ui.kfolds.isChecked():
            number_of_folds = int(self.ui.K_folds_le.text())
            self.model.K_folds(number_of_folds=number_of_folds, method=method)
        elif self.ui.K_fold_stretefide.isChecked():
            number_of_folds = int(self.ui.K_folds_le.text())
            self.model.K_folds_stratified(number_of_folds=number_of_folds, method=method)
        elif self.ui.train_test_split.isChecked():
            test_size = float(self.ui.test_size_le.text())
            self.model.train_test_split(test_size=test_size, method=method)
        if self.ui.class_report_le.text() != '':
            self.model.save_classification_report(self.ui.class_report_le.text())
        if self.ui.ROC_le.text() != '':
            self.model.show_roc(self.ui.ROC_le.text())
        if self.ui.weitse.text() != '':
            self.model.save_classification_probability(self.ui.weitse.text())
        if self.ui.det_le.text() != '':
            self.model.show_det(self.ui.det_le.text())

    def _save_url(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getExistingDirectory(options=options)
        os.chdir(fileName)
