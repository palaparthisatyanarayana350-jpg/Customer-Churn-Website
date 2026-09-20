const form = document.getElementById("predictionForm");

const resultCard = document.getElementById("resultCard");
const resultText = document.getElementById("resultText");
const resultDescription = document.getElementById("resultDescription");
const probability = document.getElementById("probability");
const riskBadge = document.getElementById("riskBadge");
const reasonList = document.getElementById("reasonList");
const riskMeterFill = document.getElementById("riskMeterFill");


// ========================================
// RISK STATE
// ========================================

function setRiskState(level) {

    // Remove previous risk classes
    resultCard.classList.remove(
        "risk-low",
        "risk-medium",
        "risk-high",
        "risk-error",
        "risk-analyzing"
    );

    riskBadge.classList.remove(
        "badge-low",
        "badge-medium",
        "badge-high",
        "badge-error",
        "badge-analyzing"
    );

    if (level === "low") {

        resultCard.classList.add("risk-low");
        riskBadge.classList.add("badge-low");

    } else if (level === "medium") {

        resultCard.classList.add("risk-medium");
        riskBadge.classList.add("badge-medium");

    } else if (level === "high") {

        resultCard.classList.add("risk-high");
        riskBadge.classList.add("badge-high");

    } else if (level === "error") {

        resultCard.classList.add("risk-error");
        riskBadge.classList.add("badge-error");

    } else {

        resultCard.classList.add("risk-analyzing");
        riskBadge.classList.add("badge-analyzing");
    }
}


// ========================================
// LOADING STATE
// ========================================

function showLoadingState() {

    setRiskState("analyzing");

    resultText.textContent = "Analyzing customer...";
    riskBadge.textContent = "ANALYZING";

    probability.textContent = "--%";

    riskMeterFill.style.width = "0%";

    reasonList.innerHTML =
        "<li>TabPFN is analyzing the customer profile...</li>";
}


// ========================================
// FORM SUBMISSION
// ========================================

form.addEventListener("submit", async function (event) {

    event.preventDefault();


    // ====================================
    // GET CUSTOMER INPUTS
    // ====================================

    const tenure = Number(
        document.getElementById("tenure").value
    );

    const monthlyCharges = Number(
        document.getElementById("monthlyCharges").value
    );

    const contract =
        document.getElementById("contract").value;

    const internet =
        document.getElementById("internet").value;

    const payment =
        document.getElementById("payment").value;

    const support =
        document.getElementById("support").value;


    // ====================================
    // SHOW LOADING STATE
    // ====================================

    showLoadingState();


    // ====================================
    // SEND REQUEST TO FLASK
    // ====================================

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    tenure: tenure,

                    monthlyCharges:
                        monthlyCharges,

                    contract: contract,

                    internet: internet,

                    payment: payment,

                    support: support
                })
            }
        );


        // ====================================
        // CHECK BACKEND RESPONSE
        // ====================================

        if (!response.ok) {
            throw new Error(
                "Prediction request failed."
            );
        }


        // ====================================
        // READ TABPFN RESULT
        // ====================================

        const data = await response.json();

        const churnProbability =
            Number(data.probability);


        // ====================================
        // DISPLAY PROBABILITY
        // ====================================

        probability.textContent =
            churnProbability.toFixed(2) + "%";


        // Smooth risk meter animation
        riskMeterFill.style.width =
            "0%";

        setTimeout(function () {

            riskMeterFill.style.width =
                churnProbability + "%";

        }, 100);


        // ====================================
        // DISPLAY RISK CATEGORY
        // ====================================

        if (churnProbability >= 60) {

            setRiskState("high");

            resultText.textContent =
                "High Churn Risk";

            riskBadge.textContent =
                "HIGH RISK";

            resultDescription.textContent =
                "The TabPFN model estimates a relatively high probability of customer churn based on the provided profile.";

        }

        else if (churnProbability >= 35) {

            setRiskState("medium");

            resultText.textContent =
                "Medium Churn Risk";

            riskBadge.textContent =
                "MEDIUM RISK";

            resultDescription.textContent =
                "The TabPFN model estimates a moderate probability of customer churn based on the provided profile.";

        }

        else {

            setRiskState("low");

            resultText.textContent =
                "Low Churn Risk";

            riskBadge.textContent =
                "LOW RISK";

            resultDescription.textContent =
                "The TabPFN model estimates a relatively low probability of customer churn based on the provided profile.";
        }


        // ====================================
        // WHAT-IF EXPLANATIONS
        // ====================================

        reasonList.innerHTML = "";

        const explanations =
            data.explanations || [];

        const featureGroups = {};


        // Group explanations by feature
        explanations.forEach(function (item) {

            if (!featureGroups[item.feature]) {

                featureGroups[item.feature] = [];
            }

            featureGroups[item.feature].push(item);
        });


        // Display grouped explanations
        Object.keys(featureGroups).forEach(
            function (feature) {

                const values =
                    featureGroups[feature];


                const li =
                    document.createElement("li");


                const results =
                    values.map(function (item) {

                        return (
                            item.value +
                            ": " +
                            item.probability.toFixed(2) +
                            "%"
                        );
                    });


                li.textContent =
                    feature +
                    " sensitivity → " +
                    results.join(" | ");


                reasonList.appendChild(li);
            }
        );


    } catch (error) {

        // ====================================
        // ERROR STATE
        // ====================================

        console.error(
            "Prediction error:",
            error
        );


        setRiskState("error");


        resultText.textContent =
            "Prediction Error";

        riskBadge.textContent =
            "ERROR";

        probability.textContent =
            "--%";

        riskMeterFill.style.width =
            "0%";


        resultDescription.textContent =
            "Unable to connect to the TabPFN prediction server. Please make sure the Flask backend is running.";


        reasonList.innerHTML =
            "<li>Check that the backend is running on port 5000.</li>";
    }


    // ====================================
    // SCROLL TO RESULT
    // ====================================

    resultCard.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });

});