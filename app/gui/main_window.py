from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QLineEdit,
    QProgressBar,
    QMessageBox
)

from PySide6.QtCore import QThread

from app.ai.worker import ArticleWorker


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Money Machine AI")
        self.resize(900, 700)

        self.title = QLabel("💰 Money Machine AI")

        self.keyword = QLineEdit()
        self.keyword.setPlaceholderText("키워드를 입력하세요")

        self.button = QPushButton("AI 글 생성")

        self.progress = QProgressBar()
        self.progress.setValue(0)

        self.status = QLabel("대기 중")

        self.editor = QTextEdit()

        layout = QVBoxLayout()

        layout.addWidget(self.title)
        layout.addWidget(self.keyword)
        layout.addWidget(self.button)
        layout.addWidget(self.progress)
        layout.addWidget(self.status)
        layout.addWidget(self.editor)

        self.setLayout(layout)

        self.button.clicked.connect(self.create_article)

    def create_article(self):

        keyword = self.keyword.text().strip()

        if keyword == "":
            QMessageBox.warning(
                self,
                "알림",
                "키워드를 입력하세요."
            )
            return

        self.button.setEnabled(False)
        self.progress.setValue(0)

        self.thread = QThread()

        self.worker = ArticleWorker(keyword)

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)

        self.worker.progress.connect(
            self.progress.setValue
        )

        self.worker.status.connect(
            self.status.setText
        )

        self.worker.finished.connect(
            self.finish_article
        )

        self.thread.start()

    def finish_article(self, article):

        self.editor.setMarkdown(article)

        self.button.setEnabled(True)

        self.thread.quit()
        self.thread.wait()
