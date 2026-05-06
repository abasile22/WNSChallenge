const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");
const dropText = document.getElementById("drop-text");
const fileList = document.getElementById("file-list");

let selectedFiles = [];

function removeFile(index) {
  selectedFiles.splice(index, 1);
  syncInputFiles();
  renderFiles();
}

function updateFileCount() {
  const fileCountDiv = document.getElementById("file-count");
  const submitBtn = document.getElementById("submit-btn");
  if (fileCountDiv) {
    if (selectedFiles.length === 3) {
      fileCountDiv.textContent = "3 archivos cargados - Listo para procesar";
      fileCountDiv.classList.remove("error");
      fileCountDiv.classList.add("complete");
      submitBtn.disabled = false;
    } else if (selectedFiles.length > 3) {
      fileCountDiv.textContent = `Error: Se cargaron ${selectedFiles.length} archivos, se requieren exactamente 3`;
      fileCountDiv.classList.remove("complete");
      fileCountDiv.classList.add("error");
      submitBtn.disabled = true;
    } else {
      fileCountDiv.textContent = `Se requieren 3 archivos (${selectedFiles.length}/3)`;
      fileCountDiv.classList.remove("complete");
      fileCountDiv.classList.add("error");
      submitBtn.disabled = true;
    }
  }
}

function renderFiles() {
  if (!fileList) return;

  fileList.innerHTML = "";

  if (selectedFiles.length === 0) {
    if (dropText) dropText.textContent = "Arrastrá archivos o hacé click";
    updateFileCount();
    return;
  }

  if (dropText) dropText.textContent = `${selectedFiles.length} archivo(s) seleccionados`;

  selectedFiles.forEach((file, index) => {
    const li = document.createElement("li");
    li.className = "file-item";

    const nameSpan = document.createElement("span");
    nameSpan.textContent = file.name;
    li.appendChild(nameSpan);

    const deleteBtn = document.createElement("button");
    deleteBtn.type = "button";
    deleteBtn.className = "delete-file-btn";
    deleteBtn.innerHTML = "✕";
    deleteBtn.onclick = () => removeFile(index);
    li.appendChild(deleteBtn);

    fileList.appendChild(li);
  });

  updateFileCount();
}

function syncInputFiles() {
  if (!fileInput) return;
  const dt = new DataTransfer();
  selectedFiles.forEach(file => dt.items.add(file));
  fileInput.files = dt.files;
}

if (dropZone) {
  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    const files = Array.from(e.dataTransfer.files);
    selectedFiles = selectedFiles.concat(files);

    syncInputFiles();
    renderFiles();
  });
}

if (fileInput) {
  fileInput.addEventListener("change", () => {
    const files = Array.from(fileInput.files);
    selectedFiles = selectedFiles.concat(files);

    syncInputFiles();
    renderFiles();
  });
}

function loadData() {
  const valor = document.getElementById("meals").value;
  const date = document.getElementById("date").value;

  fetch("/api/meals/data", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      meal: valor,
      date: date
    })
  })
    .then(res => {
      if (!res.ok) {
        return res.text().then(text => {
          try {
            const errorData = JSON.parse(text);
            throw new Error(errorData.error || `Error ${res.status}`);
          } catch (e) {
            if (e instanceof SyntaxError) {
              throw new Error(`Error ${res.status}: respuesta inválida del servidor`);
            }
            throw e;
          }
        });
      }
      return res.json();
    })
    .then(data => {
      const ingredientsContainer = document.getElementById("ingredients");
      ingredientsContainer.innerHTML = "";
      data.ingredients.forEach(ing => {
        const item = document.createElement("li");
        item.className = "ingredient-item";

        const nameSpan = document.createElement("span");
        nameSpan.className = "ingredient-name";
        nameSpan.textContent = ing.ingredient;
        item.appendChild(nameSpan);

        const weightSpan = document.createElement("span");
        weightSpan.className = "ingredient-weight";
        weightSpan.textContent = `${ing.weight}g`;
        item.appendChild(weightSpan);

        ingredientsContainer.appendChild(item);
      });
      document.getElementById("recipe").innerText = data.recipe;
      document.getElementById("total").innerText = data.total_value;
      document.getElementById("total_usd").innerText = data.total_value_usd;
      document.getElementById("results-container").classList.remove("hidden");
    })
    .catch(error => {
      showErrorModal(error.message);
    });
}

function showErrorModal(message) {
  document.getElementById("modal-message").textContent = message;
  document.getElementById("error-modal").classList.remove("hidden");
}

function closeModal() {
  document.getElementById("error-modal").classList.add("hidden");
}