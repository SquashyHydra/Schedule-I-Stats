async function initializeSaveDataPage() {
    const backButton = document.getElementById('back-button');
    const headingDiv = document.getElementById('heading');
    const gameDataDiv = document.getElementById('game-data');

    // Add functionality to the back button
    backButton.addEventListener('click', () => {
        console.log("Back button clicked. Navigating to loading page...");
        window.location.href = './loading.html'; // Navigate back to the loading page
    });

    try {
        console.log("Fetching save game data from Python...");
        const saveDataResponse = await pywebview.api.get_save_data();
        console.log("Save game data response:", saveDataResponse);

        if (saveDataResponse.status === "success") {
            const { account_summary, game_data, variable_data, trash_data, product_info } = saveDataResponse.data;
            
            headingDiv.innerHTML = `<h1>${saveDataResponse.data.selected_save} Data</h1>`; // Set the heading

            gameDataDiv.innerHTML = `
                <div class="data-grid">
                    <div class="data-block">
                        <h2>Account Information</h2>
                        <div class="data-content">
                            <p><strong>Steam Name:</strong> ${account_summary.account_summary.steam_name}</p>
                            <p><strong>Steam ID:</strong> ${saveDataResponse.data.steam_ID}</p>
                            <p><strong>Organisation Name:</strong> ${game_data.OrganisationName}</p>
                            <p><strong>World Seed:</strong> ${game_data.WorldSeed}</p>
                            <p><strong>Console Enabled:</strong> ${game_data.ConsoleEnabled ? "Yes" : "No"}</p>
                        </div>
                    </div>

                    <div class="data-block">
                        <h2>Game Statistics</h2>
                        <div class="data-content">
                            <p><strong>Rank:</strong> ${game_data.Rank}</p>
                            <p><strong>Tier:</strong> ${game_data.Tier}</p>
                            <p><strong>Total XP:</strong> ${game_data.TotalXP}</p>
                            <p><strong>XP:</strong> ${game_data.XP}</p>
                            <p><strong>Time Played:</strong> ${game_data.TimePlayed} hours</p>
                        </div>
                    </div>

                    <div class="data-block">
                        <h2>Financial Data</h2>
                        <div class="data-content">
                            <p><strong>Online Balance:</strong> $${game_data.OnlineBalance}</p>
                            <p><strong>Networth:</strong> $${game_data.Networth}</p>
                            <p><strong>Lifetime Earnings:</strong> $${game_data.LifetimeEarnings}</p>
                        </div>
                    </div>

                    <div class="data-block">
                        <h2>Meth Product Bought</h2>
                        <div class="data-content">
                            <p><strong>Acid Count:</strong> ${variable_data.AcidCount}</p>
                            <p><strong>Phosphorus Count:</strong> ${variable_data.PhosphorusCount}</p>
                        </div>
                    </div>

                    <div class="data-block">
                        <h2>Trash Data</h2>
                        <div class="data-content">
                            <p><strong>Current Trash:</strong> ${trash_data.TrashCount}</p>
                            <p><strong>Collected Trash:</strong> ${variable_data.CollectedTrashCount}</p>
                            <p><strong>Trash Bagged:</strong> ${variable_data.TrashBaggedCount}</p>
                        </div>
                    </div>

                    <div class="data-block">
                        <h2>DeadDrop Data</h2>
                        <div class="data-content">
                            <p><strong>Dead Drops:</strong> ${variable_data.DeadDropCount}</p>
                            <p><strong>Shirley Dead Drops:</strong> ${variable_data.ShirleyDeaddropCount}</p>
                        </div>
                    </div>

                    <div class="data-block">
                        <h2>Deal's & Contracts Data</h2>
                        <div class="data-content">
                            <p><strong>Benji Completed Deals:</strong> ${variable_data.BenjiCompletedDealsCount}</p>
                            <p><strong>Completed Contracts:</strong> ${variable_data.CompletedContractsCount}</p>
                        </div>
                    </div>

                    <div class="data-block">
                        <h2>Product and Sample Data</h2>
                        <div class="data-content">
                            <p><strong>Product Created:</strong> ${product_info.CreatedProductsCount}</p>
                            <p><strong>Packaged Products:</strong> ${variable_data.PackedProductCount}</p>
                            <p><strong>Sample Successes:</strong> ${variable_data.SampleSuccessCount}</p>
                            <p><strong>Sample Rejections:</strong> ${variable_data.SampleRejectedCount}</p>
                        </div>
                    </div>

                    <div class="data-block">
                        <h2>Degenerate Gambling Data</h2>
                        <div class="data-content">
                            <p><strong>Running Game High Score:</strong> ${variable_data.RunningGameHighScore}</p>
                        </div>
                    </div>
                </div>
            `;
        } else {
            gameDataDiv.innerHTML = '<h2>Error: Unable to fetch save game data.</h2>';
        }
    } catch (error) {
        gameDataDiv.innerHTML = `<h2>Error loading game data: ${error.message || error}</h2>`;
        console.error("Error fetching save game data:", error);
    }
}

window.onload = () => {
    const checkPyWebViewReady = setInterval(() => {
        if (typeof pywebview !== 'undefined' && pywebview.api) {
            console.log('PyWebView is ready. Fetching save game data...');
            clearInterval(checkPyWebViewReady);
            initializeSaveDataPage();
        } else {
            console.log('Waiting for PyWebView to be ready...');
        }
    }, 2000);
};
