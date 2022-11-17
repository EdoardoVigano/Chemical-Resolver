import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
# from PyQt5.QtCore import Qt
from PIL import Image
import pandas as pd
import style
from utils import *
from rdkit import Chem
from rdkit.Chem import Draw
from propertiesCalculation import *
# import statistics 

global chemImg, identifier, value, flag1, dataset_out
chemImg = 0
identifier = 0
value = ''
flag1 = 0
dataset_out = pd.DataFrame()

if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

class Main(QMainWindow):

    def __init__(self):
        super().__init__()     
        self.setWindowTitle("Chemical Resolver 2.0")
        self.setWindowIcon(QIcon("icons/IMG.jpg"))
        self.setGeometry(50, 50, 1000, 650)
        self.setFixedSize(self.size())
        global progressBar
        progressBar = QProgressBar()
        self.flag = 0
        self.flag2 = 0
        self.statCalc = 0
        self.target = []
        self.propertyCheck_list = []
        self.threadpool = QThreadPool()
        self.UI()
        self.show()

    def UI(self):
        self.toolbar()
        self.tabWidget()
        self.widgets()
        self.layouts()
        self.identifierDisplayInput()
        self.identifierDisplayOutput()
        self.propertiesDysplay()
        self.statisticDysplay()

    def toolbar(self):
        self.tb = self.addToolBar("Tool Bar")
        self.loadFile = QAction("Load File", self)
        self.tb.addAction(self.loadFile)
        self.loadFile.triggered.connect(self.funcLoadFile)
        self.tb.addSeparator()
        self.saveFile = QAction("Save File", self)
        self.tb.addAction(self.saveFile)
        self.saveFile.triggered.connect(self.funcSaveFile)
        self.tb.addSeparator()
        self.info = QAction("Info", self)
        self.tb.addAction(self.info)
        self.info.triggered.connect(self.funcInfo)
        self.tb.addSeparator()
        self.cleanAll = QAction("Clean Work", self)
        self.tb.addAction(self.cleanAll)
        self.cleanAll.triggered.connect(self.cleanWork)

    def tabWidget(self):
        self.tabs = QTabWidget()
        self.tabs.blockSignals(True)
        self.tabs.currentChanged.connect(self.identifierDisplayInput)
        self.tabs.currentChanged.connect(self.identifierDisplayOutput)
        self.tabs.currentChanged.connect(self.propertiesDysplay)
        self.tabs.currentChanged.connect(self.statisticDysplay)
        self.setCentralWidget(self.tabs)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tabs.addTab(self.tab1, 'Chemicals Input')
        self.tabs.addTab(self.tab2, 'Chemicals Output')
        self.tabs.addTab(self.tab3, "Physico-Chemical Properties")
        self.tabs.addTab(self.tab4, "Statistic")
        
    def widgets(self):
        ######################### widgets tab1 ################################
        self.chemicalsInputTable = QTableWidget()
        self.chemicalsInputTable.setColumnCount(1)
        self.chemicalsInputTable.setHorizontalHeaderItem(0, QTableWidgetItem('Chemicals Input'))
        self.chemicalsInputTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.chemicalsInputTable.doubleClicked.connect(self.searchChemicalsDoubleClick)
        self.addChemicalsInLine = QLineEdit()
        self.addChemicalsInLine.setPlaceholderText('Write here your chemical')
        self.btnAddChemicals = QPushButton('Add Chemicals')
        self.btnAddChemicals.clicked.connect(self.funcAddChemicals)
        #### right Img ####
        size = (725, 250)
        path = os.getcwd()
        path = os.path.join(path, "img\IMG1.jpg")
        # img = Image.open(path)
        # img = img.resize(size)
        # img.save(path)
        self.rightImg = QLabel()
        self.img_ = QPixmap(path)
        self.rightImg.setPixmap(self.img_)
        #### right top ###
        self.searchEntry = QLineEdit()
        self.searchEntry.setPlaceholderText("Search your chemicals")
        self.searchEntryBtn = QPushButton("Search Chemical")
        self.searchEntryBtn.clicked.connect(self.searchChemicals)
        ### right middle ###  
        self.identifierComboIn = QComboBox()
        self.identifierComboIn.addItems(['SELECT', 'NAME', 'SMILES','INCHI','CAS'])
        self.checkBtnName = QCheckBox('NAME')
        self.checkBtnSmiles = QCheckBox('SMILES')
        self.checkBtnInchi = QCheckBox('INCHI')
        self.checkBtnCas = QCheckBox('CAS')
        #### right bottom ###
        self.startBtn = QPushButton("Start Resolver")
        self.startBtn.clicked.connect(self.startCalculation)
        ######################### widgets tab2 ################################
        ######################### widgets tab2 ################################
        self.chemicalsOutTable = QTableWidget()
        self.showResultsBtn = QPushButton('Show Results')
        self.showResultsBtn.clicked.connect(self.functShowResults)
        ######################### widgets tab3 ################################
        ######################### widgets tab3 ################################
        self.propertyTable = QTableWidget()
        self.propertyBtn = QPushButton('Start calculation')
        self.propertyBtn.clicked.connect(self.functPropertyBtn)
        self.saveDescriptorsBtn = QPushButton("Save descriptors")
        self.saveDescriptorsBtn.clicked.connect(self.functSaveDescriptors)
        self.propertyMW = QCheckBox("Molecular Weight")
        self.propertyNumAromaticRing = QCheckBox("NumAromaticRing")
        self.propertyNumHAcceptors = QCheckBox("NumHAcceptors")
        self.propertyNumHDonors = QCheckBox("NumHDonors")
        self.propertyLogP = QCheckBox("LogP")
        self.propertyMaxPartialCharge = QCheckBox("MaxPartialCharge")
        self.propertyMinPartialCharge = QCheckBox("MinPartialCharge")
        self.propertyAll = QCheckBox("All")
        ######################### widgets tab4 ################################
        ######################### widgets tab4 ################################
        self.statisticsTable = QTableWidget()
        self.statisticsCalculationBtn = QPushButton('Statistics Calculation')
        self.statisticsCalculationBtn.clicked.connect(self.functStatisticsCalculation) 


    def layouts(self):
        global progressBar
        ################### layouts tab1 #############################
        ########## main ##################
        self.mainLayoutTab1 = QHBoxLayout()
        ##### left #####
        self.leftLayoutTab1 = QVBoxLayout()
        self.leftLayoutTab1.addWidget(self.chemicalsInputTable)
        self.leftLayoutTab1.addWidget(self.addChemicalsInLine)
        self.leftLayoutTab1.addWidget(self.btnAddChemicals)
        #################### right #########################
        ######### right main ###########
        self.rightLayoutTab1 = QVBoxLayout()
        # self.rightLayoutTab1.addWidget(self.rightImg) 
        ######### right Top ############
        self.rightLayoutIMGTab1 = QVBoxLayout()
        self.rightLayoutIMGTab1.addWidget(self.rightImg) 
        self.IMGFrameTab1 = QFrame()
        self.IMGFrameTab1.setLayout(self.rightLayoutIMGTab1)
        self.IMGFrameTab1.setStyleSheet(style.IMGFrameTab1())
        # search + botton
        # vertical 1
        self.rightTopLayoutTab1 = QHBoxLayout()
        self.rightTopLayoutTab1.addWidget(self.searchEntry, 90)
        self.rightTopLayoutTab1.addWidget(self.searchEntryBtn, 10)
        self.groupSearchRightTab1 = QGroupBox("Search Box")
        self.groupSearchRightTab1.setLayout(self.rightTopLayoutTab1)
        # self.groupSearchRightTab1.setStyleSheet(style.groupSearchRightTab1Style())
        ######### right middle ##########
        # 2 vertical in un orizontal (idetifier input e output)   
        self.rightmiddleLayoutInputTab1 = QVBoxLayout()
        self.rightmiddleLayoutOutTab1 = QVBoxLayout()
        self.rightMiddleIdentifierTab1 = QHBoxLayout()
        self.rightmiddleLayoutInputTab1.addWidget(self.identifierComboIn)
        self.checkLayoutOutNameIchiTab1 = QHBoxLayout()
        self.checkLayoutOutNameIchiTab1.addWidget(self.checkBtnName)
        self.checkLayoutOutNameIchiTab1.addWidget(self.checkBtnInchi)
        self.checkLayoutOutNameIchiTab1Group = QGroupBox()
        self.checkLayoutOutNameIchiTab1Group.setLayout(self.checkLayoutOutNameIchiTab1)
        self.checkLayoutOutSmilesCasTab1 = QHBoxLayout()
        self.checkLayoutOutSmilesCasTab1.addWidget(self.checkBtnSmiles)
        self.checkLayoutOutSmilesCasTab1.addWidget(self.checkBtnCas)
        self.checkLayoutOutSmilesCasTab1Group = QGroupBox()
        self.checkLayoutOutSmilesCasTab1Group.setLayout(self.checkLayoutOutSmilesCasTab1)
        self.rightmiddleLayoutOutTab1.addWidget(self.checkLayoutOutNameIchiTab1Group)
        self.rightmiddleLayoutOutTab1.addWidget(self.checkLayoutOutSmilesCasTab1Group)
        self.groupRightmiddleLayoutInputTab1 = QGroupBox("Inputs Identifier")
        self.groupRightmiddleLayoutInputTab1.setLayout(self.rightmiddleLayoutInputTab1)
        # self.groupRightmiddleLayoutInputTab1.setStyleSheet(style.groupRightmiddleLayoutInputTab1Style())
        self.groupRightmiddleLayoutOutTab1 = QGroupBox("Output Identifier")
        self.groupRightmiddleLayoutOutTab1.setLayout(self.rightmiddleLayoutOutTab1)
        self.rightMiddleIdentifierTab1.addWidget(self.groupRightmiddleLayoutInputTab1)
        self.rightMiddleIdentifierTab1.addWidget(self.groupRightmiddleLayoutOutTab1)
        self.groupOutputIdentifierTab1 = QGroupBox('Choose Inputs and Ouputs Identifier')
        self.groupOutputIdentifierTab1.setLayout(self.rightMiddleIdentifierTab1)
        # self.groupOutputIdentifierTab1.setStyleSheet(style.groupOutputIdentifierTab1Style())
        self.rightBottomLayoutsTab1 = QVBoxLayout()
        self.groupBottonTab1 = QGroupBox("Start Resolver")
        self.groupBottonTab1.setLayout(self.rightBottomLayoutsTab1)
        ############ right bottom ########################
        self.rightBottomLayoutsTab1.addWidget(self.startBtn)
        # self.rightBottomLayoutsTab1.addWidget(self.progressBar)
        self.rightBottomLayoutsTab1.addWidget(progressBar)
        self.groupBottonTab1.setLayout(self.rightBottomLayoutsTab1)
        ################# define layout tab1 ######################
        self.rightLayoutTab1.addWidget(self.IMGFrameTab1, 25)
        self.rightLayoutTab1.addWidget(self.groupSearchRightTab1, 25)
        self.rightLayoutTab1.addWidget(self.groupOutputIdentifierTab1, 25)
        self.rightLayoutTab1.addWidget(self.groupBottonTab1, 25)
        self.mainLayoutTab1.addLayout(self.leftLayoutTab1, 25)
        self.mainLayoutTab1.addLayout(self.rightLayoutTab1, 75)
        self.tab1.setLayout(self.mainLayoutTab1)
        ####################### layouts tab2 #################################
        ####################### layouts tab2 #################################
        self.mainLayoutTab2 = QHBoxLayout()
        self.mainLayoutTab2.addWidget(self.chemicalsOutTable, 90)
        self.mainLayoutTab2.addWidget(self.showResultsBtn, 10)
        self.tab2.setLayout(self.mainLayoutTab2)
        ######################### Layouts tab3 ################################
        ######################### Layouts tab3 ################################
        self.mainLayoutTab3 = QHBoxLayout()
        # table, left
        self.leftLayoutTab3 = QVBoxLayout() #sarà la table dei risultati
        self.leftLayoutTab3.addWidget(self.propertyTable)
        self.frameLeftLayoutTab3 = QFrame()
        self.frameLeftLayoutTab3.setLayout(self.leftLayoutTab3)
        # right layout
        # right top
        # right top pt1
        self.rightTopLayoutPt1 = QVBoxLayout()
        self.rightTopLayoutPt1.addWidget(self.propertyMW)
        self.rightTopLayoutPt1.addWidget(self.propertyLogP)
        self.rightTopLayoutPt1.addWidget(self.propertyNumHAcceptors)
        self.rightTopLayoutPt1.addWidget(self.propertyNumHDonors)
        self.groupRightTopLayoutPt1 = QGroupBox()
        self.groupRightTopLayoutPt1.setLayout(self.rightTopLayoutPt1)
        # right top pt2
        self.rightTopLayoutPt2 = QVBoxLayout()
        self.rightTopLayoutPt2.addWidget(self.propertyMaxPartialCharge)
        self.rightTopLayoutPt2.addWidget(self.propertyMinPartialCharge)
        self.rightTopLayoutPt2.addWidget(self.propertyNumAromaticRing)
        self.rightTopLayoutPt2.addWidget(self.propertyAll)
        self.groupRightTopLayoutPt2 = QGroupBox()
        self.groupRightTopLayoutPt2.setLayout(self.rightTopLayoutPt2)

        self.topLayoutTab3 = QHBoxLayout()
        self.topLayoutTab3.addWidget(self.groupRightTopLayoutPt1)
        self.topLayoutTab3.addWidget(self.groupRightTopLayoutPt2)
        self.groupTopLayoutTab3 = QGroupBox()
        self.groupTopLayoutTab3.setLayout(self.topLayoutTab3)
        # right top, bottom 
        self.rightBottomLayoutsTab3 = QVBoxLayout()
        self.rightBottomLayoutsTab3.addStretch()
        self.rightBottomLayoutsTab3.addWidget(self.propertyBtn)
        self.rightBottomLayoutsTab3.addWidget(self.saveDescriptorsBtn)
        self.rightBottomLayoutsTab3.addStretch()
        self.frameRightBottomLayoutsTab3 = QFrame()
        self.frameRightBottomLayoutsTab3.setLayout(self.rightBottomLayoutsTab3)
        # rightlayout
        self.rightLayoutTab3 = QVBoxLayout()    
        self.rightLayoutTab3.addWidget(self.groupTopLayoutTab3)
        self.rightLayoutTab3.addWidget(self.frameRightBottomLayoutsTab3)
        self.groupRightLayoutTab3 = QGroupBox()
        self.groupRightLayoutTab3.setLayout(self.rightLayoutTab3)
        # add to main tab 3
        self.mainLayoutTab3.addWidget(self.frameLeftLayoutTab3)
        self.mainLayoutTab3.addWidget(self.groupRightLayoutTab3)
        self.tab3.setLayout(self.mainLayoutTab3)
        ######################### Layouts tab4 ################################
        ######################### Layouts tab4 ################################
        self.mainLayoutTab4 = QHBoxLayout()
        self.rightLayoutTab4 = QVBoxLayout()
        self.leftLayoutTab4 = QVBoxLayout()
        self.rightLayoutTab4.addWidget(self.statisticsTable)
        self.leftLayoutTab4.addWidget(self.statisticsCalculationBtn)
        self.rightTab4Group = QGroupBox('Statistics')
        self.leftTab4Group = QGroupBox()
        self.rightTab4Group.setLayout(self.rightLayoutTab4)
        self.leftTab4Group.setLayout(self.leftLayoutTab4)
        self.mainLayoutTab4.addWidget(self.rightTab4Group,80)
        self.mainLayoutTab4.addWidget(self.leftTab4Group,20)
        self.tab4.setLayout(self.mainLayoutTab4)


    # Import Input  and set some variable as flag   
    def funcLoadFile(self):
        global progressBar, countProgressBar, endProgressBar
        self.filename, self.ok = QFileDialog.getOpenFileName(self, "Upload Dataset", "", "Import Files (*.xlsx)")
        if self.ok:
            self.dataset = pd.read_excel(self.filename)
            self.dataset = self.dataset.iloc[:,0]
            self.target = self.dataset.to_list()
            self.flag = 1
            endProgressBar = len(self.dataset)
            countProgressBar = 0
            progressBar.setValue(0)
            progressBar.setMaximum(endProgressBar)
            self.identifierDisplayInput()
    
    # save files
    def funcSaveFile(self):
        global dataset_out
        path = os.getcwd()
        path = os.path.join(path, "ChemicalResolverOutput.xlsx")
        if self.flag2 == 1 and self.flag == 1:
            dataset_out = pd.concat([dataset_out, self.propertiesOut.iloc[:,1:]], axis=1)
        dataset_out.to_excel(path)
        QMessageBox.information(self, "Info", "You have just saved the result in this folder. File Name: ChemicalResolverOutput.xlsx")
    
    def funcInfo(self):
        QMessageBox.information(self, "Info", "Chemicals Resolver was developed by Edoardo Luca Viganò, Gianluca Selvestrel, and Erika Colombo.\nThis Tool can search different molecule identifiers in a different database such as cactus, ChemID, etc.")

    # serve per rappresentare l'input nella table: Chemicals input
    def identifierDisplayInput(self):  
        if self.flag != 0:
            for i in reversed(range(self.chemicalsInputTable.rowCount())):
                self.chemicalsInputTable.removeRow(i)
            for row_data in self.dataset:
                row_number = self.chemicalsInputTable.rowCount()
                self.chemicalsInputTable.insertRow(row_number)
                self.chemicalsInputTable.setItem(row_number, 0, QTableWidgetItem(str(row_data)))
            self.chemicalsInputTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
    
    # serve per rappresentare l'output nella table: Chemicals output
    def identifierDisplayOutput(self):
        if flag1 != 0:
            for i in reversed(range(self.chemicalsOutTable.rowCount())):
                self.chemicalsOutTable.removeRow(i)
            self.chemicalsOutTable.setColumnCount(len(dataset_out.keys()))
            for j, name in enumerate(dataset_out.keys()):
                self.chemicalsOutTable.setHorizontalHeaderItem(j, QTableWidgetItem(str(name)))
                if j == 0: self.chemicalsOutTable.horizontalHeader().setSectionResizeMode(j, QHeaderView.Stretch)
                else: self.chemicalsOutTable.horizontalHeader().setSectionResizeMode(j, QHeaderView.ResizeToContents)
            for row_data in dataset_out.values:
                row_number = self.chemicalsOutTable.rowCount()
                self.chemicalsOutTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.chemicalsOutTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            self.chemicalsInputTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def propertiesDysplay(self):
        if self.propertyCheck_list != [] and self.flag2 == 1:
            for i in reversed(range(self.propertyTable.rowCount())):
                self.propertyTable.removeRow(i)  
            self.propertyTable.setColumnCount(len(self.propertiesOut.keys()))
            for j, name in enumerate(self.propertiesOut.keys()):
                self.propertyTable.setHorizontalHeaderItem(j, QTableWidgetItem(str(name)))
                if j == 0: self.propertyTable.horizontalHeader().setSectionResizeMode(j, QHeaderView.Stretch)
                else: self.propertyTable.horizontalHeader().setSectionResizeMode(j, QHeaderView.ResizeToContents)               
            for row_data in self.propertiesOut.values:
                row_number = self.propertyTable.rowCount()
                self.propertyTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.propertyTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            self.propertyTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        elif self.flag2 == 1: QMessageBox.information(self, "Warning", "Select at least one property!")
    
    ## da sistemare!
    def statisticDysplay(self):
        if self.statCalc == 1 and flag1 != 0:   
            for i in reversed(range(self.statisticsTable.rowCount())):
                    self.statisticsTable.removeRow(i)  
            self.statisticsTable.setColumnCount(len(self.statisticData.keys()))
            for j, name in enumerate(self.statisticData.keys()):
                self.statisticsTable.setHorizontalHeaderItem(j, QTableWidgetItem(str(name)))
                self.statisticsTable.horizontalHeader().setSectionResizeMode(j, QHeaderView.Stretch)
            for row_data in self.statisticData.values:
                row_number = self.statisticsTable.rowCount()
                self.statisticsTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.statisticsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            self.statisticsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def propertyCheck(self):      
        if self.propertyMW.isChecked(): self.propertyCheck_list.append('MW')
        if self.propertyNumAromaticRing.isChecked(): self.propertyCheck_list.append('NumAromaticRing')
        if self.propertyNumHDonors.isChecked(): self.propertyCheck_list.append('NumHDonors')
        if self.propertyNumHAcceptors.isChecked(): self.propertyCheck_list.append('NumHAcceptors')
        if self.propertyLogP.isChecked(): self.propertyCheck_list.append('LogP')
        if self.propertyMaxPartialCharge.isChecked(): self.propertyCheck_list.append('MaxPartialCharge')
        if self.propertyMinPartialCharge.isChecked(): self.propertyCheck_list.append('MinPartialCharge')
        if self.propertyAll.isChecked(): self.propertyCheck_list.append('All')

    def functPropertyBtn(self):
        self.verifyIdInOut()
        self.propertyCheck()
        if self.inId == 'SMILES' or self.inId == 'INCHI':
            for j, n in enumerate(self.dataset):
                if j == 0: 
                    self.propertiesOut = propertyCalculator(n, self.inId, self.propertyCheck_list)
                else:
                    data = propertyCalculator(n, self.inId, self.propertyCheck_list)
                    self.propertiesOut = pd.concat([self.propertiesOut, data])
            self.propertiesOut.reset_index(inplace=True, drop=True)
            self.flag2 = 1
            self.propertiesDysplay()
        elif 'SMILES' in self.outId or 'INCHI' in self.outId:
            inchi = [i for i in dataset_out.keys() if 'InchiFrom' in i]
            smiles = [i for i in dataset_out.keys() if 'SmilesFrom' in i]
            if inchi != []: 
                try:
                    min_ = min([dataset_out[i].value_counts()['Error'] for i in inchi])
                    for i in inchi:
                        if dataset_out[i].count('Error') == min_:
                            columnMinError = i
                            ident = 'INCHI'
                except: 
                    columnMinError = inchi[0]
                    ident = 'INCHI'
            elif smiles != []:
                try:
                    min_ = min([dataset_out[i].value_counts()['Error'] for i in smiles])
                    for i in smiles:
                        if dataset_out[i].count('Error') == min_:
                            columnMinError = i
                            ident = 'SMILES'
                except: 
                    columnMinError = smiles[0]
                    ident = 'SMILES'
            for j, n in enumerate(dataset_out[columnMinError]):
                if n != 'Error':
                    if j == 0: 
                        self.propertiesOut = propertyCalculator(n, ident, self.propertyCheck_list)
                    else:
                        data = propertyCalculator(n, ident, self.propertyCheck_list)
                        self.propertiesOut = pd.concat([self.propertiesOut, data])
            self.propertiesOut.reset_index(inplace=True, drop=True)
            self.flag2 = 1
            self.propertiesDysplay()
        else:
            QMessageBox.information(self, "Warning", "The tool for property calculation need inchi or smiles.\nSo if there'arent in input please start the resolver before")
        
    def verifyIdInOut(self):
        global identifier
        self.outId = []
        self.inId = self.identifierComboIn.currentText()
        if self.inId == 'SELECT':
            QMessageBox.information(self, 'Info', 'Please, before start research select the input identifier!')
        identifier = self.inId
        if self.checkBtnName.isChecked(): self.outId.append('NAME')
        if self.checkBtnSmiles.isChecked(): self.outId.append('SMILES')
        if self.checkBtnInchi.isChecked(): self.outId.append('INCHI')
        if self.checkBtnCas.isChecked(): self.outId.append('CAS')

    # Verify wich are the input and output identifiers
    def startCalculation(self):
        global flag1, dataset_out
        if self.flag == 0: QMessageBox.information(self, "Warning", "You must choice the input data")
        self.verifyIdInOut()
        flag1 = 1
        if self.outId == []:
            QMessageBox.information(self, "Warning", "You must choice the output Identifier")
        else:
            # create a thread   
            worker = Worker(self.inId, self.outId, self.target)
            worker.signals.progress.connect(self.updateProgressBar)
            worker.signals.end.connect(self.endCalculation)
            self.threadpool.start(worker)
            self.identifierDisplayOutput()

    def searchChemicals(self):
        global chemImg, identifier, value
        value = self.searchEntry.text()
        self.verifyIdInOut()
        if value == "":
            QMessageBox.information(self, "warning", "Search entry can't be empty!!")
        else:
            self.searchEntry.setText("")     
        if value in self.target:
            if self.inId == 'SMILES':
                identifier = 'SMILES'
                try:
                    mol = Chem.MolFromSmiles(value)
                    Draw.MolToFile(mol,'showImg.png')
                    chemImg = 1
                except:pass
            elif self.inId == 'INCHI':
                identifier = 'INCHI'
                mol = Chem.MolFromInchi(value)
                Draw.MolToFile(mol,'showImg.png')
                chemImg = 1
            if chemImg == 0:
                try: 
                    mol = Chem.MolFromSmiles(value)
                    Draw.MolToFile(mol,'showImg.png')
                    chemImg = 1 
                    identifier = 'SMILES'
                except: pass
                try:
                    mol = Chem.MolFromInchi(value)
                    Draw.MolToFile(mol,'showImg.png')
                    chemImg = 1
                    identifier = 'INCHI'
                except: pass
            if identifier == 0:
                identifier = self.inId       
            self.showChemical = ShowChemical()
            self.showChemical.show()
        elif value != "": 
            QMessageBox.information(self, "warning", "This chemical is not in list!!")
    
    # search chemicals double click
    def searchChemicalsDoubleClick(self):
        global chemImg, identifier, value
        if self.flag != 0:
            self.verifyIdInOut()
            value = self.chemicalsInputTable.item(self.chemicalsInputTable.currentRow(), 0).text()       
            if self.inId == 'SMILES':
                identifier = 'SMILES'
                try:
                    mol = Chem.MolFromSmiles(value)
                    Draw.MolToFile(mol,'showImg.png')
                    chemImg = 1
                except:pass
            elif self.inId == 'INCHI':
                identifier = 'INCHI'
                mol = Chem.MolFromInchi(value)
                Draw.MolToFile(mol,'showImg.png')
                chemImg = 1
            if chemImg == 0:
                try: 
                    mol = Chem.MolFromSmiles(value)
                    Draw.MolToFile(mol,'showImg.png')
                    chemImg = 1 
                    identifier = 'SMILES'
                except: pass
                try:
                    mol = Chem.MolFromInchi(value)
                    Draw.MolToFile(mol,'showImg.png')
                    chemImg = 1
                    identifier = 'INCHI'
                except: pass
            if identifier == 0:
                identifier = self.inId       
            self.showChemical = ShowChemical()
            self.showChemical.show()


    def functStatisticsCalculation(self):
        self.statCalc = 1
        stat = statisticsTab(self.dataset, dataset_out)
        self.statisticData = stat.percentage()
        self.statisticDysplay()

    # da sistemare
    def funcAddChemicals(self):
        global progressBar, endProgressBar, countProgressBar
        txt = self.addChemicalsInLine.text()
        if txt:
            if self.flag == 1:
                self.dataset = self.dataset.append((pd.Series(txt)),ignore_index=True)
                self.dataset.reset_index(drop=True, inplace=True)
            else:
                self.dataset = pd.Series(txt)
                countProgressBar = 0
            self.addChemicalsInLine.setText('')
            self.target = self.dataset.to_list()
            self.flag = 1
            endProgressBar = len(self.dataset)
            progressBar.setValue(0)
            progressBar.setMaximum(endProgressBar)

        else:
            QMessageBox.information(self, "Warning", "Define chemical you want to add!")
        
        self.identifierDisplayInput()

    def functShowResults(self):
        global countProgressBar, endProgressBar
        if countProgressBar<endProgressBar:
            QMessageBox.information(self, "Warning", "Wait until the tool finish the research!")
        else:
            self.identifierDisplayOutput()
    
    def functSaveDescriptors(self):
        if self.flag2 == 1:
            self.propertiesOut.to_excel('propertiesCalculated.xlsx')
            QMessageBox.information(self, "Info", "You have just saved the result in this folder. File Name: propertiesCalculated.xlsx")
        else:
            QMessageBox.information(self, "Warning", "You have to calculate the descriptors!")
    
    @ staticmethod
    def updateProgressBar():
        progressBar.setValue(countProgressBar)

    def endCalculation(self):
        QMessageBox.information(self, 'Info', "Research has been done! In Chemicals Output you can find the result")

    def cleanWork(self):        
        global chemImg, identifier, value, flag1, dataset_out
        chemImg = 0
        identifier = 0
        value = ''
        flag1 = 0
        self.dataset = pd.DataFrame()
        dataset_out = pd.DataFrame()
        self.outId = []
        self.inId = ''
        self.flag = 0
        self.flag2 = 0
        self.propertyCheck_list = []
        for i in reversed(range(self.chemicalsOutTable.rowCount())):
            self.chemicalsOutTable.removeRow(i)
        for i in reversed(range(self.chemicalsInputTable.rowCount())):
            self.chemicalsInputTable.removeRow(i)
        for i in reversed(range(self.propertyTable.rowCount())):
            self.propertyTable.removeRow(i)
        for i in reversed(range(self.statisticsTable.rowCount())):
            self.statisticsTable.removeRow(i)        
        progressBar.setValue(0)
        

