<script>
  import { goto } from '$app/navigation';
    import { signUp, confirmSignUp, fetchAuthSession } from 'aws-amplify/auth';
	import { token } from  '../../routes/store';

    let sentEmail = '';

    const register = async (e) => {
        e.preventDefault();
        const form = e.target;
        const email = form.email.value;
        const password = form.password.value;
        const username = form.username.value;

        const signUpInput = {
            username: email,
            password: password,
            options: {
                userAttributes: {
                    email: email,
                    preferred_username: username
                }
            }
        };

        await signUp(signUpInput);
        sentEmail = email;
        console.log("Email sent")

    }

    const sendCode = async(e) => {
        e.preventDefault();
        const form = e.target;
        const code = form.code.value;

        const data = await confirmSignUp({
            username: sentEmail,
            confirmationCode: code
        })
        if (data.isSignUpComplete) {
            console.log("Code sent");

            const session = await fetchAuthSession();
            token.set(session?.tokens?.idToken);
            goto('/');
        }
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

				<!-- <ListErrors errors={form?.errors} /> -->

				<form method="POST" on:submit={register}>
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
							name="username"
							type="text"
							required
							placeholder="Your Name"
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
					<button class="btn btn-lg btn-primary pull-xs-right">Sign up</button>
				</form>

			</div>

		</div>
        {#if sentEmail}
        <div class="row">
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
                <button class="btn btn-lg btn-primary pull-xs-right">Sign up</button>
            </form>
        </div>
        {/if}
	</div>
</div>