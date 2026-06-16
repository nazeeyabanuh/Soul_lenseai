// ======================
// ANALYZE BUTTON
// ======================

const analyzeBtn =
document.getElementById("analyzeBtn");

analyzeBtn.addEventListener("click", async () => {

    const text =
    document.getElementById("textInput").value;

    if (!text) {

        alert("Please enter some text.");

        return;
    }

    document.getElementById("mind")
    .innerText = "Analyzing...";

    document.getElementById("heart")
    .innerText = "Analyzing...";

    document.getElementById("aiAnalysis")
    .innerText = "Analyzing...";

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/analyze",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                    "application/json"
                },
                body: JSON.stringify({
                    text: text
                })
            }
        );

        const data =
        await response.json();

        document.getElementById("mind")
        .innerText =
        `Emotion: ${data.emotion}`;

        document.getElementById("heart")
        .innerText =
        `Style: ${data.style}
        | Confidence:
        ${data.confidence}`;

        document.getElementById("aiAnalysis")
        .innerText =
        data.ai_analysis;

        document.getElementById("insight")
        .innerText =
        data.insight;

        // ======================
        // ORB COLOR CHANGE
        // ======================

        const orb =
        document.getElementById(
            "emotionOrb"
        );

        if (orb) {

            const emotion =
            data.emotion.toLowerCase();

            if (emotion === "joy") {

                orb.style.background =
                "radial-gradient(circle,#fde047,#facc15)";
            }

            else if (
                emotion === "sadness"
            ) {

                orb.style.background =
                "radial-gradient(circle,#60a5fa,#2563eb)";
            }

            else if (
                emotion === "anger"
            ) {

                orb.style.background =
                "radial-gradient(circle,#f87171,#dc2626)";
            }

            else if (
                emotion === "fear"
            ) {

                orb.style.background =
                "radial-gradient(circle,#c084fc,#7c3aed)";
            }

            else if (
                emotion === "love"
            ) {

                orb.style.background =
                "radial-gradient(circle,#f9a8d4,#ec4899)";
            }
        }

    }

    catch (error) {

        console.error(error);

        document.getElementById(
            "aiAnalysis"
        ).innerText =
        "Backend connection failed.";
    }

});


// ======================
// HISTORY BUTTON
// ======================

document.getElementById("historyBtn")
.addEventListener("click", async () => {

    try {

        const response =
        await fetch(
            "http://127.0.0.1:8000/history"
        );

        const data =
        await response.json();

        const container =
        document.getElementById(
            "historyContainer"
        );

        container.innerHTML = "";

        data.forEach(item => {

            container.innerHTML += `

            <div class="history-card">

                <h3>${item.text}</h3>

                <p>
                    Emotion:
                    ${item.emotion}
                </p>

                <p>
                    Sentiment:
                    ${item.sentiment}
                </p>

                <p>
                    Manipulation:
                    ${item.manipulation_type}
                </p>

            </div>
            `;
        });

    }

    catch (error) {

        console.error(error);

        document.getElementById(
            "historyContainer"
        ).innerHTML =
        "<p>Failed to load history.</p>";
    }

});


// ======================
// DASHBOARD BUTTON
// ======================

document.getElementById("dashboardBtn")
.addEventListener("click", async () => {

    try {

        const response =
        await fetch(
            "http://127.0.0.1:8000/dashboard"
        );

        const data =
        await response.json();

        document.getElementById(
            "dashboardContainer"
        ).innerHTML = `

        <div class="dashboard-card">

            <h2>
                📊 SoulLens Analytics
            </h2>

            <div class="stat-grid">

                <div class="stat-box">
                    <h3>
                        ${data.total_analyses}
                    </h3>
                    <p>
                        Total Analyses
                    </p>
                </div>

                <div class="stat-box">
                    <h3>
                        ${data.most_common_emotion}
                    </h3>
                    <p>
                        Top Emotion
                    </p>
                </div>

                <div class="stat-box">
                    <h3>
                        ${data.positive_messages}
                    </h3>
                    <p>
                        Positive
                    </p>
                </div>

                <div class="stat-box">
                    <h3>
                        ${data.negative_messages}
                    </h3>
                    <p>
                        Negative
                    </p>
                </div>

                <div class="stat-box">
                    <h3>
                        ${data.manipulation_cases}
                    </h3>
                    <p>
                        Manipulation Cases
                    </p>
                </div>

            </div>

        </div>
        `;

    }

    catch (error) {

        console.error(error);

        document.getElementById(
            "dashboardContainer"
        ).innerHTML =
        "<p>Failed to load dashboard.</p>";
    }

});
document.getElementById("chartBtn")
.addEventListener("click", () => {

    document.getElementById(
        "chartContainer"
    ).innerHTML = `

    <img
        src="http://127.0.0.1:8000/emotion-chart?t=${Date.now()}"
        style="
            width:100%;
            max-width:900px;
            border-radius:20px;
            margin-top:20px;
        "
    >

    `;
});
// ======================
// DASHBOARD BUTTON
// ======================

