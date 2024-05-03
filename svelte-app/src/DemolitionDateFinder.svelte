<script>
    let address = '';
  
    async function getDemolitionDate() {
      const response = await fetch('http://localhost:5000/get_demolition_date', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ address })
      });
  
      if (response.ok) {
        const data = await response.json();
        document.getElementById('result').textContent = 'Demolition Date: ' + data.demolition_date;
      } else {
        console.error('Error:', await response.text());
      }
    }
  </script>
  
  <h1>Find Demolition Date by Address</h1>
  <input type="text" bind:value={address} placeholder="Enter address here">
  <button on:click={getDemolitionDate}>Search</button>
  <div id="result"></div>
  