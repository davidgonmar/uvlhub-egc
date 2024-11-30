document.addEventListener('DOMContentLoaded', function () {
    // Extract query parameters from the URL
    let urlParams = new URLSearchParams(window.location.search);
    let queryParam = urlParams.get('query');
    let publicationTypeParam = urlParams.get('publication_type') || 'any';  // Default to 'any' if not present
    let sortingParam = urlParams.get('sorting') || 'newest';  // Default to 'newest' if not present
    let startDateParam = urlParams.get('start_date') || '';
    let endDateParam = urlParams.get('end_date') || '';
    let minUvlParam = urlParams.get('min_uvl') || '';
    let maxUvlParam = urlParams.get('max_uvl') || '';
    let minSizeParam = urlParams.get('min_size') || '';
    let maxSizeParam = urlParams.get('max_size') || '';
    let sizeUnitParam = urlParams.get('size_unit') || 'bytes';

    // If there is a query parameter, trigger the search with that query
    if (queryParam && queryParam.trim() !== '') {
        // Pre-fill the search input with the query from the URL
        const queryInput = document.getElementById('query');
        queryInput.value = queryParam.trim();
        queryInput.dispatchEvent(new Event('input', { bubbles: true })); // Trigger input event (optional, depending on implementation)
        
        // Trigger the search function with the query, publication type, and sorting options
        send_query(queryParam, publicationTypeParam, sortingParam, startDateParam, endDateParam, minUvlParam, maxUvlParam, minSizeParam, maxSizeParam, sizeUnitParam);
    } else {
        // If no query in the URL, load all datasets (show default results)
        send_query();
    }
    // Añadir evento al botón de búsqueda
    document.getElementById('search-button').addEventListener('click', function () {
        // Obtener los valores de los filtros
        const query = document.getElementById('query').value;
        const publicationType = document.getElementById('publication_type').value;
        const sorting = document.querySelector('[name="sorting"]:checked').value;

        const startDate = document.getElementById('start_date').value;
        const endDate = document.getElementById('end_date').value;
        const minUvl = document.getElementById('min_uvl').value;
        const maxUvl = document.getElementById('max_uvl').value;

        // Obtener los valores del filtro de tamaño
        const minSize = document.getElementById('min_size').value;
        const maxSize = document.getElementById('max_size').value;
        const sizeUnit = document.getElementById('size_unit').value;

        // Log para verificar los valores de los filtros
        console.log("Filters applied:", { query, publicationType, sorting, startDate, endDate, minUvl, maxUvl, minSize, maxSize, sizeUnit });

        // Llamar a la función de búsqueda pasándole los filtros
        send_query(query, publicationType, sorting, startDate, endDate, minUvl, maxUvl, minSize, maxSize, sizeUnit);
    });

    // Añadir evento al botón de "Clear Filters"
    document.getElementById('clear-filters').addEventListener('click', clearFilters);
});

// Función para limpiar los filtros
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

    // Reset the dates to blank
    let startDateInput = document.querySelector('#start_date');
    startDateInput.value = "";

    let endDateInput = document.querySelector('#end_date');
    endDateInput.value = "";
    
    // Reset the number of UVL models filters
    let minUvlInput = document.querySelector('#min_uvl');
    minUvlInput.value = "";

    let maxUvlInput = document.querySelector('#max_uvl');
    maxUvlInput.value = "";

    // Reset file size filters
    let minSizeInput = document.querySelector('#min_size');
    minSizeInput.value = "";

    let maxSizeInput = document.querySelector('#max_size');
    maxSizeInput.value = "";

    let sizeUnitSelect = document.querySelector('#size_unit');
    sizeUnitSelect.value = "bytes"; // Default value

    // Perform a new search with the reset filters
    send_query(); // Trigger the search after clearing filters
}

// Función para inicializar los filtros de UVL
function setInitialNumUvlFilterMaxMin() {
    document.getElementById('min_uvl').value = document.getElementById('min_uvl').value || 0;
    document.getElementById('max_uvl').value = document.getElementById('max_uvl').value || 1000;
}

