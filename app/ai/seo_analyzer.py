def analyze_seo(article, keyword):
    score = 0
    checks = []

    if keyword in article:
        score += 20
        checks.append("✅ 키워드 포함")
    else:
        checks.append("❌ 키워드 부족")

    if article.count("##") >= 4:
        score += 20
        checks.append("✅ H2 구조 충분")
    else:
        checks.append("❌ H2 구조 부족")

    if "|" in article and "---" in article:
        score += 15
        checks.append("✅ 표 포함")
    else:
        checks.append("❌ 표 부족")

    if "FAQ" in article or "자주 묻는 질문" in article:
        score += 15
        checks.append("✅ FAQ 포함")
    else:
        checks.append("❌ FAQ 부족")

    if "메타 설명" in article:
        score += 10
        checks.append("✅ 메타 설명 포함")
    else:
        checks.append("❌ 메타 설명 부족")

    if "태그" in article:
        score += 10
        checks.append("✅ 태그 포함")
    else:
        checks.append("❌ 태그 부족")

    if len(article) >= 2500:
        score += 10
        checks.append("✅ 글 길이 충분")
    else:
        checks.append("❌ 글 길이 부족")

    report = f"""
---

## SEO 자동 점검 결과

**SEO 점수: {score} / 100**

{chr(10).join(checks)}

### 개선 기준
- 80점 이상: 발행 가능
- 90점 이상: 우수
- 95점 이상: 매우 우수
"""

    return score, report
