from PySide6.QtCore import QObject, Signal

from app.ai.generator import generate_article


class ArticleWorker(QObject):

    finished = Signal(str)
    progress = Signal(int)
    status = Signal(str)

    def __init__(self, keyword):
        super().__init__()
        self.keyword = keyword

    def run(self):

        self.progress.emit(10)
        self.status.emit("프롬프트 생성 중...")

        self.progress.emit(25)
        self.status.emit("OpenAI 서버 연결 중...")

        self.progress.emit(40)
        self.status.emit("AI가 글을 작성 중입니다...")

        article = generate_article(self.keyword)

        self.progress.emit(90)
        self.status.emit("본문 정리 중...")

        self.finished.emit(article)

        self.progress.emit(100)
        self.status.emit("완료!")
