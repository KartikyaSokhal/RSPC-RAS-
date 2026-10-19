import difflib
import re
from django.db.models import Q
from ..models import Topic, LearningResource, ResourcePage, TopicPublication
from .publication import visible_publications


def extract_words(text):
    return [w.casefold() for w in re.findall(r'\w+', text, re.UNICODE) if len(w) > 1]


def search(query, page=1):
    normalized = re.sub(r'\s+', ' ', query).strip()
    words = extract_words(normalized)[:8]
    if not words:
        return {'results': [], 'total': 0, 'page': page, 'has_more': False, 'suggestion': None}

    pubs = visible_publications()
    all_topics = list(Topic.objects.all().select_related('parent'))
    topics_by_id = {t.id: t for t in all_topics}

    # Build vocabulary for typo-tolerance across syllabus topics and published content
    vocab = set()
    for t in all_topics:
        for w in extract_words(t.title):
            if len(w) > 3:
                vocab.add(w)
    for p in pubs.values():
        for w in extract_words(p.search_text):
            if len(w) > 3:
                vocab.add(w)

    # Check for typo suggestion using difflib
    suggestion_words = []
    has_typo = False
    for w in words:
        if w in vocab or any(w in term for term in vocab):
            suggestion_words.append(w)
        else:
            close = difflib.get_close_matches(w, vocab, n=1, cutoff=0.72)
            if close:
                suggestion_words.append(close[0])
                has_typo = True
            else:
                suggestion_words.append(w)

    suggestion = ' '.join(suggestion_words) if has_typo else None

    # Determine effective search terms (include suggestions if typo detected)
    search_terms = list(words)
    if has_typo:
        for sw in suggestion_words:
            if sw not in search_terms:
                search_terms.append(sw)

    def get_path(t):
        p = []
        curr = t
        while curr:
            p.append(curr.title)
            curr = curr.parent
        return list(reversed(p))

    rows = []
    seen_ids = set()

    def add_result(title, snippet, url, path, kind, source_id, base_score, has_notes=True):
        if source_id in seen_ids:
            return
        seen_ids.add(source_id)
        rows.append({
            'title': title,
            'snippet': snippet,
            'url': url,
            'path': path,
            'kind': kind,
            'source_id': source_id,
            'score': base_score,
            'has_notes': has_notes,
        })

    all_pubs = {p.topic_id: p for p in TopicPublication.objects.all()}

    def is_withdrawn(t):
        curr = t
        while curr:
            p_rec = all_pubs.get(curr.id)
            if p_rec is not None and not p_rec.is_published:
                return True
            curr = curr.parent
        return False

    # 1. Search all discoverable topics (titles and ancestors)
    for t in all_topics:
        if is_withdrawn(t):
            continue

        pub = pubs.get(t.id)
        t_title = pub.title if pub else t.title
        t_slug = pub.snapshot.get('slug', t.slug) if pub else t.slug
        t_title_lower = t_title.casefold()

        # Compute visible breadcrumb path
        p = []
        curr = t
        while curr:
            c_pub = pubs.get(curr.id)
            p.append(c_pub.title if c_pub else curr.title)
            curr = curr.parent
        t_path = list(reversed(p))
        path_lower = ' '.join(t_path).casefold()

        # Calculate topic score
        score = 0
        if normalized.casefold() in t_title_lower:
            score += 80
        for w in search_terms:
            if w == t_title_lower:
                score += 50
            elif w in t_title_lower:
                score += 30
            elif w in path_lower:
                score += 10

        # Also match published note text if publication exists
        pub_snippet = ''
        if pub and pub.search_text:
            st_lower = pub.search_text.casefold()
            for w in search_terms:
                if w in st_lower:
                    score += 5
            at = min((pub.search_text.casefold().find(w) for w in search_terms if w in pub.search_text.casefold()), default=-1)
            if at >= 0:
                start = max(0, at - 60)
                pub_snippet = ('…' if start else '') + pub.search_text[start:start + 200] + ('…' if len(pub.search_text) > start + 200 else '')

        if score > 0:
            has_notes = bool(pub and pub.snapshot.get('blocks'))
            kind = 'lesson' if has_notes else 'topic'
            snippet = pub_snippet if pub_snippet else (
                f"Syllabus topic in {t_path[0]}" if len(t_path) > 1 else "Syllabus main curriculum stream."
            )
            add_result(
                title=t_title,
                snippet=snippet,
                url=f"/topic/{t_slug}",
                path=t_path,
                kind=kind,
                source_id=f"t{t.id}",
                base_score=score,
                has_notes=has_notes
            )


    # 2. Approved PDF pages
    approved_ids = {rid for p in pubs.values() for rid in p.snapshot.get('resource_ids', [])}
    if approved_ids:
        resources = {r.pk: r for r in LearningResource.objects.filter(pk__in=approved_ids, topic_id__in=pubs, status='approved')[:1000]}
        match = Q()
        for word in search_terms:
            match |= Q(text__icontains=word)
        for resource_page in ResourcePage.objects.filter(match, resource_id__in=resources).order_by('resource_id', 'page_number')[:500]:
            resource = resources[resource_page.resource_id]
            pub = pubs[resource.topic_id]
            if resource.pk not in pub.snapshot.get('resource_ids', []):
                continue
            text_lower = resource_page.text.casefold()
            pdf_score = sum(text_lower.count(w) * 2 for w in search_terms if w in text_lower)
            if resource.title.casefold() in normalized.casefold():
                pdf_score += 20
            at = min((resource_page.text.casefold().find(w) for w in search_terms if w in resource_page.text.casefold()), default=0)
            start = max(0, at - 60)
            snippet = ('…' if start else '') + resource_page.text[start:start + 200] + ('…' if len(resource_page.text) > start + 200 else '')
            topic_obj = topics_by_id.get(pub.topic_id)
            pdf_path = get_path(topic_obj) if topic_obj else [pub.title]
            add_result(
                title=f"{resource.title} · page {resource_page.page_number}",
                snippet=snippet,
                url=f"/resources/{resource.pk}?page={resource_page.page_number}",
                path=pdf_path,
                kind='pdf',
                source_id=f"r{resource.pk}p{resource_page.page_number}",
                base_score=pdf_score,
                has_notes=True
            )

    rows.sort(key=lambda r: (-r['score'], r['source_id']))
    total = len(rows)
    paged = rows[(page - 1) * 20 : page * 20]
    results = [{k: v for k, v in r.items() if k != 'score'} for r in paged]

    return {
        'results': results,
        'total': total,
        'page': page,
        'has_more': total > page * 20,
        'suggestion': suggestion
    }

