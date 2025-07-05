const sliderTabs = document.querySelectorAll(".slider-tab");
const sliderIndicator = document.querySelector(".slider-indicator");
const aboutButton = document.querySelector(".about-main")

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