/**
 * @file Lógica de la interfaz de AI-Powered Text Summarizer.
 *
 * Toda la comunicación con el backend se realiza con `fetch`. Las respuestas
 * del modelo se insertan en el DOM mediante `textContent` o creando nodos,
 * nunca con `innerHTML`, para evitar inyección de HTML.
 */

"use strict";

/**
 * Muestra un mensaje de error dentro de un contenedor.
 *
 * @param {HTMLElement} container - Elemento donde se mostrará el mensaje.
 * @param {string} message - Texto del error.
 * @returns {void}
 */
function showError(container, message) {
    container.replaceChildren();
    const paragraph = document.createElement("p");
    paragraph.className = "error-message";
    paragraph.textContent = message;
    container.appendChild(paragraph);
}

/**
 * Sustituye el contenido de un contenedor por un párrafo de texto plano.
 *
 * @param {HTMLElement} container - Elemento que se actualizará.
 * @param {string} text - Texto a mostrar.
 * @returns {void}
 */
function setParagraph(container, text) {
    container.replaceChildren();
    const paragraph = document.createElement("p");
    paragraph.textContent = text;
    container.appendChild(paragraph);
}

/** Área de texto que se desea resumir. */
const textInput = document.getElementById("text-input");
/** Botón que solicita el resumen. */
const summarizeButton = document.getElementById("summarize-button");
/** Contenedor del resumen. */
const summaryDiv = document.getElementById("summary");

/**
 * Envía el texto al backend y muestra el resumen generado.
 *
 * @async
 * @function summarizeText
 * @param {Event} event - Evento de clic del botón.
 * @returns {Promise<void>} No devuelve valor; actualiza el DOM.
 */
async function summarizeText(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append("text", textInput.value);

    try {
        const response = await fetch("/summarize", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            showError(summaryDiv, "Error: Failed to fetch summary.");
            return;
        }

        const data = await response.json();
        setParagraph(summaryDiv, data.summary);
    } catch (error) {
        showError(summaryDiv, "Error: Failed to fetch summary.");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    summarizeButton.addEventListener("click", summarizeText);
});
