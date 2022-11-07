document.getElementById("generate_key").onclick = function generate_key() {
    let method = document.getElementById("method-input").value;
    let keyField = document.getElementById("key-input");

    if (method === "cesar") {
        keyField.value = Math.floor(Math.random() * 24 + 1).toString();
    }

    else if (method === "vigenere") {
        console .log("test");
        let keyLen = Math.floor(Math.random() * 5 + 8);
        let key = "";
        for (let i = 0; i < keyLen; i++) {
            key += String.fromCharCode(97 + Math.floor(Math.random() * 26));
        }
        keyField.value = key;
    }

    else if (method === "aes128") {
        let key = "";
        for (let i = 0; i < 32; i++) { 
            key += Math.floor(Math.random() * 16).toString(16);
        }
        keyField.value = key
    }

    document.getElementById("submit-field").classList.replace("hidden", "animation")
}
