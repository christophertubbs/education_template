(() => {
    "use strict";
    const SCHEMA_VERSION = 1;
    const databaseName = "education-runtime-progress";
    const curriculumId = document.body.dataset.curriculumId;
    const curriculumVersion = document.body.dataset.curriculumVersion;
    if (!curriculumId) return;

    function openDatabase() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(databaseName, SCHEMA_VERSION);
            request.onupgradeneeded = () => {
                if (!request.result.objectStoreNames.contains("curricula")) {
                    request.result.createObjectStore("curricula", { keyPath: "curriculumId" });
                }
            };
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    async function readProgress() {
        const database = await openDatabase();
        return new Promise((resolve, reject) => {
            const request = database.transaction("curricula").objectStore("curricula").get(curriculumId);
            request.onsuccess = () => resolve(request.result || freshProgress());
            request.onerror = () => reject(request.error);
        });
    }

    function freshProgress() {
        return { schemaVersion: SCHEMA_VERSION, curriculumId, curriculumVersion, completedLessons: [], attempts: {}, missedConcepts: [], navigationSincePop: 0, preferences: { timerMode: "default" } };
    }

    async function writeProgress(progress) {
        if (progress.schemaVersion !== SCHEMA_VERSION || progress.curriculumId !== curriculumId) {
            throw new Error("Progress file is incompatible with this curriculum or runtime schema.");
        }
        if (progress.curriculumVersion !== curriculumVersion) {
            throw new Error("Progress was exported for a different curriculum version; keep the file until a compatible migration is available.");
        }
        const database = await openDatabase();
        return new Promise((resolve, reject) => {
            const request = database.transaction("curricula", "readwrite").objectStore("curricula").put(progress);
            request.onsuccess = () => resolve();
            request.onerror = () => reject(request.error);
        });
    }

    async function completeLesson() {
        const lessonId = document.querySelector("[data-lesson-id]")?.dataset.lessonId;
        if (!lessonId) return;
        const progress = await readProgress();
        if (!progress.completedLessons.includes(lessonId)) progress.completedLessons.push(lessonId);
        await writeProgress(progress);
        document.querySelector("[data-completion-status]").textContent = "Lesson completion saved on this device.";
    }

    async function renderSummary() {
        const target = document.querySelector("[data-progress-summary]");
        if (!target) return;
        const progress = await readProgress();
        target.textContent = `${progress.completedLessons.length} lessons completed; ${Object.keys(progress.attempts).length} assessments attempted.`;
    }

    async function exportProgress() {
        const progress = await readProgress();
        const blob = new Blob([JSON.stringify(progress, null, 2)], { type: "application/json" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = `${curriculumId}-progress.json`;
        link.click();
        URL.revokeObjectURL(link.href);
    }

    async function importProgress(event) {
        const file = event.target.files[0];
        if (!file) return;
        const incoming = JSON.parse(await file.text());
        await writeProgress(incoming);
        await renderSummary();
        document.querySelector("[data-progress-status]").textContent = "Progress imported.";
    }

    async function resetProgress() {
        if (!window.confirm("Reset progress for this curriculum on this device?")) return;
        await writeProgress(freshProgress());
        await renderSummary();
        document.querySelector("[data-progress-status]").textContent = "Progress reset.";
    }

    window.educationProgress = { readProgress, writeProgress };
    document.querySelectorAll("[data-learning-navigation]").forEach((link) => {
        link.addEventListener("click", async (event) => {
            const progress = await readProgress();
            progress.navigationSincePop = (progress.navigationSincePop || 0) + 1;
            const probability = Number(document.body.dataset.popProbability || 0);
            const cooldown = Number(document.body.dataset.popCooldown || 3);
            const popUrl = document.body.dataset.popUrl;
            const canReview = progress.completedLessons.length > 0;
            const shouldPop = canReview && popUrl && progress.navigationSincePop > cooldown && Math.random() < probability;
            if (shouldPop) {
                event.preventDefault();
                progress.navigationSincePop = 0;
                await writeProgress(progress);
                const separator = popUrl.includes("?") ? "&" : "?";
                window.location.assign(`${popUrl}${separator}lessons=${encodeURIComponent(progress.completedLessons.join(","))}`);
            } else {
                await writeProgress(progress);
            }
        });
    });
    document.querySelector("[data-complete-lesson]")?.addEventListener("click", () => completeLesson().catch(console.error));
    document.querySelector("[data-export-progress]")?.addEventListener("click", () => exportProgress().catch(console.error));
    document.querySelector("[data-import-progress]")?.addEventListener("change", (event) => importProgress(event).catch((error) => { document.querySelector("[data-progress-status]").textContent = error.message; }));
    document.querySelector("[data-reset-progress]")?.addEventListener("click", () => resetProgress().catch(console.error));
    renderSummary().catch(console.error);
})();
