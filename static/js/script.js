// Dark Mode Toggle
const themeToggle = document.createElement('button');
themeToggle.id = 'theme-toggle';
themeToggle.innerHTML = '🌙';
document.body.appendChild(themeToggle);

const currentTheme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', currentTheme);
themeToggle.innerHTML = currentTheme === 'dark' ? '☀️' : '🌙';

themeToggle.addEventListener('click', () => {
    const theme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    themeToggle.innerHTML = theme === 'dark' ? '☀️' : '🌙';
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.bike-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(card);
});

// Form validation
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const inputs = form.querySelectorAll('input[required]');
        let valid = true;
        inputs.forEach(input => {
            if (!input.value.trim()) {
                input.style.borderColor = 'red';
                valid = false;
            } else {
                input.style.borderColor = '#ddd';
            }
        });
        if (!valid) {
            e.preventDefault();
            alert('Veuillez remplir tous les champs requis.');
        }
    });
});

// Reservation page specific validation (if present)
const reserveForm = document.querySelector('form');
if (reserveForm && document.getElementById('start_date') && document.getElementById('end_date')) {
    reserveForm.addEventListener('submit', function(e) {
        const startInput = document.getElementById('start_date');
        const endInput = document.getElementById('end_date');
        const start = new Date(startInput.value);
        const end = new Date(endInput.value);
        const now = new Date();
        // If invalid date values, prevent
        if (isNaN(start.getTime()) || isNaN(end.getTime())) {
            e.preventDefault();
            alert('Veuillez fournir des dates valides.');
            return;
        }
        if (start < now) {
            e.preventDefault();
            alert('La date de début doit être dans le futur.');
            return;
        }
        if (end <= start) {
            e.preventDefault();
            alert('La date de fin doit être après la date de début.');
            return;
        }
        const maxMs = 7 * 24 * 60 * 60 * 1000; // 7 days
        if ((end - start) > maxMs) {
            e.preventDefault();
            alert('La réservation ne peut pas durer plus de 7 jours.');
            return;
        }
    });
}

// Zoom controls: change root font-size (scale) and persist
;(function(){
    const defaultSize = 16;
    const key = 'site_zoom'
    function getZoom(){
        const v = parseFloat(localStorage.getItem(key))
        return isNaN(v) ? 1 : v
    }
    function applyZoom(z){
        document.documentElement.style.fontSize = (defaultSize * z) + 'px'
        localStorage.setItem(key, String(z))
    }
    // init
    applyZoom(getZoom())

    const btnIn = document.getElementById('zoom-in')
    const btnOut = document.getElementById('zoom-out')
    const btnReset = document.getElementById('zoom-reset')
    if(btnIn) btnIn.addEventListener('click', ()=> applyZoom(Math.min(1.4, getZoom() + 0.1)))
    if(btnOut) btnOut.addEventListener('click', ()=> applyZoom(Math.max(0.7, getZoom() - 0.1)))
    if(btnReset) btnReset.addEventListener('click', ()=> applyZoom(1))
})();

// keyboard shortcuts: Ctrl/Cmd + +/- to zoom, Ctrl/Cmd + 0 to reset
document.addEventListener('keydown', function(e){
    const ctrl = e.ctrlKey || e.metaKey
    if(!ctrl) return
    if(e.key === '+' || e.key === '='){
        e.preventDefault();
        const v = parseFloat(localStorage.getItem('site_zoom')||1)
        const nv = Math.min(1.4, v + 0.1)
        document.documentElement.style.fontSize = (16 * nv) + 'px'
        localStorage.setItem('site_zoom', nv)
    }
    if(e.key === '-'){
        e.preventDefault();
        const v = parseFloat(localStorage.getItem('site_zoom')||1)
        const nv = Math.max(0.7, v - 0.1)
        document.documentElement.style.fontSize = (16 * nv) + 'px'
        localStorage.setItem('site_zoom', nv)
    }
    if(e.key === '0'){
        e.preventDefault();
        document.documentElement.style.fontSize = (16 * 1) + 'px'
        localStorage.setItem('site_zoom', 1)
    }
})
