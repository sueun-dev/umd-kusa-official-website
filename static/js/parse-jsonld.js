// File: parse-jsonld.js

// Use the Fetch API to load JSON-LD data from the external file.
fetch('/static/json/umd-news.json')
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(jsonData => {
    // Create a <script> tag for JSON-LD.
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(jsonData, null, 2);
    document.head.appendChild(script);
    
    // Log the extracted JSON-LD data.
    console.log("Extracted JSON-LD data:", jsonData);
  })
  .catch(error => console.error("Error loading JSON-LD data:", error));
