from PySide6.QtWidgets import (
    QWidget,
    QMessageBox,
)

from app.gui.ui_builder import build_main_ui
from app.gui.event_binder import bind_main_events
from app.gui.status_helper import add_log, update_status

from app.gui.button_state import (
    set_recommend_loading_buttons as enable_loading_buttons,
    set_working_buttons as enable_working_buttons,
    reset_buttons as enable_idle_buttons,
)

from app.services.reset_service import clear_test_data as reset_test_data

from app.controllers.content_controller import ContentController
from app.controllers.keyword_controller import KeywordController
from app.controllers.view_controller import ViewController
from app.controllers.queue_controller import QueueController


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Money Machine Pro v4.6")
        self.resize(1150, 900)

        self.thread = None
        self.worker = None

        self.blog_queue = []
        self.is_batch_mode = False
        self.current_batch_index = 0
        self.total_batch_count = 0

        build_main_ui(self)
        bind_main_events(self)

        self.content_controller = ContentController(self)
        self.keyword_controller = KeywordController(self)
        self.view_controller = ViewController(self)
        self.queue_controller = QueueController(self)

    def log(self, text):
        add_log(self, text)

    def update_status(self, text):
        update_status(self, text)

    def show_warning(self, title, message):
        QMessageBox.warning(self, title, message)

    def show_preview(self):
        self.show_warning("알림", "HTML 미리보기 기능은 다음 단계에서 연결됩니다.")

    def show_projects(self):
        self.view_controller.show_projects()

    def show_history(self):
        self.view_controller.show_history()

    def clear_test_data(self):
        reply = QMessageBox.question(
            self,
            "테스트 데이터 삭제",
            "articles 폴더와 생성 이력 DB를 모두 삭제할까요?\n\n"
            "삭제하면 추천 키워드 중복 제외 기록도 초기화됩니다.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        try:
            reset_test_data()

            self.keyword_list.clear()
            self.keyword.clear()
            self.editor.clear()
            self.logs.clear()
            self.progress.setValue(0)
            self.status.setText("테스트 데이터 삭제 완료")
            self.current_step.setText("현재 단계 : 초기화 완료")

            self.log("✅ articles 폴더 초기화 완료")
            self.log("✅ 생성 이력 DB 초기화 완료")
            self.log("✅ 추천 키워드 중복 제외 기록이 초기화되었습니다.")

            QMessageBox.information(self, "완료", "테스트 데이터가 삭제되었습니다.")

        except Exception as e:
            QMessageBox.critical(
                self,
                "오류",
                f"테스트 데이터 삭제 중 오류가 발생했습니다.\n{e}"
            )

    def load_recommended_keywords(self):
        self.keyword_controller.load_keywords()

    def select_keyword(self, item):
        keyword = item.data(1000)
        self.keyword.setText(keyword)
        self.log(f"키워드 선택: {keyword}")

    def select_and_create_blog(self, item):
        keyword = item.data(1000)
        self.keyword.setText(keyword)
        self.create_blog_article()

    def create_blog_article(self):
        keyword = self.keyword.text().strip()

        if not keyword:
            self.show_warning("알림", "키워드를 입력하거나 추천 키워드를 선택하세요.")
            return

        self.is_batch_mode = False
        self.blog_queue = []
        self.current_batch_index = 0
        self.total_batch_count = 0

        self.logs.clear()
        self.editor.clear()

        self.start_blog_worker(keyword)

    def create_batch_blog_articles(self):
        self.queue_controller.create_batch_blog_articles()

    def start_next_blog_in_queue(self):
        self.queue_controller.start_next_blog_in_queue()

    def start_blog_worker(self, keyword):
        self.content_controller.start_blog_worker(keyword)

    def create_shorts_script(self):
        keyword = self.keyword.text().strip()

        if not keyword:
            self.show_warning("알림", "키워드를 입력하거나 추천 키워드를 선택하세요.")
            return

        article_text = self.editor.toPlainText().strip()

        self.is_batch_mode = False
        self.logs.clear()
        self.progress.setValue(0)
        self.status.setText("쇼츠 대본 작업 준비 중...")
        self.current_step.setText("현재 단계 : 시작")

        self.content_controller.start_shorts_worker(keyword, article_text)

    def create_image_prompts(self):
        keyword = self.keyword.text().strip()

        if not keyword:
            self.show_warning("알림", "키워드를 입력하거나 추천 키워드를 선택하세요.")
            return

        article_text = self.editor.toPlainText().strip()

        self.is_batch_mode = False
        self.logs.clear()
        self.progress.setValue(0)
        self.status.setText("이미지 프롬프트 작업 준비 중...")
        self.current_step.setText("현재 단계 : 시작")

        self.content_controller.start_image_prompt_worker(keyword, article_text)

    def cancel_task(self):
        if self.worker:
            self.worker.cancel()

        self.blog_queue = []
        self.is_batch_mode = False
        self.current_batch_index = 0
        self.total_batch_count = 0

        self.progress.setValue(0)
        self.status.setText("작업 취소")
        self.current_step.setText("현재 단계 : 작업 취소")
        self.log("⚠ 작업이 취소되었습니다.")

        self.reset_buttons()
        self.close_thread()

    def show_error(self, msg):
        self.blog_queue = []
        self.is_batch_mode = False

        self.progress.setValue(0)
        self.status.setText("오류 발생")
        self.current_step.setText("현재 단계 : 오류 발생")
        self.log(f"❌ 오류: {msg}")

        QMessageBox.critical(self, "오류", msg)

        self.reset_buttons()
        self.close_thread()

    def set_recommend_loading_buttons(self):
        enable_loading_buttons(self)

    def set_working_buttons(self):
        enable_working_buttons(self)

    def reset_buttons(self):
        enable_idle_buttons(self)

    def close_thread(self):
        if self.thread:
            thread = self.thread
            self.thread = None
            self.worker = None

            thread.quit()
            thread.wait()
