from PyQt5.QtWidgets import QFileDialog

from GUI_4 import *
from classification import *


class ValidationExecute:

    def __init__(self):

        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.ui.leave_one_out.click()
        self.ui.K_folds_le.setText(str(5))
        self.ui.test_size_le.setText(str(0.7))
        self.ui.save_url_btn.clicked.connect(self._save_url)
        self.ui.save_model_btn.clicked.connect(self._save_model)
        self.ui.LLR.click()
        self.ui.train.clicked.connect(self._train)
        self.ui.maximum_delta_input.setText(str(0.2))
        self.ui.tpr_low_band_input.setText(str(0.5))
        self.ui.find_work_point_btn.setEnabled(False)
        self.ui.find_work_point_btn.clicked.connect(self.find_work_point)

    def set_model(self, model):
        """
        setting the classification model
        :param model: the model that defines in the last screen (type: Classification)
        :return:
        """
        self.model: Classification = model
        self.ui.model_name.setText(self.model.model_name)

    def _train(self):
        """
        train the model by validation that chosen
        :return:
        """
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
            text = open(self.ui.class_report_le.text() + ' .txt').read()
            self.ui.plainTextEdit_panel.setPlainText(text)
        if self.ui.ROC_le.text() != '':
            self.model.show_roc(self.ui.ROC_le.text())
        if self.ui.weitse.text() != '':
            self.model.save_classification_probability(self.ui.weitse.text())
        if self.ui.det_le.text() != '':
            self.model.show_det(self.ui.det_le.text())
        self.ui.find_work_point_btn.setEnabled(True)

    def _save_url(self):
        """
        set where to save the report files and the trained model
        :return:
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getExistingDirectory(options=options)
        os.chdir(fileName)
        self.ui.reports.setEnabled(True)

    def find_work_point(self):
        """
        find the best work point on the roc cerv
        :return:
        """
        plt.close()
        if self.ui.ROC_le.text() != '':
            name = self.ui.ROC_le.text()
        else:
            name = None
        repo, _ = self.model.optimal_cut_point_on_roc_(delta_max=float(self.ui.maximum_delta_input.text()),
                                                       tpr_low_bound=float(self.ui.tpr_low_band_input.text()),
                                                       name=name)
        consol = Console(color_system="windows")
        consol.print("[green] beast acurecy point report:")
        print(repo)

    def _save_model(self):
        """
        use all the data and crating a permanent model for classification
        :return:
        """
        self.model.save_model(self.ui.model_name.text())
