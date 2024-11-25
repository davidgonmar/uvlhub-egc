function test_fakenodo_connection() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/fakenodo/api', true); // Fakenodo endpoint
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.status !== 'success') {
                // Show error message if the connection is not successful
                document.getElementById("test_fakenodo_connection_error").style.display = "block";
                console.log(response); // Log the response for debugging
                console.log(response.status); // Log status for debugging
                console.log(response.message); // Log message for debugging
            } else {
                console.log('Successfully connected to FakenodoAPI');
            }
        } else if (xhr.readyState === 4 && xhr.status !== 200) {
            // Handle case when the request fails
            console.error('Error connecting to Fakenodo:', xhr.status);
        }
    };
    xhr.send();
}