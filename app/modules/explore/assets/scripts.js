document.addEventListener('DOMContentLoaded', () => {
    // Trigger search automatically when the page loads (for example, if there's a query in the URL)
    send_query();

    // Add event listener to the search button so it triggers search when clicked
    document.getElementById('search-button').addEventListener('click', send_query);

    // Optionally: if you want to handle query parameter to trigger a search when the page loads
    let urlParams = new URLSearchParams(window.location.search);
    let queryParam = urlParams.get('query');
    if (queryParam && queryParam.trim() !== '') {
        const queryInput = document.getElementById('query');
        queryInput.value = queryParam;
        queryInput.dispatchEvent(new Event('input', {bubbles: true}));
    }
});

function send_query() {
    console.log("send query...");

    // Clear previous results and hide "not found" icon
    document.getElementById('results').innerHTML = '';
    document.getElementById("results_not_found").style.display = "none";

    // Get the filter values (this uses default values to show all datasets ordered by "newest first")
    const query = document.querySelector('#query').value || ''; // Default query is empty (show all datasets)
    const publication_type = document.querySelector('#publication_type').value || 'any'; // Default publication type is "any"
    const sorting = document.querySelector('[name="sorting"]:checked').value || 'newest'; // Default sorting is "newest"
    
    const searchCriteria = {
        csrf_token: document.getElementById('csrf_token').value, // CSRF token
        query,
        publication_type,
        sorting,
    };

    console.log("Search Criteria:", searchCriteria);

    // Update the URL to reflect the current search query
    const url = new URL(window.location);
    url.searchParams.set('query', query);
    url.searchParams.set('publication_type', publication_type);
    url.searchParams.set('sorting', sorting);
    window.history.pushState({}, '', url); // Update the URL without reloading the page

    // Perform the search request (AJAX request)
    fetch('/explore', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(searchCriteria),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data); // Log the search results

        // Clear previous results
        document.getElementById('results').innerHTML = '';

        // Results counter
        const resultCount = data.length;
        const resultText = resultCount === 1 ? 'dataset' : 'datasets';
        document.getElementById('results_number').textContent = `${resultCount} ${resultText} found`;

        // Show/hide "not found" icon
        if (resultCount === 0) {
            document.getElementById("results_not_found").style.display = "block";
        } else {
            document.getElementById("results_not_found").style.display = "none";
        }

        // Display the results
        data.forEach(dataset => {
            let card = document.createElement('div');
            card.className = 'col-12';
            card.innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <div class="d-flex align-items-center justify-content-between">
                            <h3><a href="${dataset.url}">${dataset.title}</a></h3>
                            <div>
                                <span class="badge bg-primary" style="cursor: pointer;" onclick="set_publication_type_as_query('${dataset.publication_type}')">${dataset.publication_type}</span>
                            </div>
                        </div>
                        <p class="text-secondary">${formatDate(dataset.created_at)}</p>

                        <div class="row mb-2">
                            <div class="col-md-4 col-12"><span class=" text-secondary">Description</span></div>
                            <div class="col-md-8 col-12"><p class="card-text">${dataset.description}</p></div>
                        </div>

                        <div class="row mb-2">
                            <div class="col-md-4 col-12"><span class=" text-secondary">Authors</span></div>
                            <div class="col-md-8 col-12">
                                ${dataset.authors.map(author => `
                                    <p class="p-0 m-0">${author.name}${author.affiliation ? ` (${author.affiliation})` : ''}${author.orcid ? ` (${author.orcid})` : ''}</p>
                                `).join('')}
                            </div>
                        </div>

                        <div class="row mb-2">
                            <div class="col-md-4 col-12"><span class=" text-secondary">Tags</span></div>
                            <div class="col-md-8 col-12">
                                ${dataset.tags.map(tag => `<span class="badge bg-primary me-1" style="cursor: pointer;" onclick="set_tag_as_query('${tag}')">${tag}</span>`).join('')}
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-md-4 col-12"></div>
                            <div class="col-md-8 col-12">
                                <a href="${dataset.url}" class="btn btn-outline-primary btn-sm" style="border-radius: 5px;">View dataset</a>
                                <a href="/dataset/download/${dataset.id}" class="btn btn-outline-primary btn-sm" style="border-radius: 5px;">Download (${dataset.total_size_in_human_format})</a>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            document.getElementById('results').appendChild(card);
        });
    });
}

function formatDate(dateString) {
    const options = {day: 'numeric', month: 'long', year: 'numeric', hour: 'numeric', minute: 'numeric'};
    const date = new Date(dateString);
    return date.toLocaleString('en-US', options);
}

function set_tag_as_query(tagName) {
    const queryInput = document.getElementById('query');
    queryInput.value = tagName.trim();
    queryInput.dispatchEvent(new Event('input', {bubbles: true}));
}

function set_publication_type_as_query(publicationType) {
    const publicationTypeSelect = document.getElementById('publication_type');
    for (let i = 0; i < publicationTypeSelect.options.length; i++) {
        if (publicationTypeSelect.options[i].text === publicationType.trim()) {
            // Set the value of the select to the value of the matching option
            publicationTypeSelect.value = publicationTypeSelect.options[i].value;
            break;
        }
    }
    publicationTypeSelect.dispatchEvent(new Event('input', {bubbles: true}));
}

document.getElementById('clear-filters').addEventListener('click', clearFilters);

function clearFilters() {
    // Reset the search query
    let queryInput = document.querySelector('#query');
    queryInput.value = ""; // Reset the query input

    // Reset the publication type to its default value
    let publicationTypeSelect = document.querySelector('#publication_type');
    publicationTypeSelect.value = "any"; // Default value

    // Reset the sorting option to "newest"
    let sortingOptions = document.querySelectorAll('[name="sorting"]');
    sortingOptions.forEach(option => {
        option.checked = option.value == "newest"; // Default sorting
    });

    // Perform a new search with the reset filters
    send_query(); // Trigger the search after clearing filters
}
