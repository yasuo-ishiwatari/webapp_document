
const byid = document.getElementById('btn1');
const byclassname = document.getElementById('btn2');
const selectorall = document.getElementById('btn3');

const textareas = document.getElementsByTagName('textarea');

// ----------------------------------------------- //

function getElementId() {
    let str = "Element Id & Contents\n";
    str = str + "btn1: " + byid.textContent + "\n";
    str = str + "btn2: " + byclassname.textContent + "\n";
    str = str + "btn3: " + selectorall.textContent + "\n";
    textareas[0].value = str;
}

function getElementClassName() {
    const className1 = document.getElementsByClassName('className1')
    const className2 = document.getElementsByClassName('className2')
    const className3 = document.getElementsByClassName('className3')
    const className4 = document.getElementsByClassName('className4')

    let i;

    let str = "Element Class & Contents\n";    
   
    str = str + "className1: ";
    for (i = 0; i < className1.length; i++) {
        str = str + className1[i].textContent + "  ";
    }
    str = str + "\n";

    str = str + "className2: ";
    for (i = 0; i < className2.length; i++) {
        str = str + className2[i].textContent + "  ";
    }
    str = str + "\n";

    str = str + "className3: ";
    for (i = 0; i < className3.length; i++) {
        str = str + className3[i].textContent + "  ";
    }
    str = str + "\n";

    str = str + "className4: ";
    for (i = 0; i < className4.length; i++) {
        str = str + className4[i].textContent + "  ";
    }
    str = str + "\n";

    textareas[0].value = str;
}

function SelectorAll() {
    let i;
    
    // IDで取得
    const id_btn1 = document.querySelectorAll('#btn1'); 
    const id_btn2 = document.querySelectorAll('#btn2'); 
    const id_btn3 = document.querySelectorAll('#btn3'); 
    
    let str = "Element Id & Contents\n";    
   
    str = str + "btn1: " + id_btn1[0].textContent + "\n";
    str = str + "btn2: " + id_btn2[0].textContent + "\n";
    str = str + "btn3: " + id_btn3[0].textContent + "\n\n";
    
    // Classで取得
    const className1 = document.querySelectorAll('.className1');
    const className2 = document.querySelectorAll('.className2');
    const className3 = document.querySelectorAll('.className3');
    const className4 = document.querySelectorAll('.className4');

    str += "Element Class & Contents\n";    
   
    str = str + "className1: ";
    for (i = 0; i < className1.length; i++) {
        str = str + className1[i].textContent + "  ";
    }
    str = str + "\n";

    str = str + "className2: ";
    for (i = 0; i < className2.length; i++) {
        str = str + className2[i].textContent + "  ";
    }
    str = str + "\n";

    str = str + "className3: ";
    for (i = 0; i < className3.length; i++) {
        str = str + className3[i].textContent + "  ";
    }
    str = str + "\n";

    str = str + "className4: ";
    for (i = 0; i < className4.length; i++) {
        str = str + className4[i].textContent + "  ";
    }
    str = str + "\n\n";

    // Tagで取得
    const tag_btn = document.querySelectorAll('button'); 
    const tag_p = document.querySelectorAll('p'); 
    const tag_span = document.querySelectorAll('span'); 

    str += "Tag Name & Contents\n";    
   
    str = str + "button: ";
    for (i = 0; i < tag_btn.length; i++) {
        str = str + tag_btn[i].textContent + "  ";
    }
    str = str + "\n";

    str = str + "p: ";
    for (i = 0; i < tag_p.length; i++) {
        str = str + tag_p[i].textContent + "  ";
    }
    str = str + "\n";

    str = str + "span: ";
    for (i = 0; i < tag_span.length; i++) {
        str = str + tag_span[i].textContent + "  ";
    }
    str = str + "\n";

    textareas[0].value = str;
}




byid.addEventListener('click',() => {
    getElementId();
});

byclassname.addEventListener('click',() => {
    getElementClassName();
});

selectorall.addEventListener('click',() => {
    SelectorAll();
});



