function flash(message, category) {
    switch (category) {
        case "error":
            category = "danger"
            break
        case "success":
            category = "success"
            break
        default:
            category = "primary"
    }
    
    node = document.createElement('div');
    node.classList.add(`alert`)
    node.classList.add(`alert-${category}`)
    node.classList.add(`alert-dismissible`)
    node.setAttribute("role","alert")

    dismiss_button = document.createElement("button")
    dismiss_button.setAttribute("type","button")
    dismiss_button.setAttribute("data-bs-dismiss","alert")
    dismiss_button.classList.add("btn-close")

    node.innerHTML += message
    node.appendChild(dismiss_button)

    document.getElementById("flashes").appendChild(node)
}