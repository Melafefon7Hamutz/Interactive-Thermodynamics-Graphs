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
            (IsothermalProcess, "Isothermal Process"), (AdiabaticProcess,
                                                        "Adiabatic Process"),
            (IsobaricProcess, "Isobaric Process"), (IsochoricProcess, "Isochoric Process")]
        self.process_selector = QComboBox()
        for p, pn in self.process_selector_processes:
            self.process_selector.addItem(pn)
        self.process_selector.activated.connect(
            self.on_process_selector_change)
        self.layout().addWidget(self.process_selector)
        self.selected_process_type = self.process_selector_processes[0][0]

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

        # number of moles
        self.layout().addWidget(QLabel("Number of moles: "))
        self.default_moles = 1.0
        self.moles_input = QLineEdit()
        self.moles_input.setPlaceholderText("Number of moles")
        self.moles_input.setText(str(self.default_moles))
        self.moles_input.textChanged.connect(self.on_moles_input_change)
        self.layout().addWidget(self.moles_input)

        # degrees of freedom
        self.layout().addWidget(QLabel("Degrees of Freedom: "))
        self.default_dof = 3
        self.dof_input = QLineEdit()
        self.dof_input.setPlaceholderText("Degrees of Freedom")
        self.dof_input.setText(str(self.default_dof))
        self.dof_input.textChanged.connect(self.on_dof_input_change)
        self.layout().addWidget(self.dof_input)

        # readouts
        self.readout_widget = QWidget()
        self.readout_layout = QGridLayout(self.readout_widget)
        self.layout().addWidget(self.readout_widget)
        self.readout_labels = {
            "Work Done": QLabel("0.0"),
            "Heat Transfer": QLabel("0.0"),
            "Efficiency": QLabel("0.0"),
            "Carnot Efficiency": QLabel("0.0"),
            "Percentage of Carnot": QLabel("0.0"),
            "Min Temperature": QLabel("0.0"),
            "Max Temperature": QLabel("0.0"),
        }
        for row, (label_text, readout) in enumerate(self.readout_labels.items()):
            self.readout_layout.addWidget(QLabel(label_text + ": "), row, 0)
            self.readout_layout.addWidget(readout, row, 1)

    def on_process_selector_change(self, idx):
        self.selected_process_type = self.process_selector_processes[idx][0]

    def on_add_process(self):
        self.main_window.add_process(self.selected_process_type)

    def on_connect_ends(self):
        self.main_window.connect_ends()

    def on_moles_input_change(self):
        try:
            n = float(self.moles_input.text())
        except ValueError:
            n = self.default_moles
        self.main_window.update_moles(n)

    def on_dof_input_change(self):
        try:
            dof = int(self.dof_input.text())
        except ValueError:
            dof = self.default_dof
        self.main_window.update_dof(dof)

    def update_readouts(self, readouts):
        for label, value in readouts.items():
            if label in self.readout_labels:
                self.readout_labels[label].setText(str(value))
