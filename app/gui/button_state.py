def set_recommend_loading_buttons(window):
    window.recommend_btn.setEnabled(False)
    window.project_btn.setEnabled(False)
    window.history_btn.setEnabled(False)
    window.reset_data_btn.setEnabled(False)

    window.blog_btn.setEnabled(False)
    window.batch_blog_btn.setEnabled(False)
    window.shorts_btn.setEnabled(False)
    window.image_prompt_btn.setEnabled(False)
    window.preview_btn.setEnabled(False)
    window.cancel_btn.setEnabled(False)


def set_working_buttons(window):
    window.recommend_btn.setEnabled(False)
    window.project_btn.setEnabled(False)
    window.history_btn.setEnabled(False)
    window.reset_data_btn.setEnabled(False)

    window.blog_btn.setEnabled(False)
    window.batch_blog_btn.setEnabled(False)
    window.shorts_btn.setEnabled(False)
    window.image_prompt_btn.setEnabled(False)
    window.preview_btn.setEnabled(False)
    window.cancel_btn.setEnabled(True)


def reset_buttons(window):
    window.recommend_btn.setEnabled(True)
    window.project_btn.setEnabled(True)
    window.history_btn.setEnabled(True)
    window.reset_data_btn.setEnabled(True)

    window.blog_btn.setEnabled(True)
    window.batch_blog_btn.setEnabled(True)
    window.shorts_btn.setEnabled(True)
    window.image_prompt_btn.setEnabled(True)
    window.preview_btn.setEnabled(True)
    window.cancel_btn.setEnabled(False)
