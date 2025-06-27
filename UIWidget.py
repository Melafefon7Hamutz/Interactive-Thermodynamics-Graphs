import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QWidget, QComboBox, QPushButton, QLineEdit, QLabel

from IsothermalProcess import IsothermalProcess
from AdiabaticProcess import AdiabaticProcess
from IsobaricProcess import IsobaricProcess
from IsochoricProcess import IsochoricProcess


class UIWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_window = parent
        self.setFixedWidth(500)
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(PyQt5.QtCore.Qt.AlignmentFlag.AlignTop)

        # things in UI on the right
        font = PyQt5.QtGui.QFont('Ariel', 12)
        self.setFont(font)
        self.special_arguments_widgets = []

        # selector
        self.process_selector_processes = [
            (IsothermalProcess, "Isothermal Process"), (AdiabaticProcess, "Adiabatic Process"), 
            (IsobaricProcess, "Isobaric Process"), (IsochoricProcess, "Isochoric Process")]
        self.process_selector = QComboBox()
        for p, pn in self.process_selector_processes:
            self.process_selector.addItem(pn)
        self.process_selector.activated.connect(
            self.on_process_selector_change)
        self.layout().addWidget(self.process_selector)
        self.selected_process_type = self.process_selector_processes[0][0]

        # references to special argument inputs
        self.special_arguments_inputs = {}
        self.special_arguments_inputs[AdiabaticProcess] = {
            'gamma': QLineEdit()}

        # special arguments
        for process_type, _ in self.process_selector_processes:
            w = QWidget()
            w.setLayout(QGridLayout())
            self.layout().addWidget(w)
            w.hide()
            self.special_arguments_widgets.append(w)
            if process_type in self.special_arguments_inputs:
                for name, textbox in self.special_arguments_inputs[process_type].items():
                    w.layout().addWidget(QLabel(f"{name}: "), 1, 1)
                    w.layout().addWidget(textbox, 1, 2)

        self.special_arguments_widgets[0].show()

        # add button
        self.add_process_button = QPushButton()
        self.add_process_button.setText("Add Process")
        self.add_process_button.clicked.connect(self.on_add_process)
        self.layout().addWidget(self.add_process_button)

        # connect ends
        self.add_process_button = QPushButton()
        self.add_process_button.setText("Connect Ends")
        self.add_process_button.clicked.connect(self.on_connect_ends)
        self.layout().addWidget(self.add_process_button)

    def on_process_selector_change(self, idx):
        self.selected_process_type = self.process_selector_processes[idx][0]
        for i, w in enumerate(self.special_arguments_widgets):
            if i == idx:
                w.show()
            else:
                w.hide()

    def on_add_process(self):
        args = {}
        if self.selected_process_type in self.special_arguments_inputs:
            for k, v in self.special_arguments_inputs[self.selected_process_type].items():
                if v.text() != "":
                    args[k] = eval(v.text())
        self.main_window.add_process(self.selected_process_type, args)

    def on_connect_ends(self):
        self.main_window.connect_ends()
