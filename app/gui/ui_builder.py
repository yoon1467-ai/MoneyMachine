from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QProgressBar,
    QListWidget,
    QAbstractItemView,
)


def build_main_ui(window):
    window.title = QLabel("💰 Money Machine Pro v4.7")
    window.title.setStyleSheet("font-size:26px; font-weight:bold; padding:10px;")

    window.recommend_btn = QPushButton("오늘의 추천 TOP10")
    window.recommend_btn.setMinimumHeight(38)

    window.project_btn = QPushButton("프로젝트 관리")
    window.project_btn.setMinimumHeight(38)

    window.history_btn = QPushButton("생성 이력 보기")
    window.history_btn.setMinimumHeight(38)

    window.reset_data_btn = QPushButton("테스트 데이터 삭제")
    window.reset_data_btn.setMinimumHeight(38)

    window.keyword_list = QListWidget()
    window.keyword_list.setMinimumHeight(180)
    window.keyword_list.setSelectionMode(QAbstractItemView.MultiSelection)

    window.keyword = QLineEdit()
    window.keyword.setPlaceholderText("추천 키워드를 선택하거나 직접 입력하세요.")
    window.keyword.setMinimumHeight(36)

    window.blog_btn = QPushButton("블로그 글 생성")
    window.blog_btn.setMinimumHeight(38)

    window.batch_blog_btn = QPushButton("선택 키워드 일괄 생성")
    window.batch_blog_btn.setMinimumHeight(38)

    window.shorts_btn = QPushButton("쇼츠 대본 생성")
    window.shorts_btn.setMinimumHeight(38)

    window.image_prompt_btn = QPushButton("이미지 프롬프트 생성")
    window.image_prompt_btn.setMinimumHeight(38)

    window.preview_btn = QPushButton("HTML 미리보기")
    window.preview_btn.setMinimumHeight(38)

    window.blogger_draft_btn = QPushButton("Blogger 초안 저장")
    window.blogger_draft_btn.setMinimumHeight(38)

    window.cancel_btn = QPushButton("취소")
    window.cancel_btn.setMinimumHeight(38)
    window.cancel_btn.setEnabled(False)

    window.progress = QProgressBar()
    window.progress.setRange(0, 100)
    window.progress.setValue(0)
    window.progress.setFormat("%p% 완료")

    window.current_step = QLabel("현재 단계 : 대기")
    window.current_step.setStyleSheet("font-weight:bold; color:#2196F3; padding:4px;")

    window.status = QLabel("대기 중")

    window.logs = QTextEdit()
    window.logs.setReadOnly(True)
    window.logs.setMaximumHeight(160)

    window.editor = QTextEdit()

    top_btn_layout = QHBoxLayout()
    top_btn_layout.addWidget(window.recommend_btn)
    top_btn_layout.addWidget(window.project_btn)
    top_btn_layout.addWidget(window.history_btn)
    top_btn_layout.addWidget(window.reset_data_btn)

    action_btn_layout = QHBoxLayout()
    action_btn_layout.addWidget(window.blog_btn)
    action_btn_layout.addWidget(window.batch_blog_btn)
    action_btn_layout.addWidget(window.shorts_btn)
    action_btn_layout.addWidget(window.image_prompt_btn)
    action_btn_layout.addWidget(window.preview_btn)
    action_btn_layout.addWidget(window.blogger_draft_btn)
    action_btn_layout.addWidget(window.cancel_btn)

    layout = QVBoxLayout()
    layout.addWidget(window.title)
    layout.addLayout(top_btn_layout)
    layout.addWidget(QLabel("오늘의 추천 키워드"))
    layout.addWidget(window.keyword_list)
    layout.addWidget(QLabel("선택 키워드"))
    layout.addWidget(window.keyword)
    layout.addLayout(action_btn_layout)
    layout.addWidget(window.progress)
    layout.addWidget(window.current_step)
    layout.addWidget(window.status)
    layout.addWidget(QLabel("실시간 로그"))
    layout.addWidget(window.logs)
    layout.addWidget(QLabel("생성 결과"))
    layout.addWidget(window.editor)

    window.setLayout(layout)
