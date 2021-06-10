let dropdown = document.getElementById('user-posts-dropdown')
let content = document.getElementById('user-posts-dropdown-content')
let arrow = document.getElementById('user-posts-dropdown-arrow')

dropdown.onclick = () => {
    content.classList.toggle('hidden')
    arrow.classList.toggle('rotate-180')
}