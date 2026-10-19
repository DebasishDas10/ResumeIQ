
const API_URL = "https://resumeiq-api-debasish-hpg7acezd0haebbm.koreacentral-01.azurewebsites.net";

// ==========================
// ELEMENT REFERENCES
// ==========================

const resumeFile = document.getElementById("resumeFile");
const fileName = document.getElementById("fileName");
const jobDescription = document.getElementById("jobDescription");
const analyzeBtn = document.getElementById("analyzeBtn");
const statusMessage = document.getElementById("statusMessage");
const resultsSection = document.getElementById("resultsSection");

// Recommendations Elements
const recommendationsSection = document.getElementById(
    "recommendationsSection"
);
const recommendationsContainer = document.getElementById(
    "recommendationsContainer"
);

// Analysis History Elements
const loadHistoryBtn = document.getElementById("loadHistoryBtn");
const historyStatus = document.getElementById("historyStatus");
const historyContainer = document.getElementById("historyContainer");


// ==========================
// INPUT CHANGE EVENTS
// ==========================

resumeFile.addEventListener("change", () => {
    const file = resumeFile.files[0];

    fileName.textContent = file ? file.name : "No file selected";

    resultsSection.classList.add("hidden");
    recommendationsSection.classList.add("hidden");
});

jobDescription.addEventListener("input", () => {
    resultsSection.classList.add("hidden");
    recommendationsSection.classList.add("hidden");
});


// ==========================
// STATUS MESSAGES
// ==========================

function showStatus(message, type = "") {
    statusMessage.textContent = message;
    statusMessage.className = type;
}

function showHistoryStatus(message, type = "") {
    historyStatus.textContent = message;
    historyStatus.className = type;
}


// ==========================
// RENDER SKILL TAGS
// ==========================

function createSkillTag(skill, type) {
    const tag = document.createElement("span");
    tag.className = `skill-tag ${type}`;
    tag.textContent = skill;
    return tag;
}

function renderSkills(elementId, skills, type) {
    const container = document.getElementById(elementId);
    container.replaceChildren();

    if (!skills.length) {
        const emptyMessage = document.createElement("p");
        emptyMessage.textContent = "No skills to display.";
        container.appendChild(emptyMessage);
        return;
    }

    skills.forEach((skill) => {
        container.appendChild(createSkillTag(skill, type));
    });
}


// ==========================
// DISPLAY RECOMMENDATIONS
// ==========================

function displayRecommendations(recommendations) {

    // Clear previous recommendations
    recommendationsContainer.replaceChildren();

    // Hide the section if there are no recommendations
    if (!Array.isArray(recommendations) ||
        recommendations.length === 0) {

        recommendationsSection.classList.add("hidden");
        return;
    }

    // Create a recommendation card for each missing skill
    recommendations.forEach((item) => {

        const card = document.createElement("article");
        card.className = "recommendation-card";

        const heading = document.createElement("h3");
        heading.textContent = item.skill;

        const description = document.createElement("p");
        description.textContent = item.recommendation;

        card.appendChild(heading);
        card.appendChild(description);

        recommendationsContainer.appendChild(card);
    });

    // Show the recommendations section
    recommendationsSection.classList.remove("hidden");
}


// ==========================
// DISPLAY ANALYSIS RESULTS
// ==========================

