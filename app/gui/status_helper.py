from datetime import datetime

from app.services.log_service import write_log


def add_log(window, text):
    now = datetime.now().strftime("%H:%M:%S")
    message = f"[{now}] {text}"

    window.logs.append(message)
    write_log(text)


def update_status(window, text):
    window.status.setText(text)
    window.current_step.setText(f"현재 단계 : {text}")
    add_log(window, text)
