let error = document.getElementById('error-wrapper')
let btn = document.getElementById('error-close-btn')
let close = document.getElementById('error-close')
let body = document.querySelector('body')

body.classList.add('error-body')

let closeModal = () => {
    error.classList.add('hidden')
    body.classList.remove('error-body')
}

btn.onclick = () => closeModal()
close.onclick = () => closeModal()