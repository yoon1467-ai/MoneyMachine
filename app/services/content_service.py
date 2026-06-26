from app.ai.generator import generate_article
from app.ai.seo_analyzer import analyze_seo
from app.ai.shorts_generator import generate_shorts_script
from app.ai.image_prompt_generator import generate_image_prompts
from app.services.storage_service import save_content
from app.services.history_service import add_history


def generate_blog_content(keyword):
    article = generate_article(keyword)

    seo_score, seo_report = analyze_seo(article, keyword)

    final_article = article + "\n\n" + seo_report

    saved_path = save_content(
        keyword=keyword,
        content=final_article,
        suffix="blog"
    )

    add_history(
        keyword=keyword,
        content_type="blog",
        file_path=saved_path,
        seo_score=seo_score
    )

    return {
        "content": final_article,
        "saved_path": saved_path,
        "seo_score": seo_score
    }


def generate_shorts_content(keyword, article_text=""):
    shorts_script = generate_shorts_script(
        keyword,
        article_text
    )

    saved_path = save_content(
        keyword=keyword,
        content=shorts_script,
        suffix="shorts"
    )

    add_history(
        keyword=keyword,
        content_type="shorts",
        file_path=saved_path
    )

    return {
        "content": shorts_script,
        "saved_path": saved_path
    }


def generate_image_prompt_content(keyword, article_text=""):
    prompts = generate_image_prompts(
        keyword,
        article_text
    )

    saved_path = save_content(
        keyword=keyword,
        content=prompts,
        suffix="image_prompts"
    )

    add_history(
        keyword=keyword,
        content_type="image_prompts",
        file_path=saved_path
    )

    return {
        "content": prompts,
        "saved_path": saved_path
    }
