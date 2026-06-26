from PySide6.QtCore import QObject, Signal

from app.services.blogger_service import publish_post


class BloggerPublishWorker(QObject):
    finished = Signal(dict)
    progress = Signal(int)
    status = Signal(str)
    error = Signal(str)

    def __init__(self, title, content, labels=None, is_draft=True):
        super().__init__()
        self.title = title
        self.content = content
        self.labels = labels or []
        self.is_draft = is_draft
        self._cancel = False

    def cancel(self):
        self._cancel = True

    def run(self):
        try:
            self.progress.emit(10)
            self.status.emit("Blogger 게시 준비 중...")

            if self._cancel:
                return

            self.progress.emit(50)
            self.status.emit("Blogger 초안 저장 중...")

            post = publish_post(
                title=self.title,
                content=self.content,
                labels=self.labels,
                is_draft=self.is_draft
            )

            if self._cancel:
                return

            self.progress.emit(100)
            self.status.emit("Blogger 초안 저장 완료")

            self.finished.emit(post)

        except Exception as e:
            self.error.emit(str(e))
