import sys
from PyQt5.QtWidgets import QApplication

from MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)

    # Create and show main window
    window = MainWindow(app.primaryScreen().size())
    window.show()

    # Start event loop
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


# TODO
# add st graph

# ability to remove points and open the cycle
# add points at other locations than end
# ability to split point into two

# size of autorange button

# ? presice inputs

# ?? custom processes
