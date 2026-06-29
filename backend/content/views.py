from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Topic
from .serializers import ChildTopicSerializer,TopicDetailSerializer
from django.shortcuts import get_object_or_404
from .ai_engine import generate_mentor_response

@api_view(["GET"])
def topic_root_list(request):
    topics = Topic.objects.filter(parent__isnull=True).order_by("order")
    serializer = ChildTopicSerializer(topics, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def topic_detail(request,slug):
    topic = get_object_or_404(Topic,slug=slug)
    serializer = TopicDetailSerializer(topic)
    return Response(serializer.data)


@api_view(["POST"])
def topic_chat(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    message = request.data.get("message", "")
    preset = request.data.get("preset", None)
    
    if not message and not preset:
        return Response({"error": "Either message or preset field is required."}, status=400)
        
    ai_response = generate_mentor_response(topic, message, preset=preset)
    return Response({"response": ai_response})


from .models import Quiz, Question, Choice, QuizAttempt
from .serializers import QuizSerializer
from .ai_engine import generate_quiz_questions

@api_view(["GET"])
def topic_quiz(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    
    # Check if a quiz already exists
    quiz = Quiz.objects.filter(topic=topic).first()
    
    if not quiz:
        # Generate dynamic quiz questions via AI
        questions_data = generate_quiz_questions(topic)
        
        if questions_data:
            # Create a new quiz
            quiz = Quiz.objects.create(
                topic=topic,
                title=f"AI Practice Challenge: {topic.title}",
                time_limit_seconds=180
            )
            for q_data in questions_data:
                question = Question.objects.create(
                    quiz=quiz,
                    question_text=q_data.get("question_text", "Sample Question"),
                    explanation=q_data.get("explanation", "")
                )
                for c_data in q_data.get("choices", []):
                    Choice.objects.create(
                        question=question,
                        choice_text=c_data.get("text", "Choice text"),
                        is_correct=c_data.get("is_correct", False)
                    )
        else:
            # Create a standard fallback quiz if AI fails or no API Key
            quiz = Quiz.objects.create(
                topic=topic,
                title=f"Syllabus Test: {topic.title}",
                time_limit_seconds=300
            )
            question = Question.objects.create(
                quiz=quiz,
                question_text=f"Which core aspect of '{topic.title}' is key to RPSC preparation?",
                explanation="Factual accuracy on historical events, geographic formations, and administrative rulings is critical for RPSC."
            )
            Choice.objects.create(question=question, choice_text="Factual historical dates and lineages", is_correct=True)
            Choice.objects.create(question=question, choice_text="General theoretical guesses", is_correct=False)
            Choice.objects.create(question=question, choice_text="Unrelated global developments", is_correct=False)
            Choice.objects.create(question=question, choice_text="None of the above", is_correct=False)
            
    serializer = QuizSerializer(quiz)
    return Response(serializer.data)


@api_view(["POST"])
def topic_quiz_submit(request, slug):
    quiz = get_object_or_404(Quiz, topic__slug=slug)
    user_answers = request.data.get("answers", {})
    
    score = 0
    total_questions = quiz.questions.count()
    results = []
    incorrect_list = []
    
    for question in quiz.questions.all():
        correct_choice = question.choices.filter(is_correct=True).first()
        correct_choice_id = correct_choice.id if correct_choice else None
        
        user_choice_id = user_answers.get(str(question.id))
        is_correct = False
        
        if user_choice_id is not None:
            user_choice_id = int(user_choice_id)
            if user_choice_id == correct_choice_id:
                is_correct = True
                score += 1
                
        if not is_correct:
            incorrect_list.append(question)
            
        results.append({
            "question_id": question.id,
            "question_text": question.question_text,
            "user_answer": user_choice_id,
            "correct_answer": correct_choice_id,
            "is_correct": is_correct,
            "explanation": question.explanation
        })
        
    # Save the attempt to db
    attempt = QuizAttempt.objects.create(
        quiz=quiz,
        score=score,
        total_questions=total_questions
    )
    if incorrect_list:
        attempt.incorrect_questions.add(*incorrect_list)
        
    percentage = (score / total_questions * 100) if total_questions > 0 else 0
    
    return Response({
        "score": score,
        "total": total_questions,
        "percentage": percentage,
        "results": results
    })


from .models import Bookmark, UserProgress
from .ai_engine import generate_weakness_report

@api_view(["POST"])
def topic_bookmark(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    bookmark = Bookmark.objects.filter(topic=topic).first()
    
    if bookmark:
        bookmark.delete()
        is_bookmarked = False
    else:
        Bookmark.objects.create(topic=topic)
        is_bookmarked = True
        
    return Response({"bookmarked": is_bookmarked})


@api_view(["POST"])
def topic_progress(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    progress = UserProgress.objects.filter(topic=topic).first()
    
    if progress:
        progress.is_completed = not progress.is_completed
        progress.save()
        is_completed = progress.is_completed
    else:
        UserProgress.objects.create(topic=topic, is_completed=True)
        is_completed = True
        
    return Response({"is_completed": is_completed})


@api_view(["GET"])
def profile_weaknesses(request):
    attempts = QuizAttempt.objects.all().order_by("-attempted_at")[:10]
    errors_list = []
    
    for att in attempts:
        for question in att.incorrect_questions.all():
            errors_list.append(f"Chapter: {question.quiz.topic.title} - Question: {question.question_text}")
            
    if not errors_list:
        report = "Great work! You haven't answered any quiz questions incorrectly yet. Keep up the high standard!"
    else:
        report = generate_weakness_report(errors_list)
        
    return Response({"report": report})