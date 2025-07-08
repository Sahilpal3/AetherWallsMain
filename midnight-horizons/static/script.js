const sliderTabs = document.querySelectorAll(".slider-tab");
const sliderIndicator = document.querySelector(".slider-indicator");
const aboutButton = document.querySelector(".about-main");

//UPDATE the indicator height and width
const updatePagination = (tab, index) => {
  sliderIndicator.style.transform = `translateX(${tab.offsetLeft - 20}px)`;
  sliderIndicator.style.width = `${tab.getBoundingClientRect().width}px`;
};

//intialize swiper
const swiper = new Swiper(".slider-container", {
  effect: "fade",
  speed: 1300,
  autoplay: { delay: 4000, disableOnInteraction: false },
  on: {
    //update the idicator on slide change
    slideChange: () => {
      const currentTabIndex = [...sliderTabs].indexOf(
        sliderTabs[swiper.activeIndex]
      );
      updatePagination(sliderTabs[swiper.activeIndex], currentTabIndex);
    },
    //maunual slide loop
  },
});

//update slide and indicator on tab click
sliderTabs.forEach((tab, index) => {
  tab.addEventListener("click", () => {
    swiper.slideTo(index);
    updatePagination(tab, index);
  });
});

updatePagination(sliderTabs[0], 0);
window.addEventListener("resize", () =>
  updatePagination(sliderTabs[swiper.activeIndex], 0)
);

function openAbout() {
  const modal = document.getElementById("about-modal");
  modal.classList.add("show");
}
function closeAbout() {
  const modal = document.getElementById("about-modal");
  modal.classList.remove("show");
}
function closeAccount(){
  const modal = document.getElementById("acc-panel");
  modal.classList.remove("show");
}
async function openSignin() {
  closeRegister();

  const isLoggedin = await handleAccount();
  const modal = isLoggedin ? document.getElementById("acc-panel"):document.getElementById("sign-in");

  if(isLoggedin){
    try {
      const res = await fetch("/api/session");
      const data = await res.json();
      const accContent = document.getElementById("acc-content");

      accContent.innerHTML = `
        <span class="close-btn" onclick="closeAccount()">✕</span>
        <h3>Welcome, ${data.username || data.username}</h3>
        <p>You are logged in as <strong>${data.email}</strong></p>
        <p>Upload Your own Wallpapers:</p><button class="upload-btn" onclick="uploadFLow()">Upload</button>
        <button onclick="logout()" class="logout-btn">Logout</button>
      `;
    } catch (err) {
      console.error("Session fetch failed", err);
    }
  }
  if (modal) modal.classList.add("show");
}
function closeSignin() {
  const modal = document.getElementById("sign-in");
  modal.classList.remove("show");
}
function openRegister() {
  closeSignin();
  document.getElementById("register").classList.add("show");
}
function closeRegister() {
  document.getElementById("register").classList.remove("show");
}

async function logout() {
  await fetch("/logout", { method: "POST" });
  location.reload(); // Refresh UI to reflect logout
}

async function handleAccount(){
  //check if anybody is logged in or not
  const res = await fetch("/api/session");
  const data = await res.json();

  if(data.logged_in){
    return true;
  }
  return false;
}

//Handling forms

document.addEventListener("DOMContentLoaded", function () {
  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form");
  const uploadForm = document.getElementById("upload-form");

  //Login-form
  if (loginForm) {
    loginForm.addEventListener("submit", async function (e) {
      e.preventDefault();
      const email = loginForm.email.value;
      const password = loginForm.password.value;
      const message = document.getElementById("login-message");

      //send inputs, get response from py backend
      try {
        const response = await fetch("/login", {
          method: "POST",
          //sending the form data in the same format as a traditional HTML form would.
          headers: { "Content-type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams({ email, password }),
        });

        const data = await response.json();
        if (response.ok) {
          message.textContent = "Login Successful";
          message.style.color = "lightgreen";
          setTimeout(() => window.location.reload(), 2000); // Reload to update session UI
        } else {
          message.textContent = data.Error || "Login Failed";
          message.style.color = "salmon";
        }
      } catch (err) {
        message.textContent = "An Error occured try again!!";
        message.style.color = "salmon";
      }
    });
  }

  //Register-form
  if (registerForm) {
    registerForm.addEventListener("submit", async function (e) {
      e.preventDefault();
      const email = registerForm.email.value;
      const password = registerForm.password.value;
      const username = registerForm.username.value;
      const message = document.getElementById("login-message");

      //send inputs to backend
      try {
        const response = await fetch("/register", {
          method: "POST",
          headers: { "Content-type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams({ email, password, username }),
        });

        const data = await response.json();
        if (response.ok) {
          message.textContent = "Registration successful!";
          message.style.color = "lightgreen";
          //After Registration auto-login
          const loginRes = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({ email, password }),
          });
          if (loginRes.ok) {
            location.reload();
          } else {
            alert(data.error || "Registration Failed");
          }
        }else{
          message.textContent = data.error || "Registration failed.";
          message.style.color = "salmon";
        }
      } catch (err) {
        message.textContent = "An Error occured try again";
          message.style.color = "salmon";
      }
    });
  }

  //upload form
  if(uploadForm){
    uploadForm.addEventListener("submit", async function (e){
      e.preventDefault();

      const formData = new FormData(uploadForm);

      try{
        const res = await fetch("/upload",{
          method : "POST",
          body : formData
        });

        const data = await res.json()

        if(res.ok){
          alert('Upload Successful');
          closeUpload();
          uploadForm.reset();
        } else {
          alert(data.error || "Upload Failed")
        }
      }catch (err){
        alert("Error uploading. Try again!");
      }
    })
  }
});

//UploadingPics
function uploadFLow(){
  const uploadModal = document.getElementById("upload-modal")
  uploadModal.classList.add("show");
}

function closeUpload(){
  const uploadModal = document.getElementById("upload-modal")
  uploadModal.classList.remove("show");
}