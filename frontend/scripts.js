async function fetchAccounts() {
    const accountsDiv = document.getElementById('accounts');
    const loadingDiv = document.getElementById('loading');
    loadingDiv.style.display = 'block'; // Show loading text
    accountsDiv.innerHTML = ''; // Clear accounts content
    try {
        // Check if pywebview is defined
        if (typeof pywebview === 'undefined' || !pywebview.api) {
            throw new Error('PyWebView is not defined. Ensure the application is running in a PyWebView environment.');
        } else {
            console.log('PyWebView is ready.');
        }

        const accounts = await pywebview.api.fetch_accounts();
        loadingDiv.style.display = 'none'; // Hide loading text
        accounts.forEach(account => {
            const accountDiv = document.createElement('div');
            accountDiv.className = 'account';
            accountDiv.innerHTML = `
                <img class="avatar" src="${account[Object.keys(account)[0]].account_summary.avatar_url}" alt="Avatar">
                <p>${account[Object.keys(account)[0]].account_summary.steam_name}</p>
                <p>Owns Schedule I: ${account[Object.keys(account)[0]].Schedule_I_owned}</p>
            `;
            accountDiv.addEventListener('click', () => selectProfile(account)); // Add click event listener
            accountsDiv.appendChild(accountDiv);
        });
    } catch (error) {
        loadingDiv.style.display = 'none'; // Hide loading text
        accountsDiv.innerHTML = `Error fetching accounts: ${error.message || error}`;
        console.error(error);
    }
}

function selectProfile(account) {
    // Deselect any previously selected profile
    document.querySelectorAll('.account').forEach(accountDiv => {
        accountDiv.classList.remove('selected');
    });

    // Highlight the selected profile
    const selectedAccountDiv = event.currentTarget;
    selectedAccountDiv.classList.add('selected');

    // Send the selected account to Python and navigate to the workspace page
    if (typeof pywebview !== 'undefined' && pywebview.api) {
        pywebview.api.select_account(account).then(() => {
            pywebview.api.load_stats();
        });
    }

    console.log('Selected profile:', account);
}

async function checkSteamApiKey() {
    const apiKeyPopup = document.getElementById('api-key-popup');
    const saveApiKeyButton = document.getElementById('save-api-key-button');
    const apiKeyInput = document.getElementById('api-key-input');

    // Check if the API key is set
    const hasApiKey = await pywebview.api.check_steam_api_key();
    if (!hasApiKey) {
        apiKeyPopup.style.display = 'flex'; // Show the popup
    }

    // Save the API key when the button is clicked
    saveApiKeyButton.addEventListener('click', async () => {
        const apiKey = apiKeyInput.value.trim();
        if (apiKey) {
            const response = await pywebview.api.set_steam_api_key(apiKey);
            if (response.status === 'success') {
                apiKeyPopup.style.display = 'none'; // Hide the popup
                fetchAccounts(); // Fetch accounts after saving the API key
            } else {
                alert(`Error: ${response.message}`);
            }
        } else {
            alert('Please enter a valid Steam API key.');
        }
    });
}

// Call checkSteamApiKey on page load
window.onload = () => {
    const checkPyWebViewReady = setInterval(() => {
        if (typeof pywebview !== 'undefined' && pywebview.api) {
            clearInterval(checkPyWebViewReady);
            checkSteamApiKey(); // Check for API key
            fetchAccounts(); // Fetch accounts
        }
    }, 2000);
};