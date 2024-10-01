const formContainer = document.getElementById('formContainer');

function showRegisterForm() {
    formContainer.innerHTML = `
        <form id="registerForm">
            <input type="text" id="usuario" name="usuario" placeholder="Ingresa tu nombre" required>
            <input type="email" id="email" name="correo" placeholder="Ingresa tu correo" required>
            <input type="password" id="contraseña" name="contraseña" placeholder="Ingresa tu contraseña" required>
            <section class="mostrar">
                <label class="lbel" for="checkbox">Mostrar contraseña</label>
                <input type="checkbox" id="checkbox" name="checkbox">
            </section>
            <button type="button" class="submit" id="submitGeneral">Enviar</button>
            <section class="botones">
                <button type="button" class="btn" id="loginBtn">Login</button>
                <button type="button" class="btn" id="registerBtn">Register</button>
            </section>
        </form>
    `;
    attachCheckboxEvent();
    attachButtonEvents();

    const submitButton = document.getElementById('submitGeneral');
    submitButton.addEventListener('click', registerUser);
}

function showLoginForm() {
    formContainer.innerHTML = `
        <form id="loginForm">
            <input type="email" id="loginEmail" placeholder="Ingresa tu correo" required>
            <input type="password" id="loginPassword" placeholder="Ingresa tu contraseña" required>
            <section class="mostrar">
                <label class="lbel" for="loginCheckbox">Mostrar contraseña</label>
                <input type="checkbox" id="loginCheckbox">
            </section>
            <button type="button" id="submitLogin" style="background-color:#9f111b; height: 30px; width: 100px; margin-bottom: 15px; color: #fff; border-radius: 10px; box-shadow: -5px 5px 0 black; cursor: pointer;">Enviar</button>
            <section class="botones">
                <button type="button" class="btn" id="registerBtnFromLogin">Register</button>
                <button type="button" class="btn" id="loginBtnFromLogin">Login</button>
            </section>
        </form>
    `;
    attachLoginCheckboxEvent();
    attachButtonEvents();

    const loginButton = document.getElementById('submitLogin');
    loginButton.addEventListener('click', loginUser);
}

function registerUser() {
    const username = document.getElementById('usuario').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('contraseña').value;

    if (username && email && password) {
        const user = { username, email, password };
        localStorage.setItem('user', JSON.stringify(user));
        alert('Registro completado. Ahora puedes iniciar sesión.');
        showLoginForm();
    } else {
        alert('Por favor completa todos los campos.');
    }
}

function loginUser() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    const user = JSON.parse(localStorage.getItem('user'));

    if (user && user.email === email && user.password === password) {
        alert('Inicio de sesión exitoso.');
        // Aquí puedes redirigir al usuario a otra página o mostrar información adicional
    } else {
        alert('Credenciales incorrectas. Intenta nuevamente.');
    }
}

function attachCheckboxEvent() {
    const checkbox = document.getElementById('checkbox');
    checkbox.addEventListener('click', () => {
        const passwordInput = document.getElementById('contraseña');
        passwordInput.type = checkbox.checked ? 'text' : 'password';
    });
}

function attachLoginCheckboxEvent() {
    const loginCheckbox = document.getElementById('loginCheckbox');
    loginCheckbox.addEventListener('click', () => {
        const loginPasswordInput = document.getElementById('loginPassword');
        loginPasswordInput.type = loginCheckbox.checked ? 'text' : 'password';
    });
}

function attachButtonEvents() {
    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');
    const registerBtnFromLogin = document.getElementById('registerBtnFromLogin');

    if (loginBtn) {
        loginBtn.addEventListener('click', showLoginForm);
    }
    if (registerBtn) {
        registerBtn.addEventListener('click', showRegisterForm);
    }
    if (registerBtnFromLogin) {
        registerBtnFromLogin.addEventListener('click', showRegisterForm);
    }
}

showRegisterForm();