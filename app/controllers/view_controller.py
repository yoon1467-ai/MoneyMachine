from app.gui.history_view import build_history_markdown
from app.services.project_service import build_project_markdown


class ViewController:
    def __init__(self, window):
        self.window = window

    def show_projects(self):
        w = self.window

        w.logs.clear()
        w.editor.clear()

        w.progress.setValue(0)
        w.status.setText("프로젝트 관리 조회 완료")
        w.current_step.setText("현재 단계 : 프로젝트 관리")

        markdown = build_project_markdown()

        w.editor.setMarkdown(markdown)
        w.log("프로젝트 목록을 불러왔습니다.")

    def show_history(self):
        w = self.window

        w.logs.clear()
        w.editor.clear()

        w.progress.setValue(0)
        w.status.setText("생성 이력 조회 완료")
        w.current_step.setText("현재 단계 : 생성 이력")

        markdown, count = build_history_markdown(limit=50)

        w.editor.setMarkdown(markdown)

        if count == 0:
            w.log("생성 이력이 없습니다.")
        else:
            w.log(f"생성 이력 {count}개를 불러왔습니다.")
