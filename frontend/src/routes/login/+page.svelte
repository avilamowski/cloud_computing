<script>
  import { goto } from '$app/navigation';
  import { signIn, fetchAuthSession } from 'aws-amplify/auth';
  import { token } from '../../routes/store';

    const login = async (e) => {
        e.preventDefault();
        const form = e.target;
        const email = form.email.value;
        const password = form.password.value;

        const signInInput = {
            username: email,
            password: password
        };
        await signIn(signInInput);

        const session = await fetchAuthSession();
        token.set(session?.tokens?.idToken);
        goto('/');
    }
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

				<!-- <ListErrors errors={form?.errors} /> -->

				<form method="POST" on:submit={login}>
					<fieldset class="form-group">
						<input
							class="form-control form-control-lg"
							name="email"
							type="email"
							required
							placeholder="Email"
						/>
					</fieldset>
					<fieldset class="form-group">
						<input
							class="form-control form-control-lg"
							name="password"
							type="password"
							required
							placeholder="Password"
						/>
					</fieldset>
					<button class="btn btn-lg btn-primary pull-xs-right" type="submit">Sign in</button>
				</form>
			</div>
		</div>
	</div>
</div>