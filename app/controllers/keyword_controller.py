from PySide6.QtCore import QObject, QThread

from app.workers.keyword_worker import KeywordWorker
from app.gui.keyword_list_view import render_keyword_list


class KeywordController(QObject):
    def __init__(self, window):
        super().__init__(window)
        self.window = window

    def load_keywords(self):
        w = self.window

        try:
            w.set_recommend_loading_buttons()

            w.keyword_list.clear()
            w.logs.clear()
            w.progress.setValue(5)
            w.update_status("오늘의 추천 키워드 수집 중...")

            w.thread = QThread()
            w.worker = KeywordWorker()
            w.worker.moveToThread(w.thread)

            w.thread.started.connect(w.worker.run)
            w.worker.progress.connect(w.progress.setValue)
            w.worker.status.connect(w.update_status)
            w.worker.finished.connect(self.finish_keyword_recommendation)
            w.worker.error.connect(w.show_error)

            w.thread.start()

        except Exception as e:
            w.show_error(str(e))

    def finish_keyword_recommendation(self, keywords):
        w = self.window

        render_keyword_list(w, keywords)

        w.progress.setValue(100)
        w.status.setText("추천 키워드 생성 완료")
        w.current_step.setText("현재 단계 : 추천 완료")

        w.log("추천 키워드 생성 완료")
        w.log("여러 개 선택 후 '선택 키워드 일괄 생성'을 누르면 순서대로 생성됩니다.")
        w.log("더블클릭하면 해당 키워드 블로그 글 하나만 바로 생성됩니다.")

        w.close_thread()
        w.reset_buttons()
