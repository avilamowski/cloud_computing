<script>
  import { onMount } from 'svelte';
  import { post } from '$lib/api';
  import { PUBLIC_COGNITO_APP_CLIENT_ID, PUBLIC_COGNITO_URL, PUBLIC_REDIRECT_URL } from '$env/static/public';
  let code = '';
  let error = '';

  onMount(() => {
    const params = new URLSearchParams(window.location.search);
    code = params.get('code');
    error = params.get('error');

    if (code) {
      handleCognitoCode(code);
    } else if (error) {
      console.error('OAuth Error:', error);
    }
  });

  async function handleCognitoCode(code) {
    const response = await post(`${PUBLIC_COGNITO_URL}/oauth2/token/`, {
        grant_type: "authorization_code",
        client_id: PUBLIC_COGNITO_APP_CLIENT_ID,
        redirect_uri: PUBLIC_REDIRECT_URL,
        code: code
    });
    const token = await response.json();
    console.log(token)
    localStorage.setItem('token', token);

}
    // }).then(response => response.json())
    //   .then(data => {
    //     console.log('OAuth Response:', data);
    //     localStorage.setItem('token', data.id_token);
    //     window.location.href = '/';
    //   })
    //   .catch(error => {
    //     console.error('OAuth Error:', error);
    //   });
</script>

<div>
</div>