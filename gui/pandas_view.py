import os
import numpy as np
import pandas as pd
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from customexceptions import *

class pandasModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        QtCore.QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None
    
    def setData(self, index, value, role):
        if role == Qt.EditRole:#set role to edit
            
            if value==str(0):   #deal with zero error
                value = np.int64(0)

            self._data.iloc[index.row(), index.column()] = value    #set new values
            self._data.to_hdf("temp.hdf5","data")   #save to a temporary .hdf5 file
            return True
        return False
    
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
    
class PandasWidget(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.parent = parent
        self.view = QtWidgets.QTableView()
        self.model = pandasModel(pd.DataFrame())
        self.view.setModel(self.model)
        lay = QtWidgets.QVBoxLayout()
        lay.addWidget(self.view)
        button_layout = QtWidgets.QHBoxLayout()

        close_button = QtWidgets.QPushButton("Close", self)#close df
        save_to_csv_button = QtWidgets.QPushButton("Save", self)#save df to csv
        add_row_button = QtWidgets.QPushButton("Add Row", self)#add row to df
        delete_row_button = QtWidgets.QPushButton("Delete Row", self)#delete row in df
        
        button_layout.addWidget(close_button)
        button_layout.addWidget(save_to_csv_button)
        button_layout.addWidget(add_row_button)
        button_layout.addWidget(delete_row_button)

        close_button.clicked.connect(self.close_button_clicked)
        save_to_csv_button.clicked.connect(self.save_button_clicked)
        add_row_button.clicked.connect(self.add_row_clicked)
        delete_row_button.clicked.connect(self.delete_row_clicked)

        lay.addLayout(button_layout)
        self.setLayout(lay)
        self.view.show()
        self.setWindowTitle('df')
        w = int(self.parent.screen_size.width() / 2)
        h = int(self.parent.screen_size.height() / 1.5)
        self.resize(w, h)
        self.move(int(0.975*w),int(h/5))
        
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.parent.pandas_button.setChecked(False)
        return super().closeEvent(a0)
    
    def close_button_clicked(self):
        self.hide()
        self.parent.pandas_button.setChecked(False)
        
    def save_button_clicked(self):
        options = QtWidgets.QFileDialog.Options()
        directory = os.path.split(self.filename)[0]
        name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save to csv", directory, "csv (*.csv)")
        name = name.split('.')[0]+'.csv'
        self.df.to_csv(name)

    def add_row_clicked(self):
        print("Adding row to DataFrame.")
        new_row = 0
        new_item = pd.DataFrame(self.df.iloc[[new_row]])  #df to be added
        self.df = pd.concat([self.df, new_item], ignore_index=True).sort_values("particle")  #add to whole df
        model = pandasModel(self.df)    #update displayed df in window
        self.view.setModel(model)
        self.view.selectRow(new_row)  #select added row
        print("Row added.")

    def delete_row_clicked(self):
        print("Deleting selected row in Dataframe")
        old_row = 0 #row to be deleted
        self.df = self.df.drop(old_row) #delete row from df
        model = pandasModel(self.df)   #update df
        self.view.setModel(model)

        
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def update_file(self, filename, frame):
        self.filename = filename
        try:
            df = pd.read_hdf(filename).sort_values("particle")    
            print(df.head())        
            if 'frame' in df.columns:
                df2 = df[df.index == frame]    
            else:
                df2 = df.reset_index()
        except Exception as e:
            self.df = pd.DataFrame()
            raise PandasViewError(e)
        self.df=df2
        model = pandasModel(df2)
        self.view.setModel(model)

