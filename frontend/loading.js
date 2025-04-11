async function initializeLoadingPage() {
    const backButton = document.getElementById('back-button');
    const headingDiv = document.getElementById('heading');
    const statsDiv = document.getElementById('stats');

    // Add functionality to the back button
    backButton.addEventListener('click', () => {
        console.log("Back button clicked. Navigating to accounts page..."); // Debug log
        window.location.href = './accounts.html'; // Navigate back to the main page
    });

    try {
        console.log("Calling get_save_folders from Python..."); // Debug log
        const saveFoldersResponse = await pywebview.api.get_save_folders();
        console.log("Response from get_save_folders:", saveFoldersResponse); // Debug log
        if (saveFoldersResponse.status === "success") {
            const saveFolders = saveFoldersResponse.save_folders;
            headingDiv.innerHTML = `<h1>Select a save folder</h1>`; // Set the heading
            statsDiv.innerHTML = ""; // Clear previous content
            saveFolders.forEach(folder => {
                const folderDiv = document.createElement('div');
                folderDiv.className = 'folder';
                folderDiv.innerHTML = `
                    <img class="folder-icon" src="./assets/folder-icon.webp" alt="Folder Icon">
                    <p>${folder}</p>
                `;
                folderDiv.addEventListener('click', () => selectFolder(folder)); // Add click event listener
                statsDiv.appendChild(folderDiv);
            });
        } else {
            statsDiv.innerHTML = '<h1>Error: Unable to fetch save folders.</h1>';
        }
    } catch (error) {
        statsDiv.innerHTML = `<h1>Error loading stats: ${error.message || error}</h1>`;
        console.error("Error in get_save_folders:", error); // Debug log
    }
}

function selectFolder(folderName) {
    console.log(`Selected folder: ${folderName}`); // Debug log
    if (typeof pywebview !== 'undefined' && pywebview.api) {
        pywebview.api.select_save_folder(folderName).then(response => {
            console.log("Folder selection response:", response); // Debug log
            if (response.status === "success") {
                pywebview.api.load_save_data_page(); // Navigate to the save data page
            }
        }).catch(error => {
            console.error("Error sending selected folder to Python:", error); // Debug log
        });
    }
}

window.onload = () => {
    const checkPyWebViewReady = setInterval(() => {
        if (typeof pywebview !== 'undefined' && pywebview.api) {
            console.log('PyWebView is ready. Fetching save folders...');
            clearInterval(checkPyWebViewReady); // Stop checking once PyWebView is ready
            initializeLoadingPage(); // Call initializeLoadingPage when PyWebView is ready
        } else {
            console.log('Waiting for PyWebView to be ready...');
        }
    }, 2000);
};
