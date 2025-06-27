import sys
from PyQt5.QtWidgets import QApplication

from MainWindow import MainWindow



def main():
    app = QApplication(sys.argv)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


# TODO
# for each process add functions for heat and work
# display work, input heat, effitiency
# ? find temperature bounds and find carnot's effitiency
# add st graph

# ability to remove points and open the cycle
# add points at other locations than end
# ability to split point into two

# size of autorange button

# number of moles (slider ?)

# ? presice inputs

# ?? custom processes