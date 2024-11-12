<script>
  import { goto } from "$app/navigation";
  import { signIn, fetchAuthSession } from "aws-amplify/auth";
  import { token, isLoading, toastStore } from "../../routes/store";
  import Toast from "../../routes/Toast.svelte";

  let email = "";
  let password = "";
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

  // Evento para manejar el envío del formulario
  const login = async (e) => {
    e.preventDefault();

    // Validamos la contraseña antes de enviar
    if (!Object.values(passwordRequirements).every(Boolean)) {
      toastStore.show("Password must accomplish all requirements", "error");
      return;
    }

    try {
      isLoading.set(true);
      await signIn({ username: email, password });
      const session = await fetchAuthSession();
      token.set(session?.tokens?.idToken);
      goto("/");
    } catch (error) {
      toastStore.show(
        error.message || "Login failed. Please try again.",
        "error"
      );
      console.error("Login error:", error);
    } finally {
      isLoading.set(false);
    }
  };
</script>

<svelte:head>
  <title>Sign in</title>
</svelte:head>

<div class="auth-page">
  <div class="container page">
    <div class="row">
      <div class="col-md-6 offset-md-3 col-xs-12">
        <h1 class="text-xs-center">Sign In</h1>
        <p class="text-xs-center">
          <a href="/register">Need an account?</a>
        </p>

        <!-- Login Form -->
        <form method="POST" on:submit={login}>
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
              bind:value={password}
              on:input={() => validatePassword(password)}
              name="password"
              type="password"
              required
              placeholder="Password"
            />
            <!-- Requisitos de la contraseña -->
            <!-- <ul class="password-requirements">
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
                At least one symbol (ie. !@#$%^&*)
              </li>
            </ul> -->
          </fieldset>
          <button class="btn btn-lg btn-primary pull-xs-right" type="submit"
            >Sign in</button
          >
        </form>
      </div>
    </div>
  </div>
</div>

<!-- Toast component -->
<Toast />

<!-- Estilos para los requisitos -->
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
</style>
