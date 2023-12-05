document.addEventListener("DOMContentLoaded", function() {
    let questionCounter = 0;

    const addQuestionButton = document.getElementById("add-question-btn");
    const questionContainer = document.getElementById("question-container");

    addQuestionButton.addEventListener("click", function() {
        const questionDiv = document.createElement("div");
        questionDiv.className = "question";

        const questionLabel = document.createElement("label");
        questionLabel.textContent = `Question ${questionCounter + 1}`;
        questionDiv.appendChild(questionLabel);

        const questionInput = document.createElement("input");
        questionInput.type = "text";
        questionInput.name = `question_${questionCounter}`;
        questionInput.required = true;
        questionDiv.appendChild(questionInput);

        const optionsLabel = document.createElement("label");
        optionsLabel.textContent = "Options";
        questionDiv.appendChild(optionsLabel);

        for (let i = 0; i < 4; i++) {
            const optionInput = document.createElement("input");
            optionInput.type = "text";
            optionInput.name = `question_${questionCounter}_option_${i}`;
            optionInput.required = true;
            questionDiv.appendChild(optionInput);
        }

        questionContainer.appendChild(questionDiv);
        questionCounter++;
    });

    const submitButton = document.getElementById("submit-btn");

    submitButton.addEventListener("click", function() {
        const questions = document.querySelectorAll(".question");
        const quizData = [];

        questions.forEach(function(questionDiv) {
            const questionText = questionDiv.querySelector("input[type='text']").value;
            const options = [];
            const optionInputs = questionDiv.querySelectorAll("input[type='text']:not(:first-child)");

            optionInputs.forEach(function(optionInput) {
                options.push(optionInput.value);
            });

            const correctAnswer = optionInputs[0].value; // Assuming the first option is the correct answer

            const questionObj = {
                question: questionText,
                options: options,
                correctAnswer: correctAnswer
            };

            quizData.push(questionObj);
        });

        // TODO: Send quizData to the server for processing (e.g., saving in a database)

        // Reset the form after submitting
        questionContainer.innerHTML = "";
        questionCounter = 0;
    });
});