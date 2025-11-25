document.getElementById("formRegistro").addEventListener("submit", async function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const response = await fetch("https://larao.pythonanywhere.com/datos/registrar", {
        method: "POST",
        body: formData
    });
    const data = await response.json();
    if (data.error) {
        alert(data.error);
        return;
    }
    window.location.href = "{{ url_for('iniciar_sesion_bp.iniciar_sesion') }}";
});