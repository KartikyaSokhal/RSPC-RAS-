import os
import json
import dotenv
from google import genai
from google.genai import types

def load_env_fresh():
    """
    Ensures environment variables are loaded fresh from .env on every request.
    This avoids caching issues with Django's development reloader.
    """
    # Find .env path relative to this file
    env_path = os.path.join(os.path.dirname(__file__), "../.env")
    dotenv.load_dotenv(env_path, override=True)


def get_topic_context(topic):
    """
    Concatenates hierarchical details and text content blocks of a topic 
    to form the context payload for RAG.
    """
    context_parts = []
    
    # 1. Collect Hierarchy
    hierarchy = []
    curr = topic
    while curr.parent:
        hierarchy.append(curr.parent.title)
        curr = curr.parent
    if hierarchy:
        context_parts.append(f"Subject Area Hierarchy: {' > '.join(reversed(hierarchy))}")
        
    context_parts.append(f"Chapter Title: {topic.title}")
    
    # 2. Gather Direct Content Blocks
    blocks = topic.blocks.filter(block_type__in=["text", "heading"]).order_by("order")
    direct_content = []
    for b in blocks:
        if b.block_type == "heading":
            direct_content.append(f"\n### {b.content}")
        else:
            direct_content.append(b.content)
            
    if direct_content:
        context_parts.append("Reading Notes:\n" + "\n".join(direct_content))
    else:
        # 3. Gather Content from Subtopics recursively (1 level deep) if parent is empty
        child_contents = []
        for child in topic.children.all().order_by("order"):
            child_blocks = child.blocks.filter(block_type__in=["text", "heading"]).order_by("order")
            child_text = []
            for cb in child_blocks:
                if cb.block_type == "heading":
                    child_text.append(f"#### {cb.content}")
                else:
                    child_text.append(cb.content)
            if child_text:
                child_contents.append(f"Subtopic notes for [{child.title}]:\n" + "\n".join(child_text))
        
        if child_contents:
            context_parts.append("Detailed Subtopic Content:\n\n" + "\n\n".join(child_contents))
        else:
            context_parts.append("No active notes or subtopics have been defined for this chapter yet.")
            
    return "\n\n".join(context_parts)


def generate_mentor_response(topic, message, preset=None):
    """
    Triggers Gemini API model request using RAG prompt templates.
    """
    load_env_fresh()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "System Error: GEMINI_API_KEY is not set in the environment variables (.env)."
        
    try:
        client = genai.Client(api_key=api_key)
        context = get_topic_context(topic)
        
        # Action button preset prompts
        preset_prompts = {
            "explain_beginner": "Explain the concepts in the notes as if speaking to an absolute beginner. Use simple analogies and layman's terms. Keep it engaging and simple.",
            "pyq_analysis": "Perform a Previous Year Question (PYQ) trend analysis on this topic. Highlight which aspects are frequently tested in RPSC RAS (Prelims & Mains), typical question styles, and high-yield areas.",
            "revision": "Provide a quick 5-minute revision summary of this topic. Structure it as concise bullet points, highlighting core facts, dates, and historical/geographical details.",
            "mnemonics": "Design creative memory tricks or mnemonics (mixing Hindi/English is encouraged) to help memorize complex names, lists, dynasties, or dates present in the chapter content.",
            "generate_mcqs": "Draft exactly 3 high-quality multiple choice questions (MCQs) matching RPSC RAS standards from this topic. Include options A-D. At the bottom, provide the correct answers and a brief explanation for each.",
            "examiner_mode": "Act as an examiner. Ask me one challenging question based on these notes. Wait for my response before asking any more questions.",
            "exam_importance": "Rate the RPSC exam importance of this chapter as High, Medium, or Low. Explain your reasoning in 2-3 concise sentences.",
            "common_mistakes": "Highlight the top 3 common mistakes or conceptual confusions students make when studying this topic.",
            "next_topics": "Suggest the next logical topics/chapters in the RPSC syllabus the student should study next after this one, explaining the study path flow."
        }
        
        system_instruction = (
            "You are Prepal AI, an expert mentor and personal tutor for the Rajasthan State Public Service Commission (RPSC) RAS exam.\n"
            "Your objective is to guide the student through the syllabus material.\n"
            "CRITICAL: Always align your answers with the syllabus facts provided in the Context below. If general knowledge is needed, state that clearly but keep it context-aligned.\n"
            "Format all your responses using clean Markdown. Use headings, bullet lists, and tables where appropriate to make it visually premium.\n\n"
            f"Syllabus Context for chapter '{topic.title}':\n"
            f"{context}"
        )
        
        user_prompt = ""
        if preset and preset in preset_prompts:
            user_prompt = f"[System Preset Trigger: {preset.upper()}]\nInstruction: {preset_prompts[preset]}"
            if message:
                user_prompt += f"\nStudent Follow-up Input: {message}"
        else:
            user_prompt = message
            
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7
            )
        )
        return response.text
    except Exception as e:
        return f"AI Service Error: Failed to generate response from Gemini. Details: {str(e)}"


def generate_quiz_questions(topic):
    """
    Generates RPSC-style MCQs dynamically using Gemini based on chapter notes.
    """
    load_env_fresh()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
        
    try:
        client = genai.Client(api_key=api_key)
        context = get_topic_context(topic)
        
        prompt = (
            f"Generate exactly 3 RPSC RAS standard multiple-choice questions (MCQs) for the topic '{topic.title}'.\n"
            f"Use the syllabus notes below as context.\n"
            f"For each question, provide 4 choices, specify which choice is correct, and write a brief explanation.\n"
            f"You MUST return the output in a strict JSON format matching this schema:\n"
            "{\n"
            '  "questions": [\n'
            "    {\n"
            '      "question_text": "Question content here...",\n'
            '      "explanation": "Why this is correct...",\n'
            '      "choices": [\n'
            '        {"text": "Option A", "is_correct": false},\n'
            '        {"text": "Option B", "is_correct": true},\n'
            '        {"text": "Option C", "is_correct": false},\n'
            '        {"text": "Option D", "is_correct": false}\n'
            "      ]\n"
            "    }\n"
            "  ]\n"
            "}\n\n"
            f"Syllabus Context:\n{context}"
        )
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2
            )
        )
        
        data = json.loads(response.text)
        return data.get("questions", [])
    except Exception as e:
        print("Failed to generate quiz questions via AI:", e)
        return None


def generate_weakness_report(errors_list):
    """
    Analyzes student's incorrect quiz answers and generates a personalized RPSC revision plan.
    """
    load_env_fresh()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Please configure your GEMINI_API_KEY to retrieve AI analysis of your study weaknesses."
        
    try:
        client = genai.Client(api_key=api_key)
        errors_str = "\n".join(errors_list)
        
        prompt = (
            "Analyze the following list of practice questions that a student answered incorrectly during RPSC RAS preparation. "
            "Identify the main conceptual weaknesses, outline common pitfalls, and generate a personalized study plan.\n"
            "Keep the report structured, encouraging, and clear using bullet points.\n\n"
            f"List of Student Mistakes:\n{errors_str}"
        )
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"AI Weakness Profiling Error: {str(e)}"
