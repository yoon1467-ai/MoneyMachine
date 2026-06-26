from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,QLabel,QPushButton,QTextEdit,QVBoxLayout,
    QLineEdit,QProgressBar,QMessageBox,QHBoxLayout
)

from PySide6.QtCore import QThread
from app.ai.worker import ArticleWorker

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Money Machine Pro v1.1")
        self.resize(1000, 750)

        self.title = QLabel("💰 Money Machine Pro")

        self.keyword = QLineEdit()
        self.keyword.setPlaceholderText("키워드 입력")

        self.button = QPushButton("생성")
        self.cancel_btn = QPushButton("취소")
        self.cancel_btn.setEnabled(False)

        self.progress = QProgressBar()

        self.status = QLabel("대기 중")

        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        self.logs.setMaximumHeight(150)

        self.editor = QTextEdit()

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.button)
        btn_layout.addWidget(self.cancel_btn)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.keyword)
        layout.addLayout(btn_layout)
        layout.addWidget(self.progress)
        layout.addWidget(self.status)
        layout.addWidget(QLabel("실시간 로그"))
        layout.addWidget(self.logs)
        layout.addWidget(self.editor)

        self.setLayout(layout)

        self.button.clicked.connect(self.create_article)
        self.cancel_btn.clicked.connect(self.cancel_task)

    def log(self, text):
        self.logs.append(text)

    def create_article(self):

        keyword = self.keyword.text().strip()

        if not keyword:
            QMessageBox.warning(self, "알림", "키워드를 입력하세요.")
            return

        self.button.setEnabled(False)
        self.cancel_btn.setEnabled(True)

        self.thread = QThread()
        self.worker = ArticleWorker(keyword)

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.status.connect(self.status.setText)
        self.worker.status.connect(self.log)

        self.worker.finished.connect(self.finish_article)
        self.worker.error.connect(self.show_error)

        self.thread.start()

    def finish_article(self, article):

        self.editor.setMarkdown(article)

        Path("articles").mkdir(exist_ok=True)

        filename = self.keyword.text().strip().replace(" ", "_")

        with open(
            f"articles/{filename}.md",
            "w",
            encoding="utf-8"
        ) as f:
            f.write(article)

        self.log("저장 완료")

        self.button.setEnabled(True)
        self.cancel_btn.setEnabled(False)

        self.thread.quit()
        self.thread.wait()

    def cancel_task(self):

        if hasattr(self, "worker"):
            self.worker.cancel()

        self.log("작업 취소")

        self.button.setEnabled(True)
        self.cancel_btn.setEnabled(False)

    def show_error(self, msg):

        QMessageBox.critical(self, "오류", msg)

        self.log(f"오류: {msg}")

        self.button.setEnabled(True)
        self.cancel_btn.setEnabled(False)