class ShowChemical(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical")
        self.setWindowIcon(QIcon("icons/IMG.jpg"))
        self.setGeometry(150,150,280,480)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.setValues()

    def widgets(self):
        # set IMages
        global chemImg
        self.chemicalImg = QLabel()
        size = (220, 220)
        if chemImg == 1:
            img = Image.open("showImg.png")
            img = img.resize(size)
            img.save("showImg.png")
            self.img = QPixmap("showImg.png")
            chemImg = 0
        else:
            self.img = QPixmap("img/imagesNone.png")      
        self.chemicalImg.setPixmap(self.img)
        self.chemicalImg.setAlignment(Qt.AlignCenter)
        # set title
        self.titleText = QLabel("Chemical")
        self.titleText.setAlignment(Qt.AlignCenter)
        # line edit 
        self.nameEntry = QLineEdit()
        self.nameEntry.setPlaceholderText("Enter chemical name")
        self.casEntry = QLineEdit()
        self.casEntry.setPlaceholderText("Enter chemical cas")
        self.inchiEntry = QLineEdit()
        self.inchiEntry.setPlaceholderText("Enter chemical inchi")
        self.smileEntry = QLineEdit()
        self.smileEntry.setPlaceholderText("Enter chemical smiles")
        self.btnSearch = QPushButton('Search in database')
        self.btnSearch.clicked.connect(self.funcSearchBtn)
        self.btnSaveFile = QPushButton("Save")
        self.btnSaveFile.clicked.connect(self.funcSaveFile)
    
    def layouts(self):
        # top layout with img and title
        self.topLayout = QVBoxLayout()
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.chemicalImg)
        # top frame
        self.topFrame = QFrame()
        self.topFrame.setLayout(self.topLayout)
        # bottom layout
        self.bottomLayout = QFormLayout()
        self.bottomLayout.addRow(QLabel("Name:"), self.nameEntry)
        self.bottomLayout.addRow(QLabel("Cas:"), self.casEntry)
        self.bottomLayout.addRow(QLabel("Inchi:"), self.inchiEntry)
        self.bottomLayout.addRow(QLabel("smiles:"), self.smileEntry)
        self.bottomLayout.addRow(QLabel(""), self.btnSearch)
        self.bottomLayout.addRow(QLabel(""), self.btnSaveFile) 
        # bottom frame
        self.bottomFrame = QFrame()
        self.bottomFrame.setLayout(self.bottomLayout)
        # main
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def setValues(self):
        global value, flag1
        self.nameEntry.setText('')
        self.smileEntry.setText('')
        self.casEntry.setText('')
        self.inchiEntry.setText('')
        if identifier == 'SMILES':
            self.smileEntry.setText(value)
        elif identifier == 'CAS':
            self.casEntry.setText(value)
        elif identifier == 'NAME':  
            self.nameEntry.setText(value)
        elif identifier == 'INCHI':
            self.inchiEntry.setText(value)
        if flag1 ==1:
            inchi = [i for i in dataset_out.keys() if 'InchiFrom' in i]
            smiles = [i for i in dataset_out.keys() if 'SmilesFrom' in i]
            cas = [i for i in dataset_out.keys() if 'CasFrom' in i]
            name = [i for i in dataset_out.keys() if 'NameFrom' in i]
            n = (dataset_out.stack() == value).idxmax()[0]
            if identifier == 'SMILES': # [1] e non [0] va sistemato per cirpy
                try:self.inchiEntry.setText(str(dataset_out.loc[n, inchi[1]]))
                except:self.inchiEntry.setText(str(''))
                try:self.casEntry.setText(str(dataset_out.loc[n, cas[1]]))
                except:self.casEntry.setText(str(''))
                try:self.nameEntry.setText(str(dataset_out.loc[n, name[1]]))
                except:self.nameEntry.setText(str(''))
            elif identifier == 'CAS':
                try:self.inchiEntry.setText(str(dataset_out.loc[n, inchi[1]]))
                except:self.inchiEntry.setText(str(''))
                try:self.smileEntry.setText(str(dataset_out.loc[n, smiles[1]]))
                except:self.smileEntry.setText(str(''))
                try:self.nameEntry.setText(str(dataset_out.loc[n, name[1]]))
                except:self.nameEntry.setText(str(''))
            elif identifier == 'INCHI':
                try:self.smileEntry.setText(str(dataset_out.loc[n, smiles[1]]))
                except:self.smileEntry.setText(str(''))
                try:self.casEntry.setText(str(dataset_out.loc[n, cas[1]]))
                except:self.casEntry.setText(str(''))
                try:self.nameEntry.setText(str(dataset_out.loc[n, name[1]]))
                except:self.nameEntry.setText(str(''))
            elif identifier == 'NAME':
                try:self.inchiEntry.setText(str(dataset_out.loc[n, inchi[1]]))
                except:self.inchiEntry.setText(str(''))
                try:self.casEntry.setText(str(dataset_out.loc[n, cas[1]]))
                except:self.casEntry.setText(str(''))
                try:self.smileEntry.setText(str(dataset_out.loc[n, smiles[1]]))
                except:self.smileEntry.setText(str(''))

    def funcSearchBtn(self):
        global chemImg
        if identifier == 'SMILES':
            CasFromSmilesNCI_list = CasFromSmilesNCI(value)
            InchiFromSmilesNCI_list = InchiFromSmilesNCI(value)
            NameFromSmilesNCI_list = NameFromSmilesNCI(value)
            self.inchiEntry.setText(str(InchiFromSmilesNCI_list))
            self.casEntry.setText(str(CasFromSmilesNCI_list))
            self.nameEntry.setText(str(NameFromSmilesNCI_list))
        elif identifier == 'CAS':
            InchiFromCasNCI_list = InchiFromCasNCI(value)
            SmilesFromCasNCI_list = SmilesFromCasNCI(value)
            NameFromCasNCI_list = NameFromCasNCI(value)
            self.inchiEntry.setText(str(InchiFromCasNCI_list))
            self.smileEntry.setText(str(SmilesFromCasNCI_list))
            self.nameEntry.setText(str(NameFromCasNCI_list))
            try:
                if chemImg == 0 and SmilesFromCasNCI_list != 'Error':
                    mol = Chem.MolFromSmiles(SmilesFromCasNCI_list)
                    Draw.MolToFile(mol,'showImg.png')
                    # chemImg = 1
                    size = (200, 200)
                    img = Image.open("showImg.png")
                    img = img.resize(size)
                    img.save("showImg.png")
                    self.img = QPixmap("showImg.png")
                    self.chemicalImg.setPixmap(self.img)
                    self.chemicalImg.setAlignment(Qt.AlignCenter)
            except: pass                 
        elif identifier == 'INCHI':
            self.smileEntry.setText(str(SmilesFromInchiNCI(value)))
            self.casEntry.setText(str(CasFromInchiNCI(value)))
            self.nameEntry.setText(str(NameFromInchiNCI(value)))
        elif identifier == 'NAME':
            InchiFromNameNCI_list = InchiFromNameNCI(value)
            CasFromNameNCI_list = CasFromNameNCI(value)
            SmilesFromNameNCI_list = SmilesFromNameNCI(value)
            self.inchiEntry.setText(str(InchiFromNameNCI_list))
            self.casEntry.setText(str(CasFromNameNCI_list))
            self.smileEntry.setText(str(SmilesFromNameNCI_list))
            try:          
                if chemImg == 0 and SmilesFromNameNCI_list != 'Error':
                        mol = Chem.MolFromSmiles(SmilesFromNameNCI_list)
                        Draw.MolToFile(mol,'showImg.png')
                        # chemImg = 1             
                        size = (200, 200)
                        img = Image.open("showImg.png")
                        img = img.resize(size)
                        img.save("showImg.png")
                        self.img = QPixmap("showImg.png")
                        self.chemicalImg.setPixmap(self.img)
                        self.chemicalImg.setAlignment(Qt.AlignCenter)
            except: pass
                               
    def funcSaveFile(self):
        column_name = ['NAME', 'SMILES', 'CAS', 'INCHI']
        name = self.nameEntry.text()
        smiles = self.smileEntry.text()
        cas = self.casEntry.text()
        inchi = self.inchiEntry.text()
        values = [name, smiles, cas, inchi]
        data = pd.DataFrame(zip(column_name,values))
        data.to_excel('SingleChemical.xlsx')
        self.nameEntry.setText('')
        self.smileEntry.setText('')
        self.casEntry.setText('')
        self.inchiEntry.setText('')
        self.close()
        
