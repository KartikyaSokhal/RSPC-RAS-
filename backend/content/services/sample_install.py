"""Canonical sample installation shared by separately guarded local/free-demo workflows."""
from django.contrib.auth import get_user_model
from django.db import transaction

from content.models import (Topic, ContentBlock, Quiz, Question, Choice, Tag,
                            TopicAlias, TopicRelation, KeywordLinkProposal, normalized_label)
from content.services.connections import process_pending, decide
from content.services.publication import publish
from content.services.quiz import review_quiz
from content.services.sample_content import load_corpus, validate_corpus, verify_sample


def install_sample(password, *, superuser=False):
    corpus, hierarchy = load_corpus()
    validate_corpus(corpus, hierarchy)
    with transaction.atomic():
        editor = get_user_model().objects.create_user('sample-editor', password=password, is_staff=True, is_superuser=superuser)
        if not superuser:
            from django.contrib.auth.models import Permission
            editor.user_permissions.set(Permission.objects.filter(codename__startswith='view_'))
        # This checked-in hierarchy is identical to the original 142-topic tree.
        # No real database or learner record is read or copied by this command.
        for row in hierarchy:
            Topic.objects.create(**row)
        topics = Topic.objects.in_bulk()
        selected = {row['topic_id']: row for row in corpus['lessons']}
        published = set(selected)
        for pk in selected:
            node = topics[pk]
            while node.parent_id:
                published.add(node.parent_id)
                node = topics[node.parent_id]
        for lesson in corpus['lessons']:
            topic = topics[lesson['topic_id']]
            refs = [corpus['sources'][key] for key in lesson['sources']]
            reference = '\n'.join(f"{s['title']}: {s['url']}" for s in refs)
            tags = []
            for name in lesson['tags']:
                tag, _ = Tag.objects.get_or_create(normalized_name=normalized_label(name),
                                                   defaults={'name': name, 'is_public': True})
                tags.append(tag)
            topic.tags.set(tags)
            TopicAlias.objects.create(topic=topic, name=lesson['alias'], status='approved')
            from content.services.sample_content import article_html
            ContentBlock.objects.create(topic=topic, block_type='text', order=1,
                                        content=article_html(lesson, corpus), source_reference=reference)
            quiz = Quiz.objects.create(topic=topic, title=f"Sample practice · {topic.title}", time_limit_seconds=0)
            for item in lesson['questions']:
                question = Question.objects.create(quiz=quiz, primary_topic=topic,
                    question_text=item['question'], explanation=item['explanation'])
                question.tags.set(tags)
                for index, choice in enumerate(item['choices']):
                    Choice.objects.create(question=question, choice_text=choice,
                                          is_correct=index == item['answer'])
            review_quiz(quiz, editor, 'DEMO ONLY: source-checked engineering sample; '
                        'not human editorial approval for production.\n' + reference)
            for edge in lesson['connections']:
                relation = TopicRelation(source=topic, target=topics[edge['target_id']],
                                         kind='related', status='approved', reason=edge['reason'])
                relation.full_clean()
                relation.save()
        # Parents precede children in the canonical hierarchy. Publish only
        # selected lessons and their necessary ancestor navigation containers.
        for row in hierarchy:
            if row['id'] in published:
                publish(topics[row['id']], editor)
        process_pending(200)
        # Explicitly approve only the curated source/target/alias pairs. Other
        # automatically suggested matches retain their pending review state.
        for lesson in corpus['lessons']:
            for edge in lesson['connections']:
                target = selected[edge['target_id']]
                proposal = KeywordLinkProposal.objects.get(source_id=lesson['topic_id'],
                    target_id=edge['target_id'], phrase_key=normalized_label(target['alias']))
                decide(proposal, 'approved', editor)
        report = verify_sample(corpus, hierarchy)
    return report, editor
