from PySide6.QtCore import QObject, QThread, Slot

from app.workers.blogger_worker import BloggerPublishWorker


class PublishController(QObject):
    def __init__(self, window):
        super().__init__(window)
        self.window = window

    def publish_blogger_draft(self):
        w = self.window

        content = w.editor.toPlainText().strip()

        if not content:
            w.show_warning("알림", "Blogger에 저장할 글이 없습니다.")
            return

        title = self.extract_title(content)
        keyword = w.keyword.text().strip()

        labels = []

        if keyword:
            labels.append(keyword)

        w.set_working_buttons()
        w.progress.setValue(0)
        w.status.setText("Blogger 초안 저장 준비 중...")
        w.current_step.setText("현재 단계 : Blogger 초안")

        w.log("Blogger 초안 저장 시작")
        w.log(f"제목: {title}")

        w.thread = QThread()
        w.worker = BloggerPublishWorker(
            title=title,
            content=content,
            labels=labels,
            is_draft=True
        )

        w.worker.moveToThread(w.thread)

        w.thread.started.connect(w.worker.run)
        w.worker.progress.connect(w.progress.setValue)
        w.worker.status.connect(w.update_status)
        w.worker.finished.connect(self.finish_blogger_publish)
        w.worker.error.connect(w.show_error)

        w.thread.start()

    def extract_title(self, content):
        for line in content.splitlines():
            line = line.strip()

            if line.startswith("# "):
                return line.replace("# ", "").strip()

            if line and not line.startswith("---"):
                return line[:80]

        return "Money Machine Pro Draft"

    @Slot(dict)
    def finish_blogger_publish(self, post):
        w = self.window

        post_url = post.get("url", "")
        post_id = post.get("id", "")

        w.progress.setValue(100)
        w.status.setText("Blogger 초안 저장 완료")
        w.current_step.setText("현재 단계 : Blogger 초안 완료")

        w.log("✅ Blogger 초안 저장 완료")

        if post_id:
            w.log(f"✅ Post ID: {post_id}")

        if post_url:
            w.log(f"✅ URL: {post_url}")

        w.close_thread()
        w.reset_buttons()
