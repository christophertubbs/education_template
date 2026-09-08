(() => {
    const storageKey = "__APP_NAME__-curriculum-progress-v1";
    const initialProgress = {
        schemaVersion: 1,
        completedLessons: [],
        assessmentAttempts: {},
        preferences: {timersEnabled: true}
    };

    function loadProgress() {
        const stored = window.localStorage.getItem(storageKey);
        if (!stored) {
            return structuredClone(initialProgress);
        }
        try {
            const parsed = JSON.parse(stored);
            if (parsed.schemaVersion !== 1) {
                return structuredClone(initialProgress);
            }
            return parsed;
        } catch {
            return structuredClone(initialProgress);
        }
    }

    function saveProgress(progress) {
        window.localStorage.setItem(storageKey, JSON.stringify(progress, null, 2));
        renderProgress();
    }

    function completeLesson(identifier) {
        const progress = loadProgress();
        if (!progress.completedLessons.includes(identifier)) {
            progress.completedLessons.push(identifier);
        }
        saveProgress(progress);
    }

    function showLessonCompletion(button) {
        const feedback = document.querySelector("[data-completion-feedback]");
        const nextAssessmentUrl = button.dataset.nextAssessmentUrl;
        if (feedback) {
            feedback.textContent = nextAssessmentUrl
                ? "Lesson complete. Starting the related repository check."
                : "Lesson complete.";
            feedback.classList.add("correct");
        }
        if (nextAssessmentUrl) {
            window.setTimeout(() => {
                window.location.assign(nextAssessmentUrl);
            }, 900);
        }
    }

    function gradeAssessment(section) {
        const questions = [...section.querySelectorAll("[data-question-id]")];
        let correctCount = 0;
        questions.forEach((question) => {
            const selected = question.querySelector("input:checked");
            const feedback = question.querySelector(".feedback");
            const isCorrect = selected && selected.value === question.dataset.correctIndex;
            if (isCorrect) {
                correctCount += 1;
                feedback.textContent = "Correct. " + question.dataset.feedback;
                feedback.classList.add("correct");
            } else {
                feedback.textContent = "Review this concept. " + question.dataset.feedback;
                feedback.classList.remove("correct");
            }
        });
        const score = questions.length ? correctCount / questions.length : 0;
        const progress = loadProgress();
        const identifier = section.dataset.assessmentId;
        progress.assessmentAttempts[identifier] = progress.assessmentAttempts[identifier] || [];
        progress.assessmentAttempts[identifier].push({
            score,
            correctCount,
            questionCount: questions.length,
            completedAt: new Date().toISOString()
        });
        saveProgress(progress);
        const scoreElement = section.querySelector("[data-assessment-score]");
        scoreElement.textContent = `Score: ${correctCount}/${questions.length} (${Math.round(score * 100)}%). Moving to the next lesson.`;
        if (section.dataset.nextUrl) {
            window.setTimeout(() => {
                window.location.assign(section.dataset.nextUrl);
            }, 1200);
        }
    }

    function renderProgress() {
        const progress = loadProgress();
        document.querySelectorAll("[data-progress-summary]").forEach((element) => {
            const attemptCount = Object.values(progress.assessmentAttempts)
                .reduce((total, attempts) => total + attempts.length, 0);
            element.innerHTML = `
                <strong>${progress.completedLessons.length}</strong> lessons completed<br>
                <strong>${attemptCount}</strong> assessment attempts saved
            `;
        });
        document.querySelectorAll("[data-progress-json]").forEach((element) => {
            element.textContent = JSON.stringify(progress, null, 2);
        });
    }

    function exportProgress() {
        const blob = new Blob([JSON.stringify(loadProgress(), null, 2)], {
            type: "application/json"
        });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "__APP_NAME__-curriculum-progress.json";
        link.click();
        URL.revokeObjectURL(link.href);
    }

    function importProgress(file) {
        file.text().then((text) => {
            const parsed = JSON.parse(text);
            if (parsed.schemaVersion !== 1) {
                throw new Error("Unsupported progress schema version.");
            }
            saveProgress(parsed);
        }).catch((error) => {
            window.alert(error.message);
        });
    }

    function startTimer(section) {
        const timer = section.querySelector("[data-assessment-timer]");
        const seconds = Number(section.dataset.timeLimit || 0);
        if (!timer || seconds <= 0 || !loadProgress().preferences.timersEnabled) {
            if (timer) {
                timer.textContent = "Timer disabled";
            }
            return;
        }
        const endsAt = Date.now() + seconds * 1000;
        window.setInterval(() => {
            const remaining = Math.max(0, Math.ceil((endsAt - Date.now()) / 1000));
            timer.textContent = `Time remaining: ${remaining}s`;
        }, 1000);
    }

    document.addEventListener("click", (event) => {
        const completeButton = event.target.closest("[data-complete-lesson]");
        if (completeButton) {
            completeLesson(completeButton.dataset.completeLesson);
            showLessonCompletion(completeButton);
        }
        if (event.target.closest("[data-grade-assessment]")) {
            gradeAssessment(event.target.closest("[data-assessment-id]"));
        }
        if (event.target.closest("[data-export-progress]")) {
            exportProgress();
        }
        if (event.target.closest("[data-reset-progress]")) {
            saveProgress(structuredClone(initialProgress));
        }
    });

    document.addEventListener("change", (event) => {
        if (event.target.matches("[data-import-progress]") && event.target.files[0]) {
            importProgress(event.target.files[0]);
        }
    });

    document.querySelectorAll("[data-assessment-id]").forEach(startTimer);
    renderProgress();
})();
