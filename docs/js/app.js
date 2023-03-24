

/********************* Menu Js **********************/

function windowScroll() {
  const navbar = document.getElementById("navbar");
  if (
      document.body.scrollTop >= 50 ||
      document.documentElement.scrollTop >= 50
  ) {
      navbar.classList.add("nav-sticky");
  } else {
      navbar.classList.remove("nav-sticky");
  }
}

window.addEventListener('scroll', (ev) => {
  ev.preventDefault();
  windowScroll();
})




//
/********************* light-dark js ************************/
//

const btn = document.getElementById("mode");
btn.addEventListener("click", (e) => {
  let theme = localStorage.getItem("theme");
  if (theme == "light" || theme == "") {
    document.body.setAttribute("data-layout-mode", "dark");
    localStorage.setItem("theme", "dark");
  } else {
    document.body.removeAttribute("data-layout-mode");
    localStorage.setItem("theme", "light");
  }
});

//
/********************* Swicher js ************************/
//

function toggleSwitcher() {
  var i = document.getElementById("style-switcher");
  if (i.style.left === "-189px") {
    i.style.left = "-0px";
  } else {
    i.style.left = "-189px";
  }
}

function setColor(theme) {
  document.getElementById("color-opt").href = "./css/colors/" + theme + ".css";
  toggleSwitcher(false);
}



// ********** tiny slider ** testi **

var slider = tns({
  container: '.testi-slider',
  loop: true,
  autoplay: false,
  mouseDrag: true,
  controls: false,
  navPosition: "bottom",
  nav: true,
  autoplayTimeout: 5000,
  speed: 900,
  center: false,
  animateIn: "fadeIn",
  animateOut: "fadeOut",
  controlsText: ['&#8592;', '&#8594;'],
  autoplayButtonOutput: false,
  gutter: 30,
  responsive: {

    992: {
      gutter: 30,
      items: 1.2
    },

  }
});


// ********* swiper slider ** app Slider **

new Swiper('.swiper-container', {
  loop: true,
  slidesPerView: 3,
  paginationClickable: true,
  spaceBetween: 20,
  pagination: '.swiper-pagination',
  slidesPerView: 'auto',
  paginationClickable: true,
  spaceBetween: 0,
  centeredSlides: true,
  speed: 5000,
  autoplay: true,
  breakpoints: {
    1920: {
      slidesPerView: 5,
      spaceBetween: 50
    },
    992: {
      slidesPerView: 3,
      spaceBetween: 30
    },
    768: {
      slidesPerView: 1,
      spaceBetween: 30
    }
  }
});






// Contact Form
function validateForm() {
  var name = document.forms["myForm"]["name"].value;
  var email = document.forms["myForm"]["email"].value;
  var subject = document.forms["myForm"]["subject"].value;
  var comments = document.forms["myForm"]["comments"].value;
  document.getElementById("error-msg").style.opacity = 0;
  document.getElementById('error-msg').innerHTML = "";
  if (name == "" || name == null) {
      document.getElementById('error-msg').innerHTML = "<div class='alert alert-warning'>*Please enter a Name*</div>";
      fadeIn();
      return false;
  }
  if (email == "" || email == null) {
      document.getElementById('error-msg').innerHTML = "<div class='alert alert-warning'>*Please enter a Email*</div>";
      fadeIn();
      return false;
  }
  if (subject == "" || subject == null) {
      document.getElementById('error-msg').innerHTML = "<div class='alert alert-warning'>*Please enter a Subject*</div>";
      fadeIn();
      return false;
  }
  if (comments == "" || comments == null) {
      document.getElementById('error-msg').innerHTML = "<div class='alert alert-warning'>*Please enter a Comments*</div>";
      fadeIn();
      return false;
  }

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          document.getElementById("simple-msg").innerHTML = this.responseText;
          document.forms["myForm"]["name"].value = "";
          document.forms["myForm"]["email"].value = "";
          document.forms["myForm"]["subject"].value = "";
          document.forms["myForm"]["comments"].value = "";
      }
  };
  xhttp.open("POST", "php/contact.php", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("name=" + name + "&email=" + email + "&subject=" + subject + "&comments=" + comments);
  return false;
}

function fadeIn() {
  var fade = document.getElementById("error-msg");
  var opacity = 0;
  var intervalID = setInterval(function () {
      if (opacity < 1) {
          opacity = opacity + 0.5
          fade.style.opacity = opacity;
      } else {
          clearInterval(intervalID);
      }
  }, 200);
}
