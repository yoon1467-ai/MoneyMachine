import markdown


def markdown_to_html(markdown_text):
    body = markdown.markdown(
        markdown_text,
        extensions=[
            "tables",
            "fenced_code",
            "nl2br"
        ]
    )

    html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.7;
            max-width: 860px;
            margin: 40px auto;
            padding: 20px;
            color: #222;
        }}
        h1 {{
            font-size: 32px;
            border-bottom: 2px solid #ddd;
            padding-bottom: 10px;
        }}
        h2 {{
            margin-top: 36px;
            font-size: 24px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 10px;
        }}
        th {{
            background: #f5f5f5;
        }}
        code {{
            background: #f3f3f3;
            padding: 2px 4px;
        }}
    </style>
</head>
<body>
{body}
</body>
</html>
"""
    return html
