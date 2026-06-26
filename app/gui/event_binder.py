def bind_main_events(window):
    window.recommend_btn.clicked.connect(window.load_recommended_keywords)
    window.project_btn.clicked.connect(window.show_projects)
    window.history_btn.clicked.connect(window.show_history)
    window.reset_data_btn.clicked.connect(window.clear_test_data)

    window.keyword_list.itemClicked.connect(window.select_keyword)
    window.keyword_list.itemDoubleClicked.connect(window.select_and_create_blog)

    window.blog_btn.clicked.connect(window.create_blog_article)
    window.batch_blog_btn.clicked.connect(window.create_batch_blog_articles)
    window.shorts_btn.clicked.connect(window.create_shorts_script)
    window.image_prompt_btn.clicked.connect(window.create_image_prompts)

    if hasattr(window, "preview_btn") and hasattr(window, "show_preview"):
        window.preview_btn.clicked.connect(window.show_preview)

    if hasattr(window, "blogger_draft_btn") and hasattr(window, "publish_blogger_draft"):
        window.blogger_draft_btn.clicked.connect(window.publish_blogger_draft)

    window.cancel_btn.clicked.connect(window.cancel_task)
