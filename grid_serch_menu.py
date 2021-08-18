from GUI_3 import *
from classification import *
from PyQt5.QtWidgets import QTableWidgetItem


class GridSerch:
    def __init__(self,val_exact):
        self.val_exact=val_exact
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.ui.grid_search.clicked.connect(self._grid_search)
        self.ui.modal_modulation.clicked.connect(self._modal_modulation)
        self.ui.K_folds_nested_btn.clicked.connect(self._nested)
        self.ui.LLR.click()
        # self.ui.next.clicked.connect(self._next)

    def set_model(self, model):
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
                continue
            tamp_list = []
            if tamp[0] == "[" and tamp[-1] == "]":
                tamp = tamp[1:-1].split(",")
                for j in tamp:
                    j = self.typs[num](j)
                    tamp_list.append(j)
                for_grid.append((hiper_parms[num], tamp_list))
            else:
                tamp = self.typs[num](tamp)
                for_grid.append((hiper_parms[num], tamp))
        self.model.set_global_setting(for_grid)


        features_list=self.ui.nested_le.text()
        if features_list[0]=="[":
            features_list=features_list[1:]
        if features_list[-1]=="]":
            features_list=features_list[:-1]
        features_list=features_list.split(",")
        for num,i in enumerate(features_list):
            features_list[num]=int(i)
        num_features,params_dic=self.model.K_folds_nested(N_features=features_list,number_of_folds=int(self.ui.K_folds_num.text()),method=method)
        print(num_features)
        print(params_dic)


    def _grid_search(self):
        k_folds=int(self.ui.K_folds_num.text())
        core_lim = int(self.ui.core_lim.text())
        self.model.grid_search_k_folds(k_folds=k_folds,multi_proses=core_lim)
        hiper_parms = list(self.model.model.get_params().keys())
        for_grid=[]
        for num,i in enumerate(self.typs):
            tamp=self.ui.param_tabel.item(0,num).text()
            if tamp=="None":
                continue
            tamp_list=[]
            if tamp[0]=="[" and tamp[-1]=="]":
                tamp=tamp[1:-1].split(",")
                for j in tamp:
                    j=self.typs[num](j)
                    tamp_list.append(j)
                for_grid.append((hiper_parms[num],tamp_list))
            else:
                tamp=self.typs[num](tamp)
                for_grid.append((hiper_parms[num],tamp))
        self.model.grid_search(tuple(for_grid))
        self._next()

    def _modal_modulation(self):
        hiper_parms = list(self.model.model.get_params().keys())
        for_modolation = []
        for num, i in enumerate(self.typs):
            tamp = self.ui.param_tabel.item(0, num).text()
            if tamp == "None":
                continue
            tamp = self.typs[num](tamp)
            for_modolation.append((hiper_parms[num], tamp))
        self.model.model_modulation(for_modolation)
        self._next()

    def _next(self):
        self.val_exact.MainWindow.show()
        self.val_exact.set_model(self.model)
        self.MainWindow.close()

