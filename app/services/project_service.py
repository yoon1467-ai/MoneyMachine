from app.services.history_service import get_recent_history


def get_project_list(limit=100):
    rows = get_recent_history(limit=limit)

    projects = {}

    for row in rows:
        keyword, content_type, file_path, seo_score, created_at = row

        if keyword not in projects:
            projects[keyword] = {
                "keyword": keyword,
                "blog": False,
                "shorts": False,
                "image_prompts": False,
                "seo_score": "-",
                "latest_date": created_at,
                "files": []
            }

        if content_type == "blog":
            projects[keyword]["blog"] = True

        if content_type == "shorts":
            projects[keyword]["shorts"] = True

        if content_type == "image_prompts":
            projects[keyword]["image_prompts"] = True

        if seo_score is not None:
            projects[keyword]["seo_score"] = seo_score

        projects[keyword]["latest_date"] = created_at
        projects[keyword]["files"].append(file_path)

    return list(projects.values())


def build_project_markdown():
    projects = get_project_list()

    if not projects:
        return "# 프로젝트 관리\n\n아직 생성된 프로젝트가 없습니다."

    lines = []
    lines.append("# 프로젝트 관리")
    lines.append("")
    lines.append("| 번호 | 키워드 | 블로그 | 쇼츠 | 이미지 | SEO | 최근 생성일 |")
    lines.append("|---:|---|---|---|---|---:|---|")

    for index, project in enumerate(projects, start=1):
        blog = "✅" if project["blog"] else "❌"
        shorts = "✅" if project["shorts"] else "❌"
        image = "✅" if project["image_prompts"] else "❌"

        lines.append(
            f"| {index} | {project['keyword']} | {blog} | {shorts} | {image} | "
            f"{project['seo_score']} | {project['latest_date']} |"
        )

    return "\n".join(lines)
