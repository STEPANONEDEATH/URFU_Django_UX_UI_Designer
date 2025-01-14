document.addEventListener('DOMContentLoaded', function () {
    const hamburger  = document.querySelector('.hamburger');
    const aside      = document.querySelector('aside');
    const menu       = document.querySelector('.menu');
    const links      = document.querySelectorAll('.menu a');
    const isMobile   = () => window.innerWidth <= 768; // Проверка мобильного устройства

    hamburger.addEventListener('click', function () {
        if (isMobile()) {
            if (aside.style.width === '250px') {
                closeSidebar();
            } else {
                openSidebar();
            }
        }
    });

    // Закрытие бокового меню при клике на ссылку (только для мобильных устройств)
    links.forEach(link => {
        link.addEventListener('click', function (e) {
            if (isMobile()) {
                e.preventDefault();
                const href = this.href;

                closeSidebar();
                setTimeout(() => {
                    window.location.href = href;
                }, 300);
            }
        });
    });

    function openSidebar() {
        aside.style.width = '250px';
        aside.style.visibility = 'visible';
        menu.style.display = 'block';
    }

    function closeSidebar() {
        aside.style.width = '0';
        aside.style.visibility = 'hidden';
        menu.style.display = 'none';
    }
});