document
.getElementById("dashboardBtn")
.addEventListener(
    "click",
    async () => {

        const response =
        await fetch(
            "http://127.0.0.1:8000/dashboard"
        );

        const data =
        await response.json();

        document
        .getElementById(
            "dashboardContainer"
        )
        .innerHTML = `

        <div class="dashboard-card">

            <h2>
                📊 SoulLens Analytics
            </h2>

            <div class="stat-grid">

                <div class="stat-box">
                    <h3>
                    ${data.total_analyses}
                    </h3>
                    <p>
                    Total Analyses
                    </p>
                </div>

                <div class="stat-box">
                    <h3>
                    ${data.most_common_emotion}
                    </h3>
                    <p>
                    Top Emotion
                    </p>
                </div>

                <div class="stat-box">
                    <h3>
                    ${data.positive_messages}
                    </h3>
                    <p>
                    Positive
                    </p>
                </div>

                <div class="stat-box">
                    <h3>
                    ${data.negative_messages}
                    </h3>
                    <p>
                    Negative
                    </p>
                </div>

                <div class="stat-box">
                    <h3>
                    ${data.manipulation_cases}
                    </h3>
                    <p>
                    Manipulation Cases
                    </p>
                </div>

            </div>

        </div>
        `;
    }
);
// ======================
// CHART BUTTON
// ======================

document
.getElementById("chartBtn")
.addEventListener(
    "click",
    () => {

        document
        .getElementById(
            "chartContainer"
        )
        .innerHTML = `

        <div class="chart-card">

            <h2>
                📊 Emotion Distribution
            </h2>

            <img
                src="http://127.0.0.1:8000/emotion-chart?t=${Date.now()}"
            >

        </div>
        `;
    }
);

document.getElementById("relationshipBtn")
.addEventListener("click", async () => {

    const personA =
    document.getElementById("personA").value;

    const personB =
    document.getElementById("personB").value;

    const response = await fetch(
        "http://127.0.0.1:8000/relationship",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                person_a: personA,
                person_b: personB
            })
        }
    );

    const data = await response.json();

    document.getElementById(
        "relationshipResult"
    ).innerText = data.analysis;
});

const button =
document.getElementById("analyzeBtn");

button.addEventListener(
    "click",
    async () => {

        const text =
        document.getElementById(
            "textInput"
        ).value;

        document.getElementById(
            "aiAnalysis"
        ).innerText =
        "Analyzing...";

        const response =
        await fetch(
            "http://127.0.0.1:8000/analyze",
            {
                method:"POST",

                headers:{
                    "Content-Type":
                    "application/json"
                },

                body:JSON.stringify({
                    text:text
                })
            }
        );

        const data =
        await response.json();

        document.getElementById(
            "mind"
        ).innerText =
        "Emotion: " +
        data.emotion;

        document.getElementById(
            "heart"
        ).innerText =
        "Need: " +
        data.emotional_need;

        document.getElementById(
            "aiAnalysis"
        ).innerText =
        data.ai_analysis;

        document.getElementById(
            "insight"
        ).innerText =
        data.insight;
    }
);
document
.getElementById("timelineBtn")
.addEventListener(
    "click",
    async () => {

        const response =
        await fetch(
            "http://127.0.0.1:8000/timeline"
        );

        const data =
        await response.json();

        const container =
        document.getElementById(
            "timelineContainer"
        );

        container.innerHTML = "";

        data.forEach(item => {

            container.innerHTML += `
            <div class="timeline-card">

                <h3>
                ${item.emotion}
                </h3>

                <p>
                ${item.text}
                </p>

                <small>
                Analysis #${item.id}
                </small>

            </div>
            `;
        });

    }
);