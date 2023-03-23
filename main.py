import sys
import os
from PyQt5 import QtWidgets
from PyQt5 import QtCore


class SelectASCIIFiles(QtWidgets.QMainWindow):
    FILE_FILTER = 'Maya ASCII (*.ma)'

    def __init__(self, parent=None):
        super(SelectASCIIFiles, self).__init__(parent)

        self.setWindowTitle('Maya ASCII Reader')
        self.setGeometry(100, 100, 1250, 400)

        self.table_wdg = QtWidgets.QTableWidget(self)
        self.setCentralWidget(self.table_wdg)
        self.table_wdg.setColumnCount(4)
        self.table_wdg.setColumnWidth(0, 150)
        self.table_wdg.setColumnWidth(1, 150)
        self.table_wdg.setColumnWidth(2, 70)
        self.table_wdg.setColumnWidth(3, 300)
        #self.table_wdg.setColumnWidth(4, 300)
        self.table_wdg.setHorizontalHeaderLabels(['File Name', 'Reference Name', 'Loaded', 'File Path'])

        dock = QtWidgets.QDockWidget('ASCII Load')
        dock.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, dock)
        form = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout(form)
        form.setLayout(layout)

        self.btn_layout = QtWidgets.QHBoxLayout()
        self.ok_btn = QtWidgets.QPushButton('OK')
        self.cancel_btn = QtWidgets.QPushButton('Cancel')
        self.btn_layout.addWidget(self.ok_btn)
        self.btn_layout.addWidget(self.cancel_btn)
        self.browse_btn = QtWidgets.QPushButton('Browse')
        layout.addRow('Browse ASCII Files:', self.browse_btn)
        #layout.addWidget( self.browse_btn)
        dock.setWidget(form)

        self.create_connections()

    def create_connections(self):
        self.browse_btn.clicked.connect(self.getfiles)



    def getfiles(self):
        file_path = QtWidgets.QFileDialog.getOpenFileNames(self, "Select File", "", self.FILE_FILTER)
        if file_path:
            self.get_file_name(file_path[0])

    def get_file_name(self, file_lst):
        row_counter = 0

        for i in range(len(file_lst)):
            ref_counter = 0
            name = os.path.basename(file_lst[i])
            ext = os.path.splitext(file_lst[i])[-1]
            base = os.path.splitext(file_lst[i])[0]
            directory = os.path.dirname(file_lst[i])

            f = open(file_lst[i], 'r')  # 'r' = read

            for line in f:
                if line.startswith('file -r '):
                    ref_counter = 1
                    self.table_wdg.insertRow(row_counter)
                    item = QtWidgets.QTableWidgetItem(name)
                    self.table_wdg.setItem(row_counter, 0, item)
                    item = QtWidgets.QTableWidgetItem(file_lst[i])
                    self.table_wdg.setItem(row_counter, 3, item)
                    ref_name = line.split('"')[1]
                    item = QtWidgets.QTableWidgetItem(ref_name)
                    self.table_wdg.setItem(row_counter, 1, item)

                    if line.find('-dr 1'):
                        ref_load = 'No'
                        item = QtWidgets.QTableWidgetItem(ref_load)
                        self.table_wdg.setItem(row_counter, 2, item)
                    else:
                        ref_load = 'Yes'
                        item = QtWidgets.QTableWidgetItem(ref_load)
                        self.table_wdg.setItem(row_counter, 2, item)
                    row_counter += 1
            if ref_counter == 0:
                self.table_wdg.insertRow(row_counter)
                item = QtWidgets.QTableWidgetItem(name)
                self.table_wdg.setItem(row_counter, 0, item)
                item = QtWidgets.QTableWidgetItem(file_lst[i])
                self.table_wdg.setItem(row_counter, 3, item)


            f.close()

#class TableView(QtWidgets.QTableWidget):

def main():
   app = QtWidgets.QApplication(sys.argv)
   ex = SelectASCIIFiles()
   ex.show()
   sys.exit(app.exec_())


if __name__ == '__main__':
    main()
