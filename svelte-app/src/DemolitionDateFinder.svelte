<script>
    let address = "";

    async function getDemolitionDate() {
        const response = await fetch(
            "http://localhost:5001/get_demolition_date",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ address }),
            },
        );

        if (response.ok) {
            const data = await response.json();
            const resultElement = document.getElementById("result");
            resultElement.textContent = "Demolition Date: " + data.demolition_date;
            resultElement.style.color = "red"; // Set text color to green if successful
            resultElement.style.fontSize = "20px"; // Set font size to 20px
        } else {
            const errorText = await response.text();
            const resultElement = document.getElementById("result");
            resultElement.textContent = "Error: " + errorText;
            resultElement.style.color = "red"; // Set text color to red on error
            resultElement.style.fontSize = "20px"; // Set font size to 20px
            console.error("Error:", errorText);
        }
    
    }
</script>

<style>
    #container {
        display: flex;
        flex-direction: column;
        gap: 30px; /* Adds space between children */
    }

    #result {
        padding: 20px; /* Adds padding inside the result div */
    }

    input, button {
        padding: 10px;
        font-size: 16px; /* Adjust font size as necessary */
    }

    button {
        cursor: pointer; /* Makes it clear that the button is clickable */
        background-color: #f0f0f0; /* Light grey background */
        border: none;
        border-radius: 5px; /* Rounded corners for the button */
    }

    button:hover {
        background-color: #e0e0e0; /* Darker grey on hover */
    }
</style>

<div id="container">

    <h1>Find Demolition Date by Address</h1>
    <input type="text" bind:value={address} placeholder="Enter address here" />
    <button on:click={getDemolitionDate}>Search</button>
    <div id="result"></div>
</div>
