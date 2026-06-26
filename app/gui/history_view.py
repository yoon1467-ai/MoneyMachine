from app.services.history_service import get_recent_history


def build_history_markdown(limit=50):
    rows = get_recent_history(limit=limit)

    if not rows:
        return "# 생성 이력\n\n아직 생성된 콘텐츠가 없습니다.", 0

    lines = []
    lines.append("# 생성 이력")
    lines.append("")
    lines.append("| 번호 | 키워드 | 유형 | SEO | 생성일 | 파일 |")
    lines.append("|---:|---|---|---:|---|---|")

    for index, row in enumerate(rows, start=1):
        keyword, content_type, file_path, seo_score, created_at = row
        seo_text = "-" if seo_score is None else str(seo_score)

        lines.append(
            f"| {index} | {keyword} | {content_type} | {seo_text} | {created_at} | {file_path} |"
        )

    return "\n".join(lines), len(rows)
