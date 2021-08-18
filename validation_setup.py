import numpy as np
from PyQt5.QtWidgets import QFileDialog

from GUI_2 import *
from classification import *


class vlaidationSetup:
    def __init__(self, grd_win):
        self.grd_win = grd_win
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.ui.sgf_btn.clicked.connect(self._sgf)
        self.ui.normalizetion_btn.clicked.connect(self._norm)
        self.ui.offset_btn.clicked.connect(self._offset)
        self.ui.opus_normalizetion.clicked.connect(self._opus_normalization)
        self.ui.lode_feturs.clicked.connect(self._load_features)
        self.ui.show_features.clicked.connect(self._show_features)
        self.ui.next_btn.clicked.connect(self._next)
        self.ui.chi2_input.textChanged.connect(self.sync_pca_lineEdit)

        # self.ui.pushButton.clicked.connect(self.set_model)
        # self.MainWindow.show()

    def set_model(self, model):
        self.model: Classification = model
        self.ui.model_label.setText(self.model.model_name)
        self.ui.model_label.adjustSize()
        self.ui.pca_input.setText(str(self.model.features_size))
        self.ui.chi2_input.setText(str(self.model.features_size))

    def _sgf(self):
        div = self.ui.sgf_div.text()
        self.model.preprocessing(["sgf"], derivative=int(div))
        self.ui.label.setText("sgf")

    def _norm(self):
        self.model.preprocessing(["norm"])
        self.ui.label.setText("norm")

    def _offset(self):
        self.model.preprocessing(["offset"])
        self.ui.label.setText("offset")

    def _opus_normalization(self):
        self.model.preprocessing(["opus_normalization"])
        self.ui.label.setText("opus_normalization")

    def _load_features(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(options=options)
        index = np.load(fileName)
        self.model.uploader_feature(index)

    def _show_features(self):
        self.model.show_features()

    def sync_pca_lineEdit(self):
        self.ui.pca_input.setText(self.ui.chi2_input.text())

    def _next(self):
        if int(self.ui.chi2_input.text()) < int(self.model.features_size):
            fet = self.model.feature_selection(int(self.ui.chi2_input.text()))
            if self.ui.save_features.checkState() == 2:
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog
                fileName, _ = QFileDialog.getSaveFileName(options=options)
                np.save(fileName, fet)
        if int(self.model.features_size) > int(self.ui.pca_input.text()) > int(
                self.ui.chi2_input.text()):
            pca = int(self.ui.pca_input.text())
        else:
            pca = 0
        if self.ui.bootstrap.checkState() == 2:
            bootstrap = True
        else:
            bootstrap = False
        if self.ui.smote.checkState() == 2:
            smote = True
        else:
            smote = False
        if self.ui.standart_scaling.checkState() == 2:
            str_scl = True
        else:
            str_scl = False
        self.model.in_training_process(standart_scaling=str_scl, pca=pca, bootstrap=bootstrap, smoote=smote)
        self.MainWindow.close()
        self.grd_win.MainWindow.show()
        self.grd_win.set_model(self.model)
