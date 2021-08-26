import pandas as pd
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QMessageBox

from GUI import *
from classification import *
from grid_serch_menu import GridSerch
from validation_setup import vlaidationSetup
from validetion_exeute import ValidationExecute


class MainWindowLocal:
    def __init__(self, val_win):
        self.features_clicked = False
        self.target_clicked = False
        self.gruop_clicked = False
        #
        self.val_win = val_win
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.ui.uplode_csv.clicked.connect(self.upload_file)
        self.ui.select_all_btn.clicked.connect(self.select_all)
        self.ui.featchers_btn.clicked.connect(self.features_decisions)
        self.ui.target_btn.clicked.connect(self.target_decisions)
        self.ui.groups_btn.clicked.connect(self.group_decisions)
        self.ui.find_featchers_btn.clicked.connect(self.auto_fetchers)
        self.ui.filterin_butten.clicked.connect(self.filtering)
        self.ui.SVM.click()
        self.ui.next_btn.clicked.connect(self.next)
        self.MainWindow.show()
        self._set_state = 0
        self.group = None

    def auto_fetchers(self):
        cols = self.file.columns
        for num, i in enumerate(cols):
            try:
                float(i)
                self.ui.data_tabel.item(0, num).setCheckState(2)
            except:
                pass

    def upload_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(options=options)
        if fileName:
            print(fileName)
        try:
            self.file: pd.DataFrame = pd.read_csv(fileName)
            self.ui.data_tabel.setColumnCount(self.file.shape[1])
            rows = self.file.shape[0]
            if rows > 10:
                rows = 10
            self.ui.data_tabel.setRowCount(self.file.shape[0])
            self.ui.data_tabel.setRowCount(rows)
            for row in range(rows):
                for column in range(self.file.shape[1]):
                    if row == 0:
                        item = QTableWidgetItem(str(self.file.columns[column]))
                        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                        item.setCheckState(QtCore.Qt.Unchecked)
                        self.ui.data_tabel.setItem(row, column, item)
                    else:
                        item = QTableWidgetItem(str(self.file.iloc[row, column]))
                        self.ui.data_tabel.setItem(row, column, item)
            self.ui.data_tabel.setEnabled(True)
            self.ui.data_tabel.resizeColumnsToContents()
            self.ui.label_3.setText(f"The file hes uploaded")
            # buttons active
            self.ui.select_all_btn.setEnabled(True)
            self.ui.featchers_btn.setEnabled(True)
            self.ui.target_btn.setEnabled(True)
            self.ui.groups_btn.setEnabled(True)
            self.ui.find_featchers_btn.setEnabled(True)
            self.ui.filterin_butten.setEnabled(True)
        except:
            print("An exception occurred, csv file was not found or is not readable")
            self.show_popup(text_eror=" csv file was not found or is not readable", state=1)

    def show_popup(self, text_eror=" Error ", state=1):
        dict_state = {1: "Critical", 2: "Question"}
        msg = QMessageBox()
        msg.setWindowTitle("popup message")
        msg.setText(text_eror)
        if dict_state[state] == "Critical":
            msg.setIcon(QMessageBox.Critical)
        elif dict_state[state] == "Question":
            msg.setIcon(QMessageBox.Question)
        x = msg.exec_()

    def dialog_popup(self, text="Choose Number"):
        msg = QMessageBox()
        msg.setStandardButtons((QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel))
        msg.setDefaultButton(QMessageBox.Yes)
        buttons = msg.buttons()
        buttons[0].setText("None")
        buttons[1].setText("0")
        buttons[2].setText("1")
        msg.setWindowTitle("Dialog message")
        msg.setText(text)
        msg.setIcon(QMessageBox.Question)
        button = msg.exec_()
        if button == QMessageBox.Yes:
            print("0")
            return int(0)
        elif button == QMessageBox.No:
            print("1")
            return int(1)
        elif button == QMessageBox.Cancel:
            print("np.nan")
            return np.nan

    def dialog_popup_filtering(self, text="Choose Number"):
        msg = QMessageBox()
        msg.setStandardButtons((QMessageBox.Yes | QMessageBox.No))
        msg.setDefaultButton(QMessageBox.Yes)
        buttons = msg.buttons()
        buttons[0].setText("save")
        buttons[1].setText("remove")
        msg.setWindowTitle("Dialog message")
        msg.setText(text)
        msg.setIcon(QMessageBox.Question)
        button = msg.exec_()
        if button == QMessageBox.Yes:
            return int(1)
        elif button == QMessageBox.No:
            return int(0)

    def select_all(self):
        if self._set_state == 0:
            self._set_state = 2
        else:
            self._set_state = 0
        for i in range(self.file.shape[1]):
            self.ui.data_tabel.item(0, i).setCheckState(self._set_state)

    def features_decisions(self):
        self.features_clicked = True
        vals = self._raed_index()
        self.features = self.file.loc[:, vals]
        self.ui.label_3.setText(f"feathers selected")
        self._reset_buttens()

    def target_decisions(self):
        self.target_clicked = True
        vals = self._raed_index()
        self.target = self.file.loc[:, vals]
        if self.target.shape[1] == 1:
            unique = list(pd.unique(self.target.iloc[:, 0]))
            for name in unique:
                if not (str(name) == "nan" or str(name) == '1' or str(name) == '0'):
                    replace_with = self.dialog_popup(text=str(name) + " needs to be replaced by 1 or 0")
                    self.target = self.target.replace(to_replace=name, value=replace_with)
        self.ui.label_3.setText(f"target selected")
        self._reset_buttens()

    def filtering(self):
        vals = self._raed_index()
        vals = self.file.columns[vals].values
        tamp = self.file[vals]
        unique = pd.unique(np.squeeze(tamp.values))
        for name in unique:
            if not (str(name) == "nan" or str(name) == '1' or str(name) == '0'):
                replace_with = self.dialog_popup_filtering(text=str(name) + " needs to be replaced by 1 or 0")
                tamp = tamp.replace(to_replace=name, value=replace_with)
        tamp = np.where(tamp.values == 1)[0]
        if self.target_clicked:
            self.target = self.target.iloc[tamp,:]

        if self.features_clicked:
            self.features = self.features.iloc[tamp, :]
        if self.gruop_clicked:
            self.group=self.group.iloc[tamp,:]
        self.file = self.file.iloc[tamp, :]
        self._reset_buttens()

    def group_decisions(self):
        self.gruop_clicked=True
        vals = self._raed_index()
        self.group = self.file.loc[:, vals]
        self.ui.label_3.setText(f"group selected")
        self._reset_buttens()

    def _reset_buttens(self):
        for i in range(self.file.shape[1]):
            self.ui.data_tabel.item(0, i).setCheckState(0)
        if self.target_clicked and self.features_clicked:
            self.ui.next_btn.setEnabled(True)

    def _classifier_decision(self):
        if self.ui.SVM.isChecked():
            model = "svm"
        elif self.ui.random_forest.isChecked():
            model = "random"
        elif self.ui.XGboost.isChecked():
            model = "xgboost"
        elif self.ui.baiv_gussian.isChecked():
            model = "gauss"
        elif self.ui.LG_reulated.isChecked():
            model = "logistic_regression_regulated"
        elif self.ui.LG.isChecked():
            model = "logistic_regression"
        elif self.ui.LDA.isChecked():
            model = "LDA"
        return model

    def next(self):
        print(self.target.iloc[:, 0].value_counts(ascending=True))
        if self.features.empty:
            print("No features selected")
            self.show_popup(text_eror="No features selected", state=1)
        elif self.target.empty:
            print("No target selected")
            self.show_popup(text_eror="No target selected", state=1)
        elif self.target.shape[1] > 1:
            print("More then 1 target selected")
            self.show_popup(text_eror="More then 1 target selected", state=1)
        else:
            model = self._classifier_decision()
            model_ml = Classification(features=self.features.copy(), target=self.target.copy(), group=self.group,
                                      model=model)
            model_ml.limit_cores(os.cpu_count() - 2)
            self.val_win.MainWindow.show()
            self.val_win.set_model(model_ml)
            self.MainWindow.close()

    def _raed_index(self):
        vals = []
        for i in range(self.file.shape[1]):
            item = self.ui.data_tabel.item(0, i).checkState()
            if item == 2:
                vals.append(True)
            else:
                vals.append(False)
        return vals


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    model4 = ValidationExecute()
    model3 = GridSerch(model4)
    model2 = vlaidationSetup(model3)
    model = MainWindowLocal(model2)
    # model2.MainWindow.show()

    app.exec()
    # sys.exit(app.exec_())
    # sys.exit(model.app.exec_())
