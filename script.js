let grid = document.getElementById("grid");
let resbox = document.getElementById("result");
for(let i = 0; i < 9; i++){
    for(let j = 0; j < 9; j++){
        let box = document.createElement("div");
        box.className = "box";
        box.id = `${i}${j}`;
        box.style.background = "white";
        grid.appendChild(box);
    }
}


let drawing = false;

// Start drawing
grid.addEventListener("pointerdown", function(e) {
    drawing = true;

    if(e.target.classList.contains("box")) {
        e.target.style.background = "black";
    }
});

// Draw while moving
grid.addEventListener("pointermove", function(e) {

    if(drawing) {
        let box = document.elementFromPoint(e.clientX, e.clientY);

        if(box && box.classList.contains("box")) {
            box.style.background = "black";
        }
    }

});

// Stop drawing
document.addEventListener("pointerup", function() {
    drawing = false;
});

document.addEventListener("pointercancel", function() {
    drawing = false;
});

function Clear(){
    for(let i = 0; i < 9; i++){
    for(let j = 0; j < 9; j++){
        let box = document.getElementById(`${i}${j}`);
        box.style.background = "white";
    }
}
}

function getData() {

    let boxes = document.querySelectorAll(".box");

    let inputs = [];

    for(let i = 0;i < 9 ;i++){
        let row = [];
        for(let j = 0;j < 9; j++){
            let box = boxes[i * 9 + j];
            if(box.style.background === "black"){
                row.push(1);
            }else{
                row.push(0);
            }
        }
        inputs.push(row);
    }

    // boxes.forEach(function(box) {

    //     if(box.style.background === "black") {
    //         inputs.push(1);
    //     }
    //     else {
    //         inputs.push(0);
    //     }

    // });
    return inputs;
}
async function sendData() {

    let mat = getData();

    try {

        let res = await fetch("https://digitrecognizerann.onrender.com/predict", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                matrix: mat
            })
        });

        let result = await res.json();

        resbox.style.display = "block";

        resbox.innerText = `Answer is: ${result.prediction}`;

    } catch(error) {

        console.log("Error:", error);
        resbox.style.display = "block";
        resbox.innerText = "Prediction failed!";

    }
} 