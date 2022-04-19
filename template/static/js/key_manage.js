// const crypto = require("crypto");

// // The `generateKeyPairSync` method accepts two arguments:
// // 1. The type ok keys we want, which in this case is "rsa"
// // 2. An object with the properties of the key
// const { publicKey, privateKey } = crypto.generateKeyPairSync("rsa", {
//   // The standard secure default length for RSA keys is 2048 bits
//   modulusLength: 2048,
// });


// let keyPair = await window.crypto.subtle.generateKey(
//     {
//       name: "RSA-OAEP",
//       modulusLength: 4096,
//       publicExponent: new Uint8Array([1, 0, 1]),
//       hash: "SHA-256"
//     },
//     true,
//     ["encrypt", "decrypt"]
//   );

// const publicKey = keyPair.publicKey;
// await crypto.subtle.exportKey("jwk", keyPair.publicKey);
// const privateKey = keyPair.privateKey;
// await crypto.subtle.exportKey("jwk", keyPair.privateKey);









