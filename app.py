from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Codon table (simplified)
codon_table = {
    "AUG": ("Methionine", "Met"),
    "UUU": ("Phenylalanine", "Phe"),
    "UUC": ("Phenylalanine", "Phe"),
    "UAA": ("STOP", "STOP"),
    "UAG": ("STOP", "STOP"),
    "UGA": ("STOP", "STOP"),
}

def detect_sequence(seq):
    seq = seq.upper()
    if set(seq).issubset(set("ATCG")):
        return "DNA"
    elif set(seq).issubset(set("AUCG")):
        return "RNA"
    else:
        return "INVALID"

def transcribe_dna(seq, strand_type):
    if strand_type == "coding":
        return seq.replace("T", "U")
    else:
        complement = {"A":"U","T":"A","C":"G","G":"C"}
        return "".join(complement[b] for b in seq)

def translate_rna(rna):
    codons = [rna[i:i+3] for i in range(0, len(rna), 3)]
    result = []
    
    for codon in codons:
        if len(codon) < 3:
            continue
        amino = codon_table.get(codon, ("Unknown", "???"))
        result.append((codon, amino))
        if amino[0] == "STOP":
            break
    
    return result

def protein_search(sequence):
    url = f"https://rest.uniprot.org/uniprotkb/search?query={sequence}&format=json&size=1"
    try:
        res = requests.get(url).json()
        if res["results"]:
            protein = res["results"][0]
            return {
                "name": protein["proteinDescription"]["recommendedName"]["fullName"]["value"],
                "organism": protein["organism"]["scientificName"]
            }
    except:
        pass
    return {"name": "No match found", "organism": "N/A"}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    seq = data["sequence"].upper().replace("\n","")
    
    seq_type = detect_sequence(seq)
    
    if seq_type == "INVALID":
        return jsonify({"error": "Invalid sequence"})
    
    if seq_type == "DNA":
        rna = transcribe_dna(seq, data.get("strand", "coding"))
    else:
        rna = seq
    
    translation = translate_rna(rna)
    
    amino_chain = [a[1][0] for a in translation if a[1][0] != "STOP"]
    
    protein_info = protein_search("".join(amino_chain))
    
    return jsonify({
        "type": seq_type,
        "rna": rna,
        "translation": translation,
        "amino_chain": amino_chain,
        "protein": protein_info
    })

if __name__ == "__main__":
    app.run(debug=True)
