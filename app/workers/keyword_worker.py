from PySide6.QtCore import QObject, Signal

from app.ai.keyword_ai import recommend_keywords


class KeywordWorker(QObject):
    finished = Signal(list)
    progress = Signal(int)
    status = Signal(str)
    error = Signal(str)

    def run(self):
        try:
            self.progress.emit(10)
            self.status.emit("추천 키워드 후보 수집 중...")

            self.progress.emit(40)
            self.status.emit("구글/네이버 자동완성 분석 중...")

            self.progress.emit(70)
            self.status.emit("AI가 TOP10 선정 중...")

            keywords = recommend_keywords()

            self.progress.emit(100)
            self.status.emit("추천 키워드 생성 완료")

            self.finished.emit(keywords)

        except Exception as e:
            self.error.emit(str(e))
