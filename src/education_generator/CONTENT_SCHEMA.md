# Curriculum Content JSON

The generator can reuse the Django host and curriculum-app scaffold for another
repository by adding this optional field to `project.json`:

```json
{
  "curriculum_content_path": "path/to/curriculum.json"
}
```

The content file must contain the same top-level structure packaged into the
generated app:

```json
{
  "course": {
    "identifier": "example-course",
    "title": "Example Repository Curriculum",
    "description": "Course description.",
    "passing_score": 0.8
  },
  "lessons": [
    {
      "identifier": "example-lesson",
      "sequence": "1",
      "title": "Example Lesson",
      "summary": "Short lesson summary.",
      "body": ["Longer lesson paragraph."],
      "sources": [
        {
          "file_path": "README.md",
          "start_line": 1,
          "end_line": 20,
          "url": "https://example.test/repository/blob/COMMIT/README.md"
        }
      ]
    }
  ],
  "glossary": [
    {
      "identifier": "example-term",
      "term": "Example Term",
      "definition": "Definition."
    }
  ],
  "assessments": [
    {
      "identifier": "quiz-example-lesson",
      "assessment_type": "section",
      "title": "Example Lesson Quiz",
      "lesson_identifiers": ["example-lesson"],
      "time_limit_seconds": 0,
      "question_count": 3,
      "passing_score": 0.8
    }
  ],
  "questions": [
    {
      "identifier": "q-example",
      "assessment_identifier": "quiz-example-lesson",
      "prompt": "Question prompt?",
      "answers": ["Correct answer.", "Plausible distractor.", "Plausible distractor.", "Plausible distractor."],
      "correct_index": 0,
      "feedback": "Explanation grounded in the target repository.",
      "lesson_identifier": "example-lesson"
    }
  ],
  "coverage": [
    {
      "concept": "Example concept",
      "lessons": ["example-lesson"],
      "assessments": ["quiz-example-lesson"]
    }
  ]
}
```

The generator replaces any supplied `metadata` object with current generation
metadata, including the resolved target repository commit. Keep section quizzes
one-to-one with lessons when using the current lesson-completion flow.
