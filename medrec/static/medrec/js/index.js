document.addEventListener('alpine:init', () => {
    Alpine.data('index', () => ({
        isMenuCollapsed: false,
    }));
});
