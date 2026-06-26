import sys

from PySide6.QtWidgets import QApplication, QMessageBox

from app.gui.main_window import MainWindow
from app.services.app_init_service import initialize_app


def main():
    try:
        initialize_app()

        app = QApplication(sys.argv)

        window = MainWindow()
        window.show()

        sys.exit(app.exec())

    except Exception as e:
        app = QApplication(sys.argv)

        QMessageBox.critical(
            None,
            "실행 오류",
            f"프로그램 실행 중 오류가 발생했습니다.\n\n{e}"
        )


if __name__ == "__main__":
    main()
