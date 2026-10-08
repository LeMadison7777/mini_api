// Animation d'apparition des cards avec GSAP
gsap.from(".grid div", {
    duration: 1,
    y: 50,
    opacity: 0,
    stagger: 0.3,
    ease: "power2.out"
});
