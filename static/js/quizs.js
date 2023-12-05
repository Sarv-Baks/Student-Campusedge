document.addEventListener("DOMContentLoaded", function() {
    const quizContainer = document.getElementById("quiz-questions");
    const submitButton = document.getElementById("submit-btn");
    const resultsContainer = document.getElementById("quiz-results");

    // Fetch quiz questions from the server (assuming questionsData is retrieved from the server)
    fetch("/get_quiz_questions")
        .then(response => response.json())
        .then(questionsData => {
            // Display quiz questions and options
            displayQuizQuestions(questionsData);
        });

    function displayQuizQuestions(questionsData) {
        questionsData.forEach((question, index) => {
            const questionDiv = document.createElement("div");
            questionDiv.classList.add("question");
            questionDiv.innerText = `Question ${index + 1}: ${question.question_text}`;

            const optionsDiv = document.createElement("div");
            optionsDiv.classList.add("options");
            question.options.forEach((option, optionIndex) => {
                const optionLabel = document.createElement("label");
                optionLabel.innerHTML = `<input type="radio" name="question${index}" value="${optionIndex}"> ${option}`;
                optionsDiv.appendChild(optionLabel);
            });

            quizContainer.appendChild(questionDiv);
            quizContainer.appendChild(optionsDiv);
        });
    }

    submitButton.addEventListener("click", function() {
        // Gather student's answers
        const answers = [];
        const questionDivs = document.querySelectorAll(".question");
        questionDivs.forEach((questionDiv, index) => {
            const selectedOption = document.querySelector(`input[name="question${index}"]:checked`);
            if (selectedOption) {
                answers.push(parseInt(selectedOption.value));
            } else {
                answers.push(null); // Student didn't answer this question
            }
        });

        // Send student's answers to the server for evaluation
        fetch("/submit_answers", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ answers: answers })
        })
        .then(response => response.json())
        .then(result => {
            // Display quiz results
            let score = 0;
            result.forEach((isCorrect, index) => {
                if (isCorrect) {
                    score++;
                }
            });
            const percentage = (score / result.length) * 100;
            resultsContainer.innerText = `You scored ${score} out of ${result.length} (${percentage.toFixed(2)}%)`;
        });
    });
});
