document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('mobileMenuToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    let isMenuOpen = false;

    if (toggleBtn && mobileMenu) {
        toggleBtn.addEventListener('click', () => {
            isMenuOpen = !isMenuOpen;
            if (isMenuOpen) {
                // Open menu
                mobileMenu.classList.remove('-translate-y-full', 'opacity-0', 'invisible', 'pointer-events-none');
                mobileMenu.classList.add('translate-y-0', 'opacity-100', 'visible', 'pointer-events-auto');
                // Change hamburger to close icon
                toggleBtn.innerHTML = '<svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round"></path></svg>';
            } else {
                // Close menu
                mobileMenu.classList.remove('translate-y-0', 'opacity-100', 'visible', 'pointer-events-auto');
                mobileMenu.classList.add('-translate-y-full', 'opacity-0', 'invisible', 'pointer-events-none');
                // Change back to hamburger icon
                toggleBtn.innerHTML = '<svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h16" stroke-linecap="round" stroke-linejoin="round"></path></svg>';
            }
        });
    }

    // Language switcher toggle for mobile
    const langBtn = document.getElementById('langSwitcherBtn');
    if (langBtn) {
        langBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            const dropdown = langBtn.nextElementSibling;
            if (dropdown) {
                dropdown.classList.toggle('opacity-0');
                dropdown.classList.toggle('invisible');
                dropdown.classList.toggle('opacity-100');
                dropdown.classList.toggle('visible');
            }
        });

        // Close when clicking outside
        document.addEventListener('click', (e) => {
            if (!langBtn.contains(e.target)) {
                const dropdown = langBtn.nextElementSibling;
                if (dropdown && dropdown.classList.contains('opacity-100')) {
                    dropdown.classList.add('opacity-0', 'invisible');
                    dropdown.classList.remove('opacity-100', 'visible');
                }
            }
        });
    }
});
