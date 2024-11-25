#Packages
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
from os.path import isfile
from pathlib import Path
import sys
from scipy import spatial
#Our other repos
from qtwidgets.sliders import QCustomSlider
from qtwidgets.images import QImageViewer
from labvision.images import write_img
#This project
from gui.pandas_view import PandasWidget
from .file_io import check_filenames, open_movie_dialog, open_settings_dialog, save_settings_dialog

class MainWindow(QMainWindow):    
    def __init__(self, *args, movie_filename=None, settings_filename=None, screen_size=None, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)
        #input df name
        self.data_filename = "testdata.hdf5"
        #output df name
        self.output_filename = "settings.hdf5"

        self.screen_size = screen_size       
        self.setWindowTitle("Pandas project")

        self.main_panel = QWidget()
        self.main_layout = QHBoxLayout()  # Contains view and settings layout
        self.setup_menus_toolbar()
        self.main_panel.setLayout(self.main_layout)
        self.setCentralWidget(self.main_panel)
        self.setup_pandas_viewer()   

        """------------------------------------------------------------------------------
        ------------------------------------------------------------------------------
        SETUP MENUS AND TOOLBAR
        
        Setup of all the menus and toolbars at the bottom. The statusbar at the bottom
        is also initialised here.
        ---------------------------------------------------------------------------------
        ---------------------------------------------------------------------------------"""

    def setup_menus_toolbar(self):
        dir,_ =os.path.split(os.path.abspath(__file__))
        resources_dir = os.path.join(dir,'icons','icons')
        self.toolbar = QToolBar('Toolbar')
        self.toolbar.setIconSize(QSize(16,16))
        self.addToolBar(self.toolbar)

        '''
        ---------------------------------------------------------------------------------------------------
        Buttons on toolbar
        ---------------------------------------------------------------------------------------------------
        '''
        open_movie_button = QAction(QIcon(os.path.join(resources_dir,"folder-open-film.png")), "Open File", self)
        open_movie_button.setStatusTip("Open Movie")
        open_movie_button.triggered.connect(self.open_movie_click)
        self.toolbar.addAction(open_movie_button)

        save_settings_button = QAction(QIcon(os.path.join(resources_dir,"script-export.png")), "Save Settings File", self)
        save_settings_button.setStatusTip("Save Settings")
        save_settings_button.triggered.connect(self.save_settings_button_click)
        self.toolbar.addAction(save_settings_button)


        self.pandas_button = QAction(QIcon(os.path.join(resources_dir, "view_pandas.png")),"Show Dataframe View", self)
        self.pandas_button.triggered.connect(self.pandas_button_click)
        self.pandas_button.setCheckable(True)
        self.pandas_button.setChecked(False)
        self.toolbar.addAction(self.pandas_button)

        close_button = QAction(QIcon(os.path.join(resources_dir,"cross-button.png")), "Close", self)
        close_button.triggered.connect(self.close_button_click)
        self.toolbar.addAction(close_button)

        menu = self.menuBar()
        '''
        ---------------------------------------------------------------------------------------------
        File menu items
        ---------------------------------------------------------------------------------------------
        '''
        self.file_menu = menu.addMenu("&File")
        self.file_menu.addAction(open_movie_button)
        self.file_menu.addAction(save_settings_button)
        self.file_menu.addAction(close_button)
        self.file_menu.addAction(self.pandas_button)
       
        """-----------------------------------------------------------------------------------------------
        --------------------------------------------------------------------------------------------------
        SETUP VIEWER
        
        Setup for the viewer panel - LHS of Gui includes viewer, frame selector and capture v preprocessing
        image toggle button.
        --------------------------------------------------------------------------------------------------
        ----------------------------------------------------------------------------------------------"""

    """
    ---------------------------------------------------------------         
    ------------------------------------------------------------------
    Callback functions
    ------------------------------------------------------------------
    ----------------------------------------------------------------
    """
    def open_movie_click(self):
        #open the df
        print("open movie")
    
    def save_settings_button_click(self):
        #save the df
        print("save")
        
    """-------------------------------------------------------------
    Functions relevant to the tools section
    --------------------------------------------------------------"""

    def setup_pandas_viewer(self):
        if hasattr(self, 'pandas_viewer'):
            self.pandas_viewer.close()
            self.pandas_viewer.deleteLater()
        self.pandas_viewer = PandasWidget(parent=self)
        self.update_pandas_view()

    def pandas_button_click(self):
        if self.pandas_button.isChecked():
            self.pandas_viewer.show()
        else:
            self.pandas_viewer.hide()

    def update_pandas_view(self):
        fname = self.data_filename
        self.pandas_viewer.update_file(fname, 1)

    def close_button_click(self):
        sys.exit()
