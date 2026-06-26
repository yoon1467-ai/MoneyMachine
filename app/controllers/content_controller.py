from PySide6.QtCore import QObject, QThread, QTimer, Slot

from app.ai.worker import ArticleWorker, ShortsWorker, ImagePromptWorker


class ContentController(QObject):
    def __init__(self, window):
        super().__init__(window)
        self.window = window

    def start_blog_worker(self, keyword):
        w = self.window

        w.set_working_buttons()
        w.progress.setValue(0)
        w.status.setText("블로그 글 작업 준비 중...")
        w.current_step.setText("현재 단계 : 시작")

        if not w.is_batch_mode:
            w.log("블로그 글 생성 시작")

        w.log(f"선택 키워드: {keyword}")

        w.thread = QThread()
        w.worker = ArticleWorker(keyword)
        w.worker.moveToThread(w.thread)

        w.thread.started.connect(w.worker.run)
        w.worker.progress.connect(w.progress.setValue)
        w.worker.status.connect(w.update_status)
        w.worker.finished.connect(self.finish_blog_article)
        w.worker.error.connect(w.show_error)

        w.thread.start()

    def start_shorts_worker(self, keyword, article_text):
        w = self.window

        w.set_working_buttons()

        w.log("쇼츠 대본 생성 시작")
        w.log(f"선택 키워드: {keyword}")

        if article_text:
            w.log("현재 블로그 글 내용을 참고해서 쇼츠를 생성합니다.")
        else:
            w.log("블로그 글 없이 키워드만으로 쇼츠를 생성합니다.")

        w.thread = QThread()
        w.worker = ShortsWorker(keyword, article_text)
        w.worker.moveToThread(w.thread)

        w.thread.started.connect(w.worker.run)
        w.worker.progress.connect(w.progress.setValue)
        w.worker.status.connect(w.update_status)
        w.worker.finished.connect(self.finish_shorts_script)
        w.worker.error.connect(w.show_error)

        w.thread.start()

    def start_image_prompt_worker(self, keyword, article_text):
        w = self.window

        w.set_working_buttons()

        w.log("이미지 프롬프트 생성 시작")
        w.log(f"선택 키워드: {keyword}")

        if article_text:
            w.log("현재 글 내용을 참고해서 이미지 프롬프트를 생성합니다.")
        else:
            w.log("글 내용 없이 키워드만으로 이미지 프롬프트를 생성합니다.")

        w.thread = QThread()
        w.worker = ImagePromptWorker(keyword, article_text)
        w.worker.moveToThread(w.thread)

        w.thread.started.connect(w.worker.run)
        w.worker.progress.connect(w.progress.setValue)
        w.worker.status.connect(w.update_status)
        w.worker.finished.connect(self.finish_image_prompts)
        w.worker.error.connect(w.show_error)

        w.thread.start()

    @Slot(dict)
    def finish_blog_article(self, result):
        w = self.window

        article = result["content"]
        saved_path = result["saved_path"]
        keyword = w.keyword.text().strip()

        if w.is_batch_mode:
            w.editor.append(f"\n\n# {keyword}\n\n")
            w.editor.append(article)
        else:
            w.editor.setMarkdown(article)

        w.progress.setValue(100)
        w.status.setText("블로그 글 생성 완료")
        w.current_step.setText("현재 단계 : 블로그 글 완료")

        w.log("✅ 블로그 글 생성 완료")
        w.log(f"✅ 저장 완료: {saved_path}")

        w.close_thread()

        if w.is_batch_mode:
            QTimer.singleShot(500, w.start_next_blog_in_queue)
        else:
            w.reset_buttons()

    @Slot(dict)
    def finish_shorts_script(self, result):
        w = self.window

        shorts_script = result["content"]
        saved_path = result["saved_path"]

        existing_text = w.editor.toPlainText().strip()

        if existing_text:
            final_text = existing_text + "\n\n---\n\n# 쇼츠 대본\n\n" + shorts_script
        else:
            final_text = "# 쇼츠 대본\n\n" + shorts_script

        w.editor.setMarkdown(final_text)

        w.progress.setValue(100)
        w.status.setText("쇼츠 대본 생성 완료")
        w.current_step.setText("현재 단계 : 쇼츠 완료")

        w.log("✅ 쇼츠 대본 생성 완료")
        w.log(f"✅ 저장 완료: {saved_path}")

        w.close_thread()
        w.reset_buttons()

    @Slot(dict)
    def finish_image_prompts(self, result):
        w = self.window

        prompts = result["content"]
        saved_path = result["saved_path"]

        existing_text = w.editor.toPlainText().strip()

        if existing_text:
            final_text = existing_text + "\n\n---\n\n# 이미지 프롬프트\n\n" + prompts
        else:
            final_text = "# 이미지 프롬프트\n\n" + prompts

        w.editor.setMarkdown(final_text)

        w.progress.setValue(100)
        w.status.setText("이미지 프롬프트 생성 완료")
        w.current_step.setText("현재 단계 : 이미지 프롬프트 완료")

        w.log("✅ 이미지 프롬프트 생성 완료")
        w.log(f"✅ 저장 완료: {saved_path}")

        w.close_thread()
        w.reset_buttons()