function send_query(queryParam = '', publicationTypeParam = 'any', sortingParam = 'newest', startDateParam = '', endDateParam = '', minUvlParam = '', maxUvlParam = '', minSizeParam = '', maxSizeParam = '', sizeUnitParam = 'bytes') {
    console.log("send query...");

    // Limpiar los resultados anteriores y ocultar el icono de "no encontrado"
    document.getElementById('results').innerHTML = '';
    document.getElementById("results_not_found").style.display = "none";

    // Establecer valores iniciales de los filtros
    setInitialNumUvlFilterMaxMin();

    // Preparar los criterios de búsqueda incluyendo los filtros nuevos
    const searchCriteria = {
        csrf_token: document.getElementById('csrf_token').value,
        query: queryParam,
        publication_type: publicationTypeParam,
        sorting: sortingParam,
        start_date: startDateParam,
        end_date: endDateParam,
        min_uvl: minUvlParam,
        max_uvl: maxUvlParam,
        min_size: minSizeParam,
        max_size: maxSizeParam,
        size_unit: sizeUnitParam // Incluir la unidad de tamaño
    };

    // Log para verificar los parámetros de la búsqueda
    console.log("Search Criteria:", searchCriteria);

    // Actualizar la URL para reflejar la consulta de búsqueda actual
    const url = new URL(window.location);
    url.searchParams.set('query', queryParam);
    url.searchParams.set('publication_type', publicationTypeParam);
    url.searchParams.set('sorting', sortingParam);
    url.searchParams.set('start_date', startDateParam);
    url.searchParams.set('end_date', endDateParam);
    url.searchParams.set('min_uvl', minUvlParam);
    url.searchParams.set('max_uvl', maxUvlParam);
    url.searchParams.set('min_size', minSizeParam);
    url.searchParams.set('max_size', maxSizeParam);
    url.searchParams.set('size_unit', sizeUnitParam);
    window.history.pushState({}, '', url);

    // Log para verificar el URL de la solicitud
    console.log("Request URL:", url.toString());

    // Realizar la solicitud de búsqueda
    fetch('/explore', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(searchCriteria),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        console.log("Response Status:", response.status);
        return response.json();
    })
    .then(data => {
        console.log("Response Data:", data);

        // Limpiar los resultados anteriores
        document.getElementById('results').innerHTML = '';

        // Contador de resultados
        const resultCount = data.length;
        const resultText = resultCount === 1 ? 'dataset' : 'datasets';
        document.getElementById('results_number').textContent = `${resultCount} ${resultText} found`;

        // Mostrar/ocultar el icono de "no encontrado"
        if (resultCount === 0) {
            document.getElementById("results_not_found").style.display = "block";
        } else {
            document.getElementById("results_not_found").style.display = "none";
        }

        // Mostrar los resultados
        if (resultCount > 0) {
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
                                <div class="col-md-4 col-12"><span class="text-secondary">Description</span></div>
                                <div class="col-md-8 col-12"><p class="card-text">${dataset.description}</p></div>
                            </div>

                            <div class="row mb-2">
                                <div class="col-md-4 col-12"><span class="text-secondary">Authors</span></div>
                                <div class="col-md-8 col-12">
                                    ${dataset.authors.map(author => `
                                        <p class="p-0 m-0">${author.name}${author.affiliation ? ` (${author.affiliation})` : ''}${author.orcid ? ` (${author.orcid})` : ''}</p>
                                    `).join('')}
                                </div>
                            </div>

                            <div class="row mb-2">
                                <div class="col-md-4 col-12"><span class="text-secondary">Tags</span></div>
                                <div class="col-md-8 col-12">
                                    ${dataset.tags.map(tag => `<span class="badge bg-primary me-1" style="cursor: pointer;" onclick="set_tag_as_query('${tag}')">${tag}</span>`).join('')}
                                </div>
                            </div>
                            
                            <div class="row mb-2">
                                <div class="col-md-8 col-12">
                                    <div class="rating-container" data-average="${ dataset.average_rating }">
                                        <div class="stars-background">
                                            <span class="fa fa-star"></span>
                                            <span class="fa fa-star"></span>
                                            <span class="fa fa-star"></span>
                                            <span class="fa fa-star"></span>
                                            <span class="fa fa-star"></span>
                                        </div>
                                        <div class="stars-foreground" style="width: ${ dataset.average_rating * 20 }%">
                                            <span class="fa fa-star"></span>
                                            <span class="fa fa-star"></span>
                                            <span class="fa fa-star"></span>
                                            <span class="fa fa-star"></span>
                                            <span class="fa fa-star"></span>
                                        </div>
                                        <p id="average-rating" class="text-muted mt-2" style="margin-bottom: -20px; margin-top: 0px !important;">
                                            Rating: ${ dataset.average_rating }
                                        </p>
                                    </div>    
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
        } else {
            console.log("No datasets found.");
        }
    })
    .catch(error => {
        console.error("Error fetching datasets:", error);
    });
}

// Función para formatear la fecha
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    const date = new Date(dateString);
    return date.toLocaleDateString(undefined, options);
}
