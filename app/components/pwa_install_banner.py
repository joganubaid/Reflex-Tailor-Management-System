import reflex as rx


def pwa_install_banner() -> rx.Component:
    """Smart install banner for PWA that appears for new users on mobile devices."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("smartphone", class_name="h-6 w-6 text-purple-600"),
                rx.el.div(
                    rx.el.p(
                        "Install TailorFlow App",
                        class_name="font-semibold text-gray-800",
                    ),
                    rx.el.p(
                        "Get quick access from your home screen",
                        class_name="text-sm text-gray-600",
                    ),
                    class_name="flex-1",
                ),
                class_name="flex items-center gap-3",
            ),
            rx.el.div(
                rx.el.button(
                    "Install",
                    id="pwa-install-btn",
                    class_name="bg-purple-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-purple-700 transition-colors",
                ),
                rx.el.button(
                    rx.icon("x", class_name="h-4 w-4"),
                    id="pwa-dismiss-btn",
                    class_name="p-2 text-gray-400 hover:text-gray-600",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between p-4",
        ),
        rx.el.script("""
            // PWA Install Banner Logic
            let deferredPrompt;
            let installBanner = document.getElementById('pwa-install-banner');
            let installBtn = document.getElementById('pwa-install-btn');
            let dismissBtn = document.getElementById('pwa-dismiss-btn');

            // Check if already dismissed
            if (localStorage.getItem('pwa-dismissed') === 'true') {
                if (installBanner) installBanner.style.display = 'none';
            }

            // Check if already installed
            if (window.matchMedia('(display-mode: standalone)').matches || 
                window.navigator.standalone === true) {
                if (installBanner) installBanner.style.display = 'none';
            }

            // Listen for beforeinstallprompt event
            window.addEventListener('beforeinstallprompt', (e) => {
                e.preventDefault();
                deferredPrompt = e;
                if (installBanner) installBanner.style.display = 'block';
            });

            // Install button click
            if (installBtn) {
                installBtn.addEventListener('click', async () => {
                    if (deferredPrompt) {
                        deferredPrompt.prompt();
                        const { outcome } = await deferredPrompt.userChoice;
                        if (outcome === 'accepted') {
                            console.log('User accepted the install prompt');
                        }
                        deferredPrompt = null;
                        if (installBanner) installBanner.style.display = 'none';
                    } else {
                        // Fallback for browsers that don't support install prompt
                        window.location.href = '/install-instructions';
                    }
                });
            }

            // Dismiss button click
            if (dismissBtn) {
                dismissBtn.addEventListener('click', () => {
                    if (installBanner) installBanner.style.display = 'none';
                    localStorage.setItem('pwa-dismissed', 'true');
                });
            }

            // iOS Safari detection and instructions
            const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
            const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);

            if (isIOS && isSafari && installBtn) {
                installBtn.textContent = 'Add to Home Screen';
                installBtn.addEventListener('click', () => {
                    alert('To install this app on iOS: tap the Share button, then "Add to Home Screen"');
                });
            }
            """),
        id="pwa-install-banner",
        class_name="fixed top-0 left-0 right-0 z-50 bg-white border-b border-gray-200 shadow-sm",
        style={"display": "none"},
    )