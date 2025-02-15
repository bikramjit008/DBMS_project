// menuList for Header
const m = document.getElementById("menu_icon");
const m_l = document.getElementById("menu");

m.addEventListener("click", openmenu);

if(window.innerWidth <= 600){
    m_l.style.display = "none";
}

function openmenu() {
  if (m_l.style.display == "none") {
    m_l.style.display = "flex";
  } else {
    m_l.style.display = "none";
  }
}

// mainSection Typewriter effect
let t = "";
let i = 0;
let text = "Pay Tolls Easily!";
let tE = document.getElementById("tEffect");
let speed = 100;

function typeWriter() {
    if (i == text.length) {
        i = 0;
        t = "";
        tE.innerText = t;
        setTimeout(typeWriter, speed); // Pass a reference, not an invocation
    } else if (i < text.length) {
        t += text[i];
        i++;
        tE.innerText = t;
        setTimeout(typeWriter, speed); // Pass a reference, not an invocation
    }
}

typeWriter();

// Log in page jane ke liye clicked button
function rLog_in(){
  window.location.href = "login.html";
}

// Sign Up page jane ke liye button clicked
function rSign_up() {
  window.location.href = "signup.html";
}

// back to home page
function back() {
  window.location.href = "interface.html";
}

// vehicle registration ke liye clicked
function reg_veh() {
  window.location.href = "vehicle_register.html";
}

// pay toll par click karne par 
function pay_t() {
  window.location.href = "Pay_toll.html";
}

// user inter face me jane ke liye clicked
function back_user() {
  window.location.href = "user_interface.html";
}
