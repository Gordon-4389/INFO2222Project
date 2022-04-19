function str2ab(str) {
  const buf = new ArrayBuffer(str.length);
  const bufView = new Uint8Array(buf);
  for (let i = 0, strLen = str.length; i < strLen; i++) {
    bufView[i] = str.charCodeAt(i);
  }
  return buf;
}
function ab2str(buf) {
  return String.fromCharCode.apply(null, new Uint8Array(buf));
}
async function exportPrivateKey(key) {
  const exported = await window.crypto.subtle.exportKey(
    "pkcs8",
    key
  );
  const exportedAsString = ab2str(exported);
  // console.log(exportedAsString)
  return exportedAsString
  // const exportedAsBase64 = window.btoa(exportedAsString);
  // const pemExported = `-----BEGIN PRIVATE KEY-----\n${exportedAsBase64}\n-----END PRIVATE KEY-----`;

  // const exportKeyOutput = document.querySelector(".exported-key");
  // exportKeyOutput.textContent = pemExported;
  // console.log(exportKeyOutput)
}

async function exportPublicKey(key) {
  const exported = await window.crypto.subtle.exportKey(
    "spki",
    key
  );
  const exportedAsString = ab2str(exported);
  // console.log(exportedAsString)
  return exportedAsString
  // const exportedAsBase64 = window.btoa(exportedAsString);
  // const pemExported = `-----BEGIN PUBLIC KEY-----\n${exportedAsBase64}\n-----END PUBLIC KEY-----`;

  // const exportKeyOutput = document.querySelector(".exported-key");
  // exportKeyOutput.textContent = pemExported;
}
  // const exportedAsBase64 = window.btoa(exportedAsString);
  // const pemExported = `-----BEGIN PUBLIC KEY-----\n${exportedAsBase64}\n-----END PUBLIC KEY-----`;

  // const exportKeyOutput = document.querySelector(".exported-key");
  // exportKeyOutput.classList.add("fade-in");
  // exportKeyOutput.addEventListener("animationend", () => {
  //   exportKeyOutput.classList.remove("fade-in");
  // });
  // exportKeyOutput.textContent = pemExported;

// }

window.crypto.subtle.generateKey(
  {
    name: "RSA-OAEP",
    // Consider using a 4096-bit key for systems that require long-term security
    modulusLength: 2048,
    publicExponent: new Uint8Array([1, 0, 1]),
    hash: "SHA-256",
  },
  true,
  ["encrypt", "decrypt"]
).then((keyPair) => {
  const exportButton = document.querySelector(".spki");
  // exportButton.addEventListener("click", () => {
  var pub = exportPublicKey(keyPair.publicKey);
  var private = exportPrivateKey(keyPair.privateKey)
  // });
});









