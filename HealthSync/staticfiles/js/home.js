const loginsec = document.querySelector('.login-section');
const loginlink = document.querySelector('.login-link');
const registerlink = document.querySelector('.register-link');

// Show register form, hide login form
registerlink.addEventListener('click', () => {
    loginsec.classList.add('active');
});

// Show login form, hide register form
loginlink.addEventListener('click', () => {
    loginsec.classList.remove('active');
});
