/* # ===========================================================
#  COPYRIGHT © 2024 Sueun Cho. ALL RIGHTS RESERVED.
#
#  This code is the intellectual property of Sueun Cho. 
#  Unauthorized reproduction, distribution, or use of this code 
#  is strictly prohibited. This notice must not be removed.
#  For permission to use this code or any part thereof, please 
#  contact the copyright holder.
#  
#  저작권 © 2024 조수은. "코드" 작성에 대해서만 모든 권리 보유.
#
#  이 코드는 조수은의 지적 재산입니다. 이 코드의 무단 복제, 배포, 
#  또는 사용은 엄격히 금지됩니다. 이 주석을 삭제하지 마십시오.
#  이 코드 또는 그 일부를 사용하려면 저작권자에게 문의하십시오.
#  E-mail : sueun.dev@gamil.com
#  gitrhub : sueun-dev
# =========================================================== */

(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();


    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 45) {
            $('.nav-bar').addClass('sticky-top');
        } else {
            $('.nav-bar').removeClass('sticky-top');
        }
    });


    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({ scrollTop: 0 }, 100, 'easeInOutExpo');
        return false;
    });


    // Header carousel
    $(".header-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        items: 1,
        dots: true,
        loop: true,
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        autoplayTimeout: 2500,
        smartSpeed: 800,
        margin: 24,
        dots: false,
        loop: true,
        responsive: {
            0: {
                items: 1
            },
            992: {
                items: 2
            }
        }
    });

})(jQuery);


function copyEmailToClipboard(element) {
    let email;

    // 이메일 주소 비교
    if (element === "seo@umd.edu") {
        email = "seo@umd.edu";
    } else {
        email = "umdkusa@gmail.com";
    }
    // 가상의 입력 필드 생성
    const tempInput = document.createElement("input");
    tempInput.style.position = "absolute";
    tempInput.style.left = "-9999px";
    tempInput.value = email;
    document.body.appendChild(tempInput);

    // 텍스트 선택 및 복사
    tempInput.select();
    document.execCommand("copy");

    // 입력 필드 제거
    document.body.removeChild(tempInput);

    // 사용자에게 알림
    alert("이메일 주소가 클립보드에 복사되었습니다: " + email);
}

function confirmPresident() {
    const isPresident = confirm("권한이 있으신가요?\n비밀번호를 7번 틀리면 24시간 동안 로그인 불가입니다.");
    if (isPresident) {
        return true;  // Proceed with the form submission
    } else {
        return false; // Prevent the form submission
    }
}