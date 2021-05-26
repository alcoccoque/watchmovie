const slider = document.querySelector(".slider");
const btnLeft = document.getElementById("moveLeft");
const btnRight = document.getElementById("moveRight");
const indicators = document.querySelectorAll(".indicator");

let baseSliderWidth = slider.offsetWidth;
let activeIndex = 0; // the current page on the slider




// Update the indicators that show which page we're currently on
function updateIndicators(index) {
  indicators.forEach((indicator) => {
    indicator.classList.remove("active");
  });
  let newActiveIndicator = indicators[index];
  newActiveIndicator.classList.add("active");
}

// Scroll Left button
btnLeft.addEventListener("click", (e) => {
  let movieWidth = document.querySelector(".film").getBoundingClientRect()
    .width;
  let scrollDistance = movieWidth * 6; // Scroll the length of 6 movies.

  slider.scrollBy({
    top: 0,
    left: -scrollDistance,
    behavior: "smooth",
  });
  activeIndex = (activeIndex - 1) % 3;
  console.log(activeIndex);
  updateIndicators(activeIndex);
});

// Scroll Right button
btnRight.addEventListener("click", (e) => {
  let movieWidth = document.querySelector(".film").getBoundingClientRect()
    .width;
  let scrollDistance = movieWidth * 5; // Scroll the length of 6 movies. TODO: make work for mobile because (4 movies/page instead of 6)

  console.log(`movieWidth = ${movieWidth}`);
  console.log(`scrolling right ${scrollDistance}`);





  // if we're on the last page
  if (activeIndex == 2) {
    // duplicate all the items in the slider (this is how we make 'looping' slider)
    populateSlider();
    slider.scrollBy({
      top: 0,
      left: +scrollDistance,
      behavior: "smooth",
    });
    activeIndex = 0;
    updateIndicators(activeIndex);
  } else {
    slider.scrollBy({
      top: 0,
      left: +scrollDistance,
      behavior: "smooth",
    });
    activeIndex = (activeIndex + 1) % 3;
    console.log(activeIndex);
    updateIndicators(activeIndex);
  }
});

var swiper = new Swiper('.product-slider', {
        spaceBetween: 30,
        effect: 'fade',
        // initialSlide: 2,
        loop: false,
        navigation: {
            nextEl: '.next',
            prevEl: '.prev'
        },
        // mousewheel: {
        //     // invert: false
        // },
        on: {
            init: function(){
                var index = this.activeIndex;

                var target = $('.product-slider__item').eq(index).data('target');

                console.log(target);

                $('.product-img__item').removeClass('active');
                $('.product-img__item#'+ target).addClass('active');
            }
        }

    });

    swiper.on('slideChange', function () {
        var index = this.activeIndex;

        var target = $('.product-slider__item').eq(index).data('target');

        console.log(target);

        $('.product-img__item').removeClass('active');
        $('.product-img__item#'+ target).addClass('active');

        if(swiper.isEnd) {
            $('.prev').removeClass('disabled');
            $('.next').addClass('disabled');
        } else {
            $('.next').removeClass('disabled');
        }

        if(swiper.isBeginning) {
            $('.prev').addClass('disabled');
        } else {
            $('.prev').removeClass('disabled');
        }
    });

    $(".js-fav").on("click", function() {
        $(this).find('.heart').toggleClass("is-active");
    });

  
  
  


  


