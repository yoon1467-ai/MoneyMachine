from PySide6.QtWidgets import QListWidgetItem


def render_keyword_list(window, keywords):
    window.keyword_list.clear()

    for index, item in enumerate(keywords, start=1):
        text = (
            f"{index}위 | 추천도 {item['score']}점 | "
            f"{item['keyword']} | {item['reason']}"
        )

        list_item = QListWidgetItem(text)
        list_item.setData(1000, item["keyword"])
        window.keyword_list.addItem(list_item)
