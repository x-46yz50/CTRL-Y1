function clampShiftInput() {
  const input = document.getElementById("shift");
  let value = parseInt(input.value);

  if (isNaN(value)) value = 1;
  if (value < 1) value = 1;
  if (value > 26) value = 26;

  input.value = value;
  return value;
}

function caesarCipher(str, shift) {
  return str.replace(/[a-z]/gi, c => {
    const base = c === c.toUpperCase() ? 65 : 97;
    return String.fromCharCode((c.charCodeAt(0) - base + shift + 26) % 26 + base);
  });
}

function encrypt() {
  const shift = clampShiftInput();
  const text = document.getElementById("inputText").value;
  document.getElementById("outputText").value = caesarCipher(text, shift);
}

function decrypt() {
  const shift = clampShiftInput();
  const text = document.getElementById("inputText").value;
  document.getElementById("outputText").value = caesarCipher(text, -shift);
}

function copyResult() {
  const output = document.getElementById("outputText");
  if (!output.value.trim()) return;

  navigator.clipboard.writeText(output.value);

  const btn = document.getElementById("copyBtn");
  const svg = btn.querySelector("svg");

  // muda o ícone para check
  svg.innerHTML = `
    <polyline points="20 6 9 17 4 12" stroke="#00ffFF" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  `;

  setTimeout(() => {
    svg.innerHTML = `
      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
    `;
    svg.setAttribute("stroke", "#ccc");
  }, 1200);
}

// eventos de clique
document.getElementById("encryptBtn").addEventListener("click", encrypt);
document.getElementById("decryptBtn").addEventListener("click", decrypt);
document.getElementById("copyBtn").addEventListener("click", copyResult);

// correção dinâmica ao digitar
document.getElementById("shift").addEventListener("input", clampShiftInput);
