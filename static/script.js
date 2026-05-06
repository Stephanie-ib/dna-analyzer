function analyze() {
    const sequence = document.getElementById("sequence").value;
    const strand = document.getElementById("strand").value;

    fetch("/analyze", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({sequence, strand})
    })
    .then(res => res.json())
    .then(data => {
        if(data.error){
            document.getElementById("results").innerHTML = "Invalid sequence!";
            return;
        }

        let html = `<h3>Type: ${data.type}</h3>`;
        html += `<p>mRNA: ${data.rna}</p>`;

        html += "<h3>Translation</h3>";
        data.translation.forEach(t => {
            html += `<p>${t[0]} → ${t[1][0]} (${t[1][1]})</p>`;
        });

        html += `<h3>Protein</h3>`;
        html += `<p>Name: ${data.protein.name}</p>`;
        html += `<p>Organism: ${data.protein.organism}</p>`;

        document.getElementById("results").innerHTML = html;
    });
}

// File Upload
document.getElementById("fileInput").addEventListener("change", function(e){
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = function(){
        document.getElementById("sequence").value = reader.result;
    }
    reader.readAsText(file);
});

// Drag & Drop
const dropZone = document.getElementById("dropZone");

dropZone.addEventListener("dragover", e => e.preventDefault());

dropZone.addEventListener("drop", e => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    const reader = new FileReader();
    reader.onload = function(){
        document.getElementById("sequence").value = reader.result;
    }
    reader.readAsText(file);
});

html += `<div class="card">`;
html += `<h3>Sequence Type</h3><p>${data.type}</p>`;

html += `<h3>mRNA</h3><p>${data.rna}</p>`;

html += `<h3>Translation</h3>`;
data.translation.forEach(t => {
    html += `<p><strong>${t[0]}</strong> → ${t[1][0]} (${t[1][1]})</p>`;
});

html += `<h3>Protein</h3>`;
html += `<p><strong>Name:</strong> ${data.protein.name}</p>`;
html += `<p><strong>Organism:</strong> ${data.protein.organism}</p>`;
html += `</div>`;
