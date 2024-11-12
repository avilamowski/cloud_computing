<script>
  import { goto } from "$app/navigation";
  import { signUp, confirmSignUp } from "aws-amplify/auth";
  import { isLoading, toastStore } from "../../routes/store";
  import Toast from "../../routes/Toast.svelte";

  let sentEmail = "";
  let showModal = false;
  let email = "";
  let password = "";
  let username = "";
  let passwordRequirements = {
    length: false,
    lowercase: false,
    uppercase: false,
    number: false,
    symbol: false,
  };

  // Función para validar los requisitos de la contraseña
  const validatePassword = (password) => {
    passwordRequirements.length = password.length >= 8;
    passwordRequirements.lowercase = /[a-z]/.test(password);
    passwordRequirements.uppercase = /[A-Z]/.test(password);
    passwordRequirements.number = /[0-9]/.test(password);
    passwordRequirements.symbol = /[!@#$%^&*(),.?":{}|<>]/.test(password);
  };

  const register = async (e) => {
    e.preventDefault();

    // Validamos la contraseña antes de enviar
    if (!Object.values(passwordRequirements).every(Boolean)) {
      toastStore.show("Password must accomplish all requirements", "error");
      return;
    }

    const signUpInput = {
      username: email,
      password: password,
      options: {
        userAttributes: {
          email: email,
          preferred_username: username,
        },
      },
    };

    try {
      isLoading.set(true);
      await signUp(signUpInput);
      sentEmail = email;
      toggleModal(); // Mostrar el modal para el código de confirmación
    } catch (error) {
      toastStore.show(error.message || "Registration failed.", "error");
    } finally {
      isLoading.set(false);
    }
  };

  const sendCode = async (e) => {
    e.preventDefault();
    const form = e.target;
    const code = form.code.value;

    try {
      isLoading.set(true);
      const data = await confirmSignUp({
        username: sentEmail,
        confirmationCode: code,
      });

      if (data.isSignUpComplete) {
        goto("/login"); // Redirigir a login
      }
    } catch (error) {
      toastStore.show(error.message || "Code confirmation failed.", "error");
    } finally {
      isLoading.set(false);
    }
  };

  function toggleModal() {
    showModal = !showModal;
    document.body.style.overflow = showModal ? "hidden" : "";
  }
</script>

<svelte:head>
  <title>Sign up</title>
</svelte:head>

<div class="auth-page">
  <div class="container page">
    <div class="row">
      <div class="col-md-6 offset-md-3 col-xs-12">
        <h1 class="text-xs-center">Sign up</h1>
        <p class="text-xs-center">
          <a href="/login">Have an account?</a>
        </p>

        <!-- Registration Form -->
        <form method="POST" on:submit={register}>
          <fieldset class="form-group">
            <input
              class="form-control form-control-lg"
              bind:value={email}
              name="email"
              type="email"
              required
              placeholder="Email"
            />
          </fieldset>
          <fieldset class="form-group">
            <input
              class="form-control form-control-lg"
              bind:value={username}
              name="username"
              type="text"
              required
              placeholder="Your Name"
            />
          </fieldset>
          <fieldset class="form-group">
            <input
              class="form-control form-control-lg"
              bind:value={password}
              on:input={() => validatePassword(password)}
              name="password"
              type="password"
              required
              placeholder="Password"
            />
            <!-- Requisitos de la contraseña -->
            <ul class="password-requirements">
              <li class={passwordRequirements.length ? "valid" : ""}>
                At least 8 characters
              </li>
              <li class={passwordRequirements.lowercase ? "valid" : ""}>
                At least one lowercase letter
              </li>
              <li class={passwordRequirements.uppercase ? "valid" : ""}>
                At least one uppercase letter
              </li>
              <li class={passwordRequirements.number ? "valid" : ""}>
                At least one number
              </li>
              <li class={passwordRequirements.symbol ? "valid" : ""}>
                At least one symbol (e.g., !@#$%^&*)
              </li>
            </ul>
          </fieldset>
          <button class="btn btn-lg btn-primary pull-xs-right">Sign up</button>
        </form>

        {#if showModal}
          <div class="modal">
            <div class="modal-content">
              <h3>Enter Confirmation Code</h3>
              <form method="POST" on:submit={sendCode}>
                <fieldset class="form-group">
                  <input
                    class="form-control form-control-lg"
                    name="code"
                    type="text"
                    required
                    placeholder="Code"
                  />
                </fieldset>
                <button class="btn btn-lg btn-primary pull-xs-right"
                  >Submit</button
                >
              </form>
            </div>
          </div>
        {/if}
      </div>
    </div>
  </div>
</div>

<!-- Toast component -->
<Toast />

<style>
  .password-requirements {
    list-style: none;
    padding: 0;
    font-size: 0.9em;
    color: #6c757d;
  }
  .password-requirements li.valid {
    color: green;
  }
  .modal {
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.4);
  }
  .modal-content {
    background-color: #fefefe;
    padding: 20px;
    border: 1px solid #888;
    width: 50%;
    max-width: 600px;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  }
</style>
