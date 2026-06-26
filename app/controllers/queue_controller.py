class QueueController:
    def __init__(self, window):
        self.window = window

    def create_batch_blog_articles(self):
        w = self.window
        selected_items = w.keyword_list.selectedItems()

        if not selected_items:
            w.show_warning("알림", "일괄 생성할 추천 키워드를 1개 이상 선택하세요.")
            return

        keywords = []

        for item in selected_items:
            keyword = item.data(1000)

            if keyword and keyword not in keywords:
                keywords.append(keyword)

        if not keywords:
            w.show_warning("알림", "선택된 키워드를 읽을 수 없습니다.")
            return

        w.is_batch_mode = True
        w.blog_queue = keywords
        w.current_batch_index = 0
        w.total_batch_count = len(keywords)

        w.logs.clear()
        w.editor.clear()
        w.progress.setValue(0)

        w.log(f"일괄 생성 시작: 총 {w.total_batch_count}개")

        self.start_next_blog_in_queue()

    def start_next_blog_in_queue(self):
        w = self.window

        if not w.blog_queue:
            w.progress.setValue(100)
            w.status.setText("일괄 생성 완료")
            w.current_step.setText("현재 단계 : 일괄 생성 완료")
            w.log("✅ 모든 키워드 생성 완료")
            w.reset_buttons()
            return

        keyword = w.blog_queue.pop(0)
        w.current_batch_index += 1
        w.keyword.setText(keyword)

        w.log("")
        w.log("========================================")
        w.log(f"{w.current_batch_index}/{w.total_batch_count} 번째 글 생성")
        w.log(f"키워드: {keyword}")
        w.log("========================================")

        w.start_blog_worker(keyword)
