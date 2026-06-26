from PySide6.QtCore import QObject, Signal
from app.ai.generator import generate_article

class ArticleWorker(QObject):

    finished = Signal(str)
    progress = Signal(int)
    status = Signal(str)
    error = Signal(str)

    def __init__(self, keyword):
        super().__init__()
        self.keyword = keyword
        self._cancel = False

    def cancel(self):
        self._cancel = True

    def run(self):
        try:
            self.progress.emit(10)
            self.status.emit("프롬프트 생성 중...")

            if self._cancel:
                return

            self.progress.emit(30)
            self.status.emit("OpenAI 연결 중...")

            if self._cancel:
                return

            self.progress.emit(50)
            self.status.emit("본문 생성 중...")

            article = generate_article(self.keyword)

            if self._cancel:
                return

            self.progress.emit(90)
            self.status.emit("후처리 중...")

            self.finished.emit(article)

            self.progress.emit(100)
            self.status.emit("완료!")

        except Exception as e:
            self.error.emit(str(e))
