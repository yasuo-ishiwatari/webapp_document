const btn_blue = document.getElementById('btn_blue');
const btn_red = document.getElementById('btn_red');
const btn_green = document.getElementById('btn_green');

const box_blue = document.getElementById('box1');
const box_red = document.getElementById('box2');
const box_green = document.getElementById('box3');

let blue_on = false;
let green_on = false;

btn_blue.addEventListener('click',() => {
    if (blue_on == false) {
        blue_on = true;
        console.log("blue on");
        btn_blue.classList.add('btn_blue');
        box_blue.classList.add('box_blue')
    } else {
        blue_on = false;
        console.log("blue off");
        btn_blue.classList.remove('btn_blue')
        box_blue.classList.remove('box_blue')
    }
});

btn_red.addEventListener('click',() => {
    btn_red.classList.toggle('btn_red');
    box_red.classList.toggle('box_red');
});

btn_green.addEventListener('click',() => {
    if (green_on == false) {
        green_on = true;
        btn_green.classList.add('btn_green');
        box_green.classList.add('box_green');
    } else {
        green_on = false;
        btn_green.classList.remove('btn_green')
        box_green.classList.remove('box_green')
    }
});
