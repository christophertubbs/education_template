# Curriculum Content JSON

The generator reuses the Django host and curriculum-app scaffold for each
repository by loading curriculum from a data path in `project.json`:

```json
{
  "curriculum_content_path": "path/to/curriculum.json"
}
```

When the field is omitted, the generator uses the conventional path
`curricula/<repository-name>/curriculum.json`.

The path is relative to `project.json`. A caller may upload a different data
file for one generation run without changing project configuration:

```bash
python -m education_generator --curriculum-content /path/to/curriculum.json
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
metadata, including the resolved target repository commit. The Python generator
contains no fallback lessons, glossary entries, assessments, or questions. Keep
section quizzes one-to-one with lessons when using the current lesson-completion
flow.
