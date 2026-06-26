from PySide6.QtCore import QObject, Signal

from app.services.content_service import (
    generate_blog_content,
    generate_shorts_content,
    generate_image_prompt_content,
)


class BaseWorker(QObject):
    finished = Signal(dict)
    progress = Signal(int)
    status = Signal(str)
    error = Signal(str)

    def __init__(self):
        super().__init__()
        self._cancel = False

    def cancel(self):
        self._cancel = True

    def is_cancelled(self):
        return self._cancel

    def emit_step(self, progress, message):
        if self.is_cancelled():
            return False

        self.progress.emit(progress)
        self.status.emit(message)
        return True


class ArticleWorker(BaseWorker):
    def __init__(self, keyword):
        super().__init__()
        self.keyword = keyword

    def run(self):
        try:
            if not self.emit_step(10, "블로그 글 작업 준비 중..."):
                return

            if not self.emit_step(30, "블로그 글 생성 중..."):
                return

            result = generate_blog_content(self.keyword)

            if self.is_cancelled():
                self.status.emit("작업이 취소되었습니다.")
                return

            if not self.emit_step(90, "블로그 글 저장 중..."):
                return

            self.finished.emit(result)

            self.progress.emit(100)
            self.status.emit(f"블로그 글 생성 완료 / SEO {result['seo_score']}점")

        except Exception as e:
            self.error.emit(str(e))


class ShortsWorker(BaseWorker):
    def __init__(self, keyword, article_text=""):
        super().__init__()
        self.keyword = keyword
        self.article_text = article_text

    def run(self):
        try:
            if not self.emit_step(10, "쇼츠 작업 준비 중..."):
                return

            if not self.emit_step(50, "쇼츠 대본 생성 중..."):
                return

            result = generate_shorts_content(
                self.keyword,
                self.article_text
            )

            if self.is_cancelled():
                self.status.emit("작업이 취소되었습니다.")
                return

            if not self.emit_step(90, "쇼츠 대본 저장 중..."):
                return

            self.finished.emit(result)

            self.progress.emit(100)
            self.status.emit("쇼츠 대본 생성 완료")

        except Exception as e:
            self.error.emit(str(e))


class ImagePromptWorker(BaseWorker):
    def __init__(self, keyword, article_text=""):
        super().__init__()
        self.keyword = keyword
        self.article_text = article_text

    def run(self):
        try:
            if not self.emit_step(10, "이미지 프롬프트 준비 중..."):
                return

            if not self.emit_step(50, "이미지 프롬프트 생성 중..."):
                return

            result = generate_image_prompt_content(
                self.keyword,
                self.article_text
            )

            if self.is_cancelled():
                self.status.emit("작업이 취소되었습니다.")
                return

            if not self.emit_step(90, "이미지 프롬프트 저장 중..."):
                return

            self.finished.emit(result)

            self.progress.emit(100)
            self.status.emit("이미지 프롬프트 생성 완료")

        except Exception as e:
            self.error.emit(str(e))
