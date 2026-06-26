from pathlib import Path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from app.services.config_service import load_config


SCOPES = ["https://www.googleapis.com/auth/blogger"]


def get_blogger_service():
    config = load_config()

    credentials_path = Path(config["blogger_credentials_file"])
    token_path = Path("config") / "blogger_token.json"

    if not credentials_path.exists():
        raise FileNotFoundError(
            "Blogger 인증 파일이 없습니다.\n"
            "Google Cloud에서 OAuth Client JSON을 받은 뒤 "
            "config/blogger_credentials.json 으로 저장하세요."
        )

    creds = None

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(
            str(token_path),
            SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path),
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        token_path.parent.mkdir(parents=True, exist_ok=True)

        with open(token_path, "w", encoding="utf-8") as token_file:
            token_file.write(creds.to_json())

    return build("blogger", "v3", credentials=creds)


def publish_post(title, content, labels=None, is_draft=True):
    config = load_config()
    blog_id = config.get("blogger_blog_id", "")

    if not blog_id:
        raise ValueError(
            "config/settings.json에 blogger_blog_id가 없습니다."
        )

    service = get_blogger_service()

    body = {
        "title": title,
        "content": content,
    }

    if labels:
        body["labels"] = labels

    post = service.posts().insert(
        blogId=blog_id,
        body=body,
        isDraft=is_draft
    ).execute()

    return post
