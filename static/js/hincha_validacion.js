let form = document.getElementById("formulario");
let deportes= document.getElementById("sport");
let regionSeleccionada = document.getElementById("region");
let comunaSeleccionada = document.getElementById("comuna");
let tipo = document.getElementById("tipo");
let nombre = document.getElementById("nombre");
let email = document.getElementById("email");
let numero = document.getElementById("celular");
let descripcion = document.getElementById("descripcion");

let modal = document.getElementById("modal-container");
let aceptar = document.getElementById("aceptar");
let cancelar = document.getElementById("cancelar");

let modalAccept = document.getElementById("modal-confirmation");
let confirmar = document.getElementById("confirmar");

form.addEventListener("submit", validar);

function validar(event) {
    isValid = true;
    event.preventDefault();

    const setInvalid = (element, error, valid) => {
        element.style.borderColor = "red";
        element.style.boxShadow = "1px 1px 5px rgba(255, 0, 0, 0.5)";
        error.hidden = false;
        valid.hidden = true;
    }

    const setValid = (element, error, valid) => {
        element.style.borderColor = "#1e90ff";
        element.style.boxShadow = "1px 1px 5px #1e90ff";
        error.hidden = true;
        valid.hidden = false;
    }

    const deporteValido = () =>{
        const error = document.getElementById("invalid-sport");
        const valid = document.getElementById("valid-sport");

        const deporte = deportes.selectedOptions;


        if (deporte.length >= 1 && deporte.length <= 3) {
            setValid(deportes, error, valid);
            return true;
        } else {
            setInvalid(deportes, error, valid);
            return false;
        }
          
    }


    const regionValida = () => {
        const error = document.getElementById("invalid-region");
        const valid = document.getElementById("valid-region");

        if (regionSeleccionada.value == "no-selection" || !regionSeleccionada) {
            setInvalid(regionSeleccionada, error, valid);
            return false;
        }
        else {
            setValid(regionSeleccionada, error, valid);
            return true;
        }
    }

    const comunaValida = () => {
        const error = document.getElementById("invalid-comuna");
        const valid = document.getElementById("valid-comuna");

        if (comunaSeleccionada.value == "no-selection-comuna" || !comunaSeleccionada) {
            setInvalid(comunaSeleccionada, error, valid);
            return false;
        }
        else {
            setValid(comunaSeleccionada, error, valid);
            return true;
        }
    }

    const tipoValido = () => {
        const error = document.getElementById("invalid-tipo");
        const valid = document.getElementById("valid-tipo");

        if (tipo.value == "no-selection-tipo") {
            setInvalid(tipo, error, valid);
            return false;
        }
        else {
            setValid(tipo, error, valid);
            return true;
        }
    }

    const nombreValido = () => {
        const error = document.getElementById("invalid-nombre");
        const valid = document.getElementById("valid-nombre");

        if (nombre.value == "" || nombre.value.trim().length < 3 || nombre.value.trim().length > 80 || !isNaN(nombre.value.trim())) {
            setInvalid(nombre, error, valid);
            return false;
        }
        else {
            setValid(nombre, error, valid);
            return true;
        }
    }

    const emailValido = () => {
        const error = document.getElementById("invalid-email");
        const valid = document.getElementById("valid-email");
        const regEx = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        
        if (!regEx.test(email.value) || email.value.trim() === "") {
            setInvalid(email, error, valid);
            return false;
        }
        else {
            setValid(email, error, valid);
            return true;
        }
    }

    const numeroValido = () => {
        const error = document.getElementById("invalid-cel");
        const valid = document.getElementById("valid-cel");

        if (!numero || numero.value.trim() === "") {
            setValid(numero, error, valid);
        }
        else {
            if (isNaN(numero.value) || numero.value.trim().length != 9) {
                setInvalid(numero, error, valid);
                return false;
            }
            else {
                setValid(numero, error, valid);
                return true;
            }
        }
    }
    const descripcionValida = () => {
        const error = document.getElementById("invalid-desc");
        const valid = document.getElementById("valid-desc");

        if (descripcion.value.trim().length > 250) {
            setInvalid(descripcion, error, valid);
            return false;
        }
        setValid(descripcion, error, valid);
        return true;
    }


    const validationArray = [
        deporteValido(),
        regionValida(),
        comunaValida(),
        tipoValido(),
        nombreValido(),
        emailValido(),
        numeroValido(),
        descripcionValida()
    ];

    isValid = !validationArray.includes(false);

    if (isValid) {
        modal.style.display = "flex";
        aceptar.addEventListener("click", () => {
            modal.style.display = "none";
            modalAccept.style.display = "flex";
            confirmar.addEventListener("click", () => {
                form.submit();
            })
        });
        cancelar.addEventListener("click", () => {
            modal.style.display = "none";
            return false;
        });
    }
}