class WorkerSignals(QObject):

    progress = pyqtSignal(int) 
    end = pyqtSignal(int) 

class Worker(QRunnable):
    '''
    Worker thread
    '''
    signals = WorkerSignals()
    def __init__(self, inId, outId, target):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        global  dataset_out, countProgressBar
        self.inId = inId
        self.outId = outId
        self.target = target
        
        
    @pyqtSlot()
    def run(self):
        '''
        Your code goes in this function
        '''
        print("Thread start") 
        global dataset_out
        
        # cas out
        if self.inId == 'NAME' and 'CAS' in self.outId:
            if dataset_out.empty:
                dataset_out = self.casFromNameAll()
            else:
                df = self.casFromNameAll()
                dataset_out = pd.concat([dataset_out, df.iloc[:,1:]], axis=1)
            
        if self.inId == 'SMILES' and 'CAS' in self.outId:
            if dataset_out.empty:
                dataset_out = self.casFromSmilesAll()
            else:
                df = self.casFromSmilesAll()
                dataset_out = pd.concat([dataset_out, df.iloc[:,1:]], axis=1)    
        
        if self.inId == 'INCHI' and 'CAS' in self.outId:
            if dataset_out.empty:
                dataset_out = self.casFromInchiAll()
            else:
                df = self.casFromInchiAll()
                dataset_out = pd.concat([dataset_out, df.iloc[:,1:]], axis=1)
        
        # smiles out
        if self.inId == 'NAME' and 'SMILES' in self.outId: 
            if dataset_out.empty:
                dataset_out = self.smilesFromNameAll()
            else:
                df = self.smilesFromNameAll()
                dataset_out = pd.concat([dataset_out, df.iloc[:,1:]], axis=1)

        if self.inId == 'INCHI' and 'SMILES' in self.outId:
            if dataset_out.empty:
                dataset_out = self.smilesFromInchiAll()
            else:
                df = self.smilesFromInchiAll()
                dataset_out = pd.concat([dataset_out, df.iloc[:,1:]], axis=1) 

        if self.inId == 'CAS' and 'SMILES' in self.outId:
            if dataset_out.empty:
                dataset_out = self.smilesFromCasAll()
            else:
                df = self.smilesFromCasAll()
                dataset_out = pd.concat([dataset_out, df.iloc[:,1:]], axis=1) 

        # name out
        if self.inId == 'INCHI' and 'NAME' in self.outId:
            if dataset_out.empty:
                dataset_out = self.nameFromInchiAll()
            else:
                df = self.nameFromInchiAll()
                dataset_out = pd.concat([dataset_out, df.iloc[:,1:]], axis=1) 
        if self.inId == 'SMILES' and 'NAME' in self.outId:  
            if dataset_out.empty:
                dataset_out = self.nameFromSmilesAll()
            else:
                df = self.nameFromSmilesAll()
                dataset_out = pd.concat([dataset_out, df.iloc[:,1:]], axis=1) 
        if self.inId == 'CAS' and 'NAME' in self.outId:      
            if dataset_out.empty:
                dataset_out = self.nameFromCasAll()
            else:
                df = self.nameFromCasAll()
                dataset_out = pd.concat([dataset_out, df.iloc[:,1:]], axis=1) 

        # inchi out
        if self.inId == 'NAME' and 'INCHI' in self.outId:
            if dataset_out.empty:
                dataset_out = self.inchiFromNameAll()
            else:
                df = self.inchiFromNameAll()
                dataset_out = pd.concat([dataset_out, df.iloc[:,1:]], axis=1) 
        if self.inId == 'SMILES' and 'INCHI' in self.outId:
            if dataset_out.empty:
                dataset_out = self.inchiFromSmilesAll()
            else:
                df = self.inchiFromSmilesAll()
                dataset_out = pd.concat([dataset_out, df.iloc[:,1:]], axis=1) 
        if self.inId == 'CAS' and 'INCHI' in self.outId:
            if dataset_out.empty:
                dataset_out = self.inchiFromCasAll()
            else:
                df = self.inchiFromCasAll()
                dataset_out = pd.concat([dataset_out, df.iloc[:,1:]], axis=1) 
        self.signals.end.emit(1)
        print("Thread complete")
        # return dataset_out

            
    ############################## CAS From ###################################
    def casFromNameAll(self):
        global countProgressBar
        CasFromNameCirpy_list = []
        CasFromNameChemID_list = []
        CasFromNameNCI_list = []
        for name in self.target:
            # qua serve qualcosa per i database che si vuole interrogare
            CasFromNameCirpy_list.append(CasFromNameCirpy(name))
            CasFromNameChemID_list.append(CasFromNameChemID(name))
            CasFromNameNCI_list.append(CasFromNameNCI(name))
            self.signals.progress.emit(countProgressBar)
            countProgressBar += 1
        data = zip(self.target, CasFromNameCirpy_list, CasFromNameChemID_list, CasFromNameNCI_list)
        df_casFromNameAll = pd.DataFrame(data, columns = ['Name', 'CasFromNameCirpy', 'CasFromNameChemID', 'CasFromNameNCI'])
        return df_casFromNameAll
    
    def casFromSmilesAll(self):
        global countProgressBar
        CasFromSmilesNCI_list = []
        # CasFromSmilesPubchem = [] da fare
        for smiles in self.target:
            # qua serve qualcosa per i database che si vuole interrogare
            CasFromSmilesNCI_list.append(CasFromSmilesNCI(smiles))
            self.signals.progress.emit(countProgressBar)
            countProgressBar += 1
        data = zip(self.target, CasFromSmilesNCI_list)
        df_CasFromSmilesAll = pd.DataFrame(data, columns = ['SMILES', 'CasFromSmilesNCI'])
        return df_CasFromSmilesAll
          
    def casFromInchiAll(self):
        global countProgressBar
        CasFromInchiChemID_list = []
        CasFromInchiNCI_list = []
        for inchi in self.target:
            # qua serve qualcosa per i database che si vuole interrogare
            CasFromInchiChemID_list.append(CasFromInchiChemID(inchi))
            CasFromInchiNCI_list.append(CasFromInchiNCI(inchi))
            self.signals.progress.emit(countProgressBar)
            countProgressBar += 1
        data = zip(self.target, CasFromInchiChemID_list, CasFromInchiNCI_list)
        df_CasFromInchiAll = pd.DataFrame(data, columns = ['INCHI', 'CasFromInchiChemID', 'CasFromInchiNCI'])
        return df_CasFromInchiAll

    ############################## SMILES From ################################
    def smilesFromNameAll(self):
        global countProgressBar
        SmilesFromNameNCI_list = []
        for name in self.target:
            # qua serve qualcosa per i database che si vuole interrogare
            SmilesFromNameNCI_list.append(SmilesFromNameNCI(name))
            self.signals.progress.emit(countProgressBar)
            countProgressBar += 1
        data = zip(self.target, SmilesFromNameNCI_list)
        df_SmilesFromNameAll = pd.DataFrame(data, columns = ['NAME', 'SmilesFromNameNCI'])
        return df_SmilesFromNameAll

    def smilesFromCasAll(self): 
        global countProgressBar
        SmilesFromCasCST_list = []
        SmilesFromCasPubChem_list= []
        SmilesFromCasNCI_list = []
        for cas in self.target:
            # qua serve qualcosa per i database che si vuole interrogare
            SmilesFromCasCST_list.append(SmilesFromCasCST(cas))
            SmilesFromCasPubChem_list.append(SmilesFromCasPubChem(cas))
            SmilesFromCasNCI_list.append(SmilesFromCasNCI(cas))
            self.signals.progress.emit(countProgressBar)
            countProgressBar += 1
        data = zip(self.target, SmilesFromCasCST_list, SmilesFromCasPubChem_list, SmilesFromCasNCI_list)
        df_SmilesFromCasAll = pd.DataFrame(data, columns = ['CAS', 'SmilesFromCasCST', 'SmilesFromCasPubChem', 'SmilesFromCasNCI'])
        return df_SmilesFromCasAll

    def smilesFromInchiAll(self):
        global countProgressBar 
        SmilesFromInchiNCI_list = []
        for inchi in self.target:
            # qua serve qualcosa per i database che si vuole interrogare
            SmilesFromInchiNCI_list.append(SmilesFromInchiNCI(inchi))
            self.signals.progress.emit(countProgressBar)
            countProgressBar += 1
        data = zip(self.target, SmilesFromInchiNCI_list)
        df_SmilesFromInchiAll = pd.DataFrame(data, columns = ['INCHI', 'SmilesFromInchiNCI'])
        return df_SmilesFromInchiAll

    ############################## NAME From ##################################
    def nameFromSmilesAll(self):
        global countProgressBar
        NameFromSmilesNCI_list = []
        for smiles in self.target:
            # qua serve qualcosa per i database che si vuole interrogare
            NameFromSmilesNCI_list.append(NameFromSmilesNCI(smiles))
            self.signals.progress.emit(countProgressBar)
            countProgressBar += 1
        data = zip(self.target, NameFromSmilesNCI_list)
        df_NameFromSmilesAll = pd.DataFrame(data, columns = ['SMILES', 'NameFromSmilesNCI'])
        return df_NameFromSmilesAll

    def nameFromCasAll(self):
        global countProgressBar
        nameFromCasChemID_list = []
        NameFromCasNCI_list = []
        for cas in self.target:
            # qua serve qualcosa per i database che si vuole interrogare
            nameFromCasChemID_list.append(NameFromCasChemID(cas))
            NameFromCasNCI_list.append(NameFromCasNCI(cas))
            self.signals.progress.emit(countProgressBar)
            countProgressBar += 1
        data = zip(self.target, nameFromCasChemID_list, NameFromCasNCI_list)
        df_NameFromCasNCIAll = pd.DataFrame(data, columns = ['CAS', 'NameFromCasChemID', 'NameFromCasNCI'])
        return df_NameFromCasNCIAll   

    def nameFromInchiAll(self):
        global countProgressBar
        NameFromInchiChemID_list = []
        NameFromInchiNCI_list = []
        for inchi in self.target:
            # qua serve qualcosa per i database che si vuole interrogare
            NameFromInchiChemID_list.append(NameFromInchiChemID(inchi))
            NameFromInchiNCI_list.append(NameFromInchiNCI(inchi))
            self.signals.progress.emit(countProgressBar)
            countProgressBar += 1
        data = zip(self.target, NameFromInchiChemID_list, NameFromInchiNCI_list)
        df_NameFromInchiAll = pd.DataFrame(data, columns = ['INCHI', 'NameFromInchiChemID', 'NameFromInchiNCI'])
        return df_NameFromInchiAll   
    ############################## INCHI From #################################
    def inchiFromNameAll(self):
        global countProgressBar 
        InchiFromNameNCI_list = []
        for name in self.target:
            # qua serve qualcosa per i database che si vuole interrogare
            InchiFromNameNCI_list.append(InchiFromNameNCI(name))
            self.signals.progress.emit(countProgressBar)
            countProgressBar += 1
        data = zip(self.target, InchiFromNameNCI_list)
        df_InchiFromNameAll = pd.DataFrame(data, columns = ['NAME', 'InchiFromNameNCI'])
        return df_InchiFromNameAll 
        
    def inchiFromCasAll(self):
        global countProgressBar
        InchiFromCasChemID_list = []
        InchiFromCasNCI_list = []
        for cas in self.target:
            # qua serve qualcosa per i database che si vuole interrogare
            InchiFromCasChemID_list.append(InchiKeyFromCasChemID(cas))
            InchiFromCasNCI_list.append(InchiFromCasNCI(cas))
            self.signals.progress.emit(countProgressBar)
            countProgressBar += 1
        data = zip(self.target, InchiFromCasChemID_list, InchiFromCasNCI_list)
        df_InchiFromCasAll = pd.DataFrame(data, columns = ['CAS', 'InchiKeyFromCasChemID', 'InchiFromCasNCI'])
        return df_InchiFromCasAll

    def inchiFromSmilesAll(self):
        global countProgressBar 
        InchiFromSmilesNCI_list = []
        for smiles in self.target:
            # qua serve qualcosa per i database che si vuole interrogare
            InchiFromSmilesNCI_list.append(InchiFromSmilesNCI(smiles))
            self.signals.progress.emit(countProgressBar)
            countProgressBar += 1
        data = zip(self.target, InchiFromSmilesNCI_list)
        df_InchiFromSmilesAll = pd.DataFrame(data, columns = ['SMILES', 'InchiFromSmilesNCI'])
        return df_InchiFromSmilesAll 

class statisticsTab:
    def __init__(self, dataTarget, dataOutput):#, dataProperty):
        self.dataTarget = dataTarget
        self.dataOutput = dataOutput
        # self.dataProperty = dataProperty

    def percentage(self):
        if 'Error' in self.dataOutput.values:
            self.percResolver = list(self.dataOutput[self.dataOutput == 'Error'].count())
            self.percResolver = [100-round(i*100/len(self.dataOutput.iloc[:,0])) for i in self.percResolver]
            self.percResolver = pd.DataFrame(zip(list(self.dataOutput.keys()), self.percResolver), columns=['Database', 'Percentage Resolver %'])
        else: 
            self.percResolver =  pd.DataFrame(zip(list(self.dataOutput.keys()), ['100'] * len(list(self.dataOutput.keys()))), columns=['Database', 'Percentage Resolver %'])   
        return self.percResolver.iloc[1:,:]       
        

def main():
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()
    
    
        