function displayResults(data) {

    const score = Math.max(
        0,
        Math.min(100, Number(data.match_score) || 0)
    );

    document.getElementById("matchScore").textContent =
        `${score}%`;

    document.getElementById("matchedCount").textContent =
        data.total_matched_skills;

    document.getElementById("missingCount").textContent =
        data.missing_skills.length;

    document.getElementById("progressFill").style.width =
        `${score}%`;

    renderSkills(
        "matchedSkills",
        data.matched_skills,
        "matched"
    );

    renderSkills(
        "missingSkills",
        data.missing_skills,
        "missing"
    );

    // Display personalized skill recommendations
    displayRecommendations(data.recommendations);

    let feedback = "";

    if (score >= 80) {
        feedback =
            "Strong technical skill overlap with this job description.";
    } else if (score >= 50) {
        feedback =
            "Moderate skill overlap. Review the missing skills.";
    } else {
        feedback =
            "Low skill overlap. Consider developing the missing skills.";
    }

    document.getElementById("matchFeedback").textContent =
        feedback;

    resultsSection.classList.remove("hidden");

    resultsSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


// ==========================
// ANALYZE RESUME
// ==========================

analyzeBtn.addEventListener("click", async () => {

    const file = resumeFile.files[0];
    const jd = jobDescription.value.trim();

    resultsSection.classList.add("hidden");
    recommendationsSection.classList.add("hidden");

    if (!file) {
        showStatus("Please upload your resume.", "error");
        return;
    }

    if (
        file.type !== "application/pdf" &&
        !file.name.toLowerCase().endsWith(".pdf")
    ) {
        showStatus("Please select a PDF file.", "error");
        return;
    }

    if (file.size > 5 * 1024 * 1024) {
        showStatus(
            "Resume must be smaller than 5 MB.",
            "error"
        );
        return;
    }

    if (!jd) {
        showStatus(
            "Please enter a job description.",
            "error"
        );
        return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_description", jd);

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "Analyzing...";

    showStatus("Analyzing your resume. Please wait.");

    try {

        const response = await fetch(
            `${API_URL}/analyze-resume`,
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {

            let message = "Resume analysis failed.";

            if (typeof data.detail === "string") {
                message = data.detail;
            } else if (Array.isArray(data.detail)) {
                message = "Please check your inputs.";
            }

            throw new Error(message);
        }

        displayResults(data);

        showStatus(
            "Resume analysis completed and saved successfully!",
            "success"
        );

        // Previously loaded history may now be outdated
        if (!historyContainer.classList.contains("hidden")) {

            showHistoryStatus(
                "A new analysis was saved. Click View Analysis History to refresh."
            );
        }

    } catch (error) {

        showStatus(
            error instanceof TypeError
                ? "Cannot connect to the backend. Check that FastAPI is running."
                : error.message,
            "error"
        );

    } finally {

        analyzeBtn.disabled = false;
        analyzeBtn.textContent = "Analyze My Resume →";
    }
});


// ==========================
// FORMAT ANALYSIS DATE
// ==========================

function formatAnalysisDate(dateString) {

    if (!dateString) {
        return "Date unavailable";
    }

    const date = new Date(dateString);

    if (Number.isNaN(date.getTime())) {
        return "Date unavailable";
    }

    return date.toLocaleString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    });
}


// ==========================
// CREATE HISTORY SKILLS
// ==========================

function createHistorySkills(title, skills, type) {

    const section = document.createElement("div");
    section.className = "history-skills";

    const heading = document.createElement("h4");
    heading.textContent = title;

    const tagsContainer = document.createElement("div");
    tagsContainer.className = "skill-tags";

    if (skills.length === 0) {

        const emptyMessage = document.createElement("p");
        emptyMessage.textContent = "None";
        tagsContainer.appendChild(emptyMessage);

    } else {

        skills.forEach((skill) => {
            tagsContainer.appendChild(
                createSkillTag(skill, type)
            );
        });
    }

    section.appendChild(heading);
    section.appendChild(tagsContainer);

    return section;
}


// ==========================
// CREATE HISTORY CARD
// ==========================

function createHistoryCard(analysis) {

    const card = document.createElement("article");
    card.className = "history-card";

    const header = document.createElement("div");
    header.className = "history-card-header";

    const info = document.createElement("div");

    const title = document.createElement("h3");
    title.textContent =
        analysis.filename || "Unknown resume";

    const date = document.createElement("p");
    date.className = "history-date";

    date.textContent =
        `Analysis #${analysis.analysis_id} • ` +
        formatAnalysisDate(analysis.created_at);

    info.appendChild(title);
    info.appendChild(date);

    const score = document.createElement("span");
    score.className = "history-score";

    const scoreValue = Math.max(
        0,
        Math.min(100, Number(analysis.match_score) || 0)
    );

    score.textContent = `${scoreValue.toFixed(2)}%`;

    header.appendChild(info);
    header.appendChild(score);

    card.appendChild(header);

    const matchedSkills = Array.isArray(
        analysis.matched_skills
    )
        ? analysis.matched_skills
        : [];

    const missingSkills = Array.isArray(
        analysis.missing_skills
    )
        ? analysis.missing_skills
        : [];

    card.appendChild(
        createHistorySkills(
            "✓ Matched Skills",
            matchedSkills,
            "matched"
        )
    );

    card.appendChild(
        createHistorySkills(
            "Missing Skills",
            missingSkills,
            "missing"
        )
    );

    return card;
}


// ==========================
// DISPLAY ANALYSIS HISTORY
// ==========================

function displayHistory(history) {

    historyContainer.replaceChildren();

    if (history.length === 0) {

        const emptyMessage = document.createElement("p");

        emptyMessage.textContent =
            "No previous analyses found. Analyze a resume to get started.";

        historyContainer.appendChild(emptyMessage);

    } else {

        history.forEach((analysis) => {
            historyContainer.appendChild(
                createHistoryCard(analysis)
            );
        });
    }

    historyContainer.classList.remove("hidden");
}


// ==========================
// FETCH ANALYSIS HISTORY
// ==========================

loadHistoryBtn.addEventListener("click", async () => {

    loadHistoryBtn.disabled = true;
    loadHistoryBtn.textContent = "Loading History...";

    showHistoryStatus(
        "Fetching saved analyses from SQL Server..."
    );

    try {

        const response = await fetch(
            `${API_URL}/analysis-history`
        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                typeof data.detail === "string"
                    ? data.detail
                    : "Unable to load analysis history."
            );
        }

        if (!Array.isArray(data.history)) {

            throw new Error(
                "Unexpected history response from server."
            );
        }

        displayHistory(data.history);

        showHistoryStatus(
            `${data.history.length} saved analysis record(s) found.`
        );

    } catch (error) {

        historyContainer.classList.add("hidden");

        showHistoryStatus(
            error instanceof TypeError
                ? "Cannot connect to the backend. Check that FastAPI is running."
                : error.message,
            "error"
        );

    } finally {

        loadHistoryBtn.disabled = false;
        loadHistoryBtn.textContent = "View Analysis History";
    }
});
