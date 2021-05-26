 $('.add-to-watch-list').on('click', function() {
    const movieId = $(this).data('id')
    fetch(`/movie/${movieId}`, {
        method: 'GET',
        header: ''
    })
})