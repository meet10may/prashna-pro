"""
OCR module using OpenAI GPT-4o Vision API.
Handles image-to-text extraction and structuring.
"""

import openai
import base64
import json
import re
import os


def encode_image_to_base64(image_path: str) -> str:
    """Read an image file and return its base64 encoding."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_mime_type(image_path: str) -> str:
    """Get MIME type from file extension."""
    ext = os.path.splitext(image_path)[1].lower()
    return {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }.get(ext, "image/jpeg")


def extract_text_from_images(image_paths: list, api_key: str, model: str = "gpt-4o") -> str:
    """
    Send all images to OpenAI GPT-4o Vision in a single request.
    Returns raw extracted text.
    """
    client = openai.OpenAI(api_key=api_key)

    # Build content array: prompt + all images
    content = [
        {
            "type": "text",
            "text": """You are an expert OCR system specialized in reading handwritten exam/question papers.

You are given images of a handwritten question paper (pages in order). Extract ALL text EXACTLY as written.

Rules:
- Preserve ALL question numbering (Q1, Q2, 1., 2., etc.)
- Preserve ALL subparts (a), (b), (c), (i), (ii), etc.
- Preserve ALL marks in brackets like (5), [10], (2 marks), etc.
- Preserve section headings (Section A, Section B, Part I, Part II, etc.)
- Preserve any instructions, time duration, total marks mentioned
- Maintain the ORIGINAL language exactly (English, Hindi, or mixed)
- For Hindi/Devanagari text, transcribe it accurately in Devanagari script
- If a question contains a DIAGRAM, GRAPH, FIGURE, MAP, or IMAGE, add [DIAGRAM: brief description] at that location
  For example: [DIAGRAM: Triangle ABC with angle B = 90 degrees] or [DIAGRAM: Bar graph showing population data]
- Do NOT summarize or paraphrase anything
- Do NOT skip any text, even if partially legible (mark unclear parts with [unclear])
- Do NOT add any commentary or explanation
- Clearly mark page boundaries as --- Page 1 ---, --- Page 2 ---, etc.

Return ONLY the raw extracted text, nothing else."""
        }
    ]

    for i, path in enumerate(image_paths):
        b64 = encode_image_to_base64(path)
        mime = get_mime_type(path)
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:{mime};base64,{b64}",
                "detail": "high"
            }
        })

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": content}],
        max_tokens=4096,
    )

    return response.choices[0].message.content.strip()


def structure_extracted_text(raw_text: str, api_key: str, model: str = "gpt-4o") -> dict:
    """
    Send combined raw text to OpenAI for cleaning and structuring into JSON.
    """
    client = openai.OpenAI(api_key=api_key)

    prompt = f"""You are an exam paper formatting assistant. You will receive raw OCR text from a handwritten question paper.

Your job is to:
1. Clean the text while PRESERVING the exact meaning of every question
2. Fix minor OCR errors and grammar issues WITHOUT changing question content
3. Standardize numbering format (Q1., Q2., or 1., 2., etc.)
4. Standardize subpart format: (a), (b), (c) or (i), (ii), (iii)
5. Standardize marks format: [marks] at end of each question
6. Detect and organize sections, instructions, and metadata

Return STRICTLY valid JSON with this exact structure (no markdown, no backticks, no explanation):

{{
  "exam_title": "extracted exam title or empty string",
  "class": "class/grade or empty string",
  "subject": "subject name or empty string",
  "time": "time duration or empty string",
  "total_marks": "total marks or empty string",
  "instructions": ["instruction 1", "instruction 2"],
  "sections": [
    {{
      "section_name": "Section A or similar",
      "questions": [
        {{
          "number": "1",
          "text": "Full question text",
          "marks": "5",
          "subparts": [
            "(a) subpart text",
            "(b) subpart text"
          ]
        }}
      ]
    }}
  ]
}}

IMPORTANT RULES:
- If there are no clear sections, put all questions in a single section named "Questions"
- If marks are not mentioned for a question, use an empty string for marks
- If metadata (class, subject, time, etc.) is not found, use empty strings
- Keep Hindi/Devanagari text as-is in the JSON
- Every question MUST be included - do not skip any
- Subparts should include their labels like "(a)", "(i)", etc.

Here is the raw OCR text:

{raw_text}

Return ONLY the JSON object:"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096,
        temperature=0.1,
    )

    response_text = response.choices[0].message.content.strip()

    # Clean markdown code fences if present
    response_text = re.sub(r'^```json\s*', '', response_text)
    response_text = re.sub(r'^```\s*', '', response_text)
    response_text = re.sub(r'\s*```$', '', response_text)
    response_text = response_text.strip()

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        # Retry: ask the model to fix the JSON
        retry_response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": f"The following text is supposed to be valid JSON but has errors. Fix it and return ONLY valid JSON, nothing else:\n\n{response_text}"}
            ],
            max_tokens=4096,
            temperature=0,
        )
        retry_text = retry_response.choices[0].message.content.strip()
        retry_text = re.sub(r'^```json\s*', '', retry_text)
        retry_text = re.sub(r'^```\s*', '', retry_text)
        retry_text = re.sub(r'\s*```$', '', retry_text)
        return json.loads(retry_text)


def process_images_to_structured(image_paths: list, api_key: str, model_name: str = "gpt-4o") -> dict:
    """
    Full pipeline: images -> OCR -> structure -> JSON
    Returns (structured_dict, raw_text)
    """
    # Step 1: Extract text from all images in one call
    raw_text = extract_text_from_images(image_paths, api_key, model=model_name)

    # Step 2: Structure the extracted text
    structured = structure_extracted_text(raw_text, api_key, model=model_name)

    return structured, raw_